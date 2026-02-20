import os
from pathlib import Path
from manim import *
from jwf.configs import RunnerConfig, SimulationConfig
from jwf.environment import forest

import numpy as np
import jax
from omegaconf import OmegaConf
import pandas as pd
from jwf.render.plot import cells_to_image #This is my own JaxWildfire simulator, code yet to be public!
from jwf.environment.landcover import Landcover

from dataclasses import dataclass

# Create a dummy DictConfig
_CONFIG_PATH = Path(__file__).resolve().parent / "jwf_config.yaml"
JWF_DUMMY_CONFIG = OmegaConf.load(str(_CONFIG_PATH))


class Params:
    def __init__(self, grid_height, grid_width, wind_angle, wind_speed):
        self.grid_height = grid_height
        self.grid_width = grid_width
        self.wind_angle = wind_angle
        self.wind_speed = wind_speed


def run_simulation_custom(rollout_seed, grid_height, grid_width, file_name="jwf"):
    from jwf.environment import sampler
    from jwf.render import plot
    from jwf.spread.runner import SimulationRunner
    import jax
    import jax.random as jr
    import numpy as np

    key = jr.PRNGKey(rollout_seed)
    simulation_key = jr.PRNGKey(rollout_seed + 1)

    prams = Params(
        grid_height=grid_height, grid_width=grid_width, wind_angle=0.0, wind_speed=0.0
    )
    forest_init = sampler.esa_forest(key=key, params=prams)

    sim_config = SimulationConfig(
        p_base=0.6, p_continue=0.5, s_1=0.003, w_1=0.5, w_2=0.5, alpha_gamma=0.1
    )
    run_config = RunnerConfig(num_steps=100, store_history=True)
    runner = SimulationRunner(routine="stochastic", for_calibration=False)
    final_state, rng, history = runner.run(
        forest_init, sim_config, run_config, simulation_key
    )

    # Now emulate the rollout data
    sim_states = history  # Same structure as perform_rollout output
    sim_rewards = np.zeros((history.fire.cells.shape[0],))  # Dummy rewards
    sim_dones = np.zeros((history.fire.cells.shape[0],))  # Dummy dones

    # You might also want to package env_params if needed
    env_params = prams  # or a custom struct

    # Save if needed
    datapath = f"data/{file_name}"
    os.makedirs("data", exist_ok=True)
    # Save selected fields from history into a single .npz file

    fire_states = np.array(history.fire.cells)
    landcover_data = np.array(history.landcover.data)
    wind_direction = np.array(history.wind.direction)
    wind_speed = np.array(history.wind.speed)
    vegetatiion_canopy = np.array(history.vegetation.canopy)
    vegetation_density = np.array(history.vegetation.density)

    np.savez(
        f"{datapath}_sim_data.npz",
        fire_states=np.array(history.fire.cells),
        landcover=np.array(history.landcover.data),
        wind_direction=np.array(history.wind.direction),
        wind_speed=np.array(history.wind.speed),
        vegetation_canopy=np.array(history.vegetation.canopy),
        vegetation_density=np.array(history.vegetation.density),
    )

    return Data(
        fire_states=fire_states,
        wind_direction=wind_direction,
        wind_speed=wind_speed,
        landcover_data=landcover_data,
        vegetation_canopy=vegetatiion_canopy,
        vegetation_density=vegetation_density,
    )


@dataclass
class Data:
    fire_states: np.ndarray
    wind_direction: np.ndarray
    wind_speed: np.ndarray
    landcover_data: np.ndarray
    vegetation_canopy: np.ndarray
    vegetation_density: np.ndarray


class FireSpreadModule:
    """
    Runs a wildfire rollout via perform_rollout, then plays it back
    on a Manim Scene/Slide by recoloring a grid of squares per timestep.
    """

    def __init__(
        self,
        scene,
        rollout_seed: int = 69,
        cell_size: float = 0.05,
        overwrite_simulation: bool = True,
        agent_interaction: bool = False,
    ):
        self.scene = scene

        # before running simulation

        # 1) Run the JAX rollout to get back sim_states and env_params
        data = self._get_data(
            rollout_seed=rollout_seed,
            overwrite_simulation=overwrite_simulation,
            file_name="jwf",
        )
        self.data = data

        T = self.data.fire_states.shape[0]  # Number of timesteps

        self.landcover_states = Landcover(data=self.data.landcover_data[0])
        self.agent_interaction = agent_interaction

        print(
            f"Simulated {T} timesteps with {self.data.fire_states.shape[1]}x{self.data.fire_states.shape[2]} grid."
        )

        self.T = T
        self.H, self.W = self.data.fire_states.shape[1:3]
        # sim_states has shape (T, H, W) of integer cell codes (0=unburned,1=burning,2=burned)
        self.cell_size = cell_size

        # 2) Build a grid of Squares once
        self.squares: list[list[Square]] = []
        # center the grid at ORIGIN
        x0 = -(self.W - 1) * (cell_size) / 2
        y0 = (self.H - 1) * (cell_size) / 2
        for i in range(self.H):
            row = []
            for j in range(self.W):
                sq = Square(side_length=cell_size)
                sq.set_stroke(BLACK, width=1)
                sq.move_to([x0 + j * (cell_size), y0 - i * (cell_size), 0])
                scene.add(sq)
                row.append(sq)
            self.squares.append(row)

    def _run_simulation(self, rollout_seed, file_name: str = "jwf"):
        return run_simulation_custom(
            rollout_seed=rollout_seed,
            grid_height=80,
            grid_width=80,
            file_name=file_name,
        )

    def _get_data(
        self,
        rollout_seed,
        overwrite_simulation: bool = False,
        file_name: str = "jwf",
    ):
        """
        Load or run the simulation to get fire states.
        If overwrite_simulation is True, it will re-run the simulation.
        """
        os.makedirs("data", exist_ok=True)
        if overwrite_simulation:
            # Run the simulation and save the states
            data = self._run_simulation(
                rollout_seed=rollout_seed,
                file_name=file_name,
            )
            return data

        else:
            # Check if the saved states exist
            print("Simulation data found. Loading existing data...")
            # If they exist, load them
            # Load the saved states
            data = np.load(f"data/{file_name}_sim_data.npz", allow_pickle=True)
            fire_cells = data["fire_cells"]
            landcover_data = data["landcover"]
            wind_direction = data["wind_direction"]
            wind_speed = data["wind_speed"]
            vegetation_canopy = data["vegetation_canopy"]
            vegetation_density = data["vegetation_density"]
            return Data(
                fire_states=fire_cells,
                wind_direction=wind_direction,
                wind_speed=wind_speed,
                landcover_data=landcover_data,
                vegetation_canopy=vegetation_canopy,
                vegetation_density=vegetation_density,
            )

    def run(self):
        """
        Iterate over each timestep, recolor the grid, and advance the slide.
        """
        color_map = {
            0: GREEN,  # unburned
            1: RED,  # burning
            2: DARK_GREY,  # burned
        }
        previous_frame = None

        # Show the initial states
        #

        # Create an animation that sets the initial colors
        landcover = self.landcover_states
        print("Converting fire states to RGB image for initial display...")
        print(f"LANDCOVER: {landcover}")
        print(f"LANDCOVER SHAPE: {landcover.data.shape if landcover else 'None'}")
        rgb_image = cells_to_image(self.data.fire_states[0], landcover=landcover)

        anims = []
        for i in range(self.H):
            for j in range(self.W):
                anims.append(
                    self.squares[i][j].animate.set_fill(
                        ManimColor.from_rgb(rgb_image[i, j]),
                        opacity=1,
                        # color_map[frame[i, j]], opacity=1
                    )
                    # self.squares[i][j].animate.set_fill(color_map[0], opacity=1)
                    # self.squares[i][j].animate.set_fill(
                    #     color_map[self.fire_states[0, i, j]], opacity=1
                    # )
                )

        # set all initially to unburned
        #
        print(f"TIME STEPS: {self.T}")
        veg_list = [
            ("Tree", "#006400"),
            ("Shrub", "#FFD700"),
            ("Grass", "#ADFF2F"),
            ("Crop", "#FF69B4"),
            ("Urban", "#8B0000"),
            ("Sparse", "#D3D3D3"),
            ("Snow", "#FFFFFF"),
            ("Water", "#0000CD"),
            ("Wetland", "#7FFFD4"),
            ("Mangrove", "#2E8B57"),
            ("Moss", "#9ACD32"),
        ]
        veg_items = []
        for name, color in veg_list:
            # Use same square size as grid cells
            box = (
                Square(side_length=self.cell_size)
                .set_fill(color, opacity=1)
                .set_stroke(BLACK, width=1)
            )
            label = Text(name, font_size=14)
            item = VGroup(box, label).arrange(RIGHT, buff=0.1)
            veg_items.append(item)
        legend = VGroup(*veg_items).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        # Place legend to the right of the grid, aligned at the top
        sq_group = VGroup(*[sq for row in self.squares for sq in row])
        legend.next_to(sq_group, RIGHT, buff=1).align_to(sq_group, UP)
        self.scene.play(
            AnimationGroup(*anims, lag_ratio=0.1),
            Create(legend),  # Add legend
            run_time=0.8,
        )

        self.scene.next_slide()

        # set the initial fire
        burning_cells = np.where(self.data.fire_states[0] == 1)
        self.scene.play(
            *[
                self.squares[i][j].animate.set_fill(color_map[1], opacity=1)
                for i, j in zip(*burning_cells)
            ],
            run_time=0.5,
        )
        self.scene.wait(0.5)

        # show the initial wind arrow
        wind_text = Text("Wind", font_size=30).to_corner(UL, buff=0.5)

        # First index is time, second is height, third is width
        wind_direction = self.data.wind_direction[
            0
        ][
            0
        ][
            0
        ]  # this is a angle in degrees, where 0 is east, 90 is north, 180 is west, and 270 is south
        wind_speed = self.data.wind_speed[0][0][0]
        wind_arrow = Arrow(
            start=ORIGIN,
            end=1
            * np.array(
                [
                    np.cos(np.radians(wind_direction)),
                    np.sin(np.radians(wind_direction)),
                    0,
                ]
            ),
            color=BLUE,
            buff=0.1,
        ).next_to(wind_text, RIGHT, buff=0.5)
        self.scene.play(
            Write(wind_text),
            Create(wind_arrow),
            run_time=0.5,
        )

        valve_state_prev = -1

        self.scene.next_slide()
        self.reward_text = None  # Initialize reward text
        self.cumulative_reward = 0.0
        for t in range(self.T):
            print(t)
            frame = self.data.fire_states[t]

            if previous_frame is None:
                # Initialize previous_frame on the first iteration
                previous_frame = frame.copy()

            # Check which states changed
            # This is a simple optimization to avoid unnecessary animation

            if previous_frame is not None and np.array_equal(frame, previous_frame):
                # If the frame is the same as the previous one, skip animation
                continue

            i_idxs, j_idxs = np.where(previous_frame != frame)

            previous_frame = frame.copy()

            self.scene.play(
                *[
                    self.squares[i][j].animate.set_fill(
                        color_map[frame[i, j]], opacity=1
                    )
                    for i, j in zip(i_idxs, j_idxs)
                ],
                run_time=0.1,
            )
