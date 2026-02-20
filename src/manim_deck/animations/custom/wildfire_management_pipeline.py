from manim import (
    Scene,
    Square,
    VGroup,
    Text,
    Circle,
    UL,
    GREEN,
    RED,
    DARK_GREY,
    BLUE,
    BLACK,
    LEFT,
    RIGHT,
    Create,
    UP,
    Arrow,
    Rectangle,
    YELLOW,
    DOWN,
    Write,
    Transform,
    TransformFromCopy,
)
import numpy as np


class HierarhchicalPipelineModule:
    """
    Visualize initial pipeline inputs: fire state grid, k-step forecast, and available resources.
    """

    def __init__(
        self,
        scene: Scene,
        resources: int,
        cell_size: float = 0.125,
    ):
        self.scene = scene
        self.resources = resources

        self.state_color = {0: GREEN, 1: RED, 2: DARK_GREY}

        total_size = 1.5
        # Define the base low-resolution pattern
        base_pattern = np.array(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 0, 1, 1, 0, 0],
                [0, 1, 2, 2, 1, 0],
                [0, 0, 2, 2, 2, 0],
                [0, 0, 0, 1, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ],
            dtype=int,
        )

        forecast_pattern = np.array(
            [
                [0, 0, 1, 1, 0, 0],
                [0, 1, 2, 2, 1, 0],
                [0, 2, 2, 2, 2, 0],
                [0, 1, 2, 2, 2, 0],
                [0, 0, 1, 2, 0, 0],
                [0, 0, 0, 1, 0, 0],
            ],
            dtype=int,
        )

        self.cell_size = total_size

        # Upscale the pattern to create higher resolution grids
        upscale_factor = 2
        self.fire_state = np.kron(
            base_pattern, np.ones((upscale_factor, upscale_factor), dtype=int)
        )
        self.forecast = np.kron(
            forecast_pattern, np.ones((upscale_factor, upscale_factor), dtype=int)
        )

        total_size = 1.5
        self.cell_size = (
            total_size / self.fire_state.shape[0]
        )  # Adjust cell size based on grid size

    def get_mobjects(self) -> VGroup:
        # Main fire-state grid
        H, W = self.fire_state.shape
        squares = []
        for i in range(H):
            for j in range(W):
                sq = Square(side_length=self.cell_size)
                sq.set_stroke(BLACK, width=0.5)
                state = int(self.fire_state[i, j])
                color = self.state_color.get(state, DARK_GREY)
                sq.set_fill(color, opacity=1)
                squares.append(sq)

        grid = VGroup(*squares).arrange_in_grid(rows=H, cols=W, buff=0.03)
        grid.to_corner(UL, buff=1)
        init_label = Text("Fire State", font_size=18).next_to(grid, UP, buff=0.1)
        grid = VGroup(grid, init_label)

        # Dummy forecast grid
        h, w = self.forecast.shape
        fg_sqs = []
        for i in range(h):
            for j in range(w):
                fg = Square(side_length=self.cell_size)
                fg.set_stroke(BLACK, width=0.3)
                st = int(self.forecast[i, j])
                color = self.state_color.get(st, DARK_GREY)
                fg.set_fill(color, opacity=1)
                fg_sqs.append(fg)
        fg_group = VGroup(*fg_sqs).arrange_in_grid(rows=h, cols=w, buff=0.03)
        label = Text("Forecast", font_size=18).next_to(fg_group, UP, buff=0.1)
        forecast_vg = VGroup(fg_group, label).next_to(grid, RIGHT, buff=0.5)

        # Available resources
        # We use the original larger cell_size for the resource circles to keep them visible
        resource_circles = []
        for _ in range(self.resources):
            c = Circle(
                radius=self.cell_size * 2 / 2
            )  # Use original cell_size for visibility
            c.set_fill(BLUE, opacity=1)
            c.set_stroke(BLACK, width=0.5)
            resource_circles.append(c)
        resources_vg = VGroup(*resource_circles).arrange(RIGHT, buff=0.2)
        resources_vg.next_to(forecast_vg, RIGHT, buff=1)
        res_label = Text("Resources", font_size=20).next_to(resources_vg, UP, buff=0.1)

        incident_commander = Text("Incident Commander", font_size=24)
        incident_commander.next_to(res_label, RIGHT, buff=1)
        arrow_to_commander = Arrow(
            res_label.get_right() + RIGHT * 0.2,
            incident_commander.get_left(),
            buff=0.1,
            color=BLUE,
        )

        # Highlight four quadrants with semi-transparent rectangles
        # Copy initial grid to Incident Commander
        grid_copy = grid.copy().scale(0.8).next_to(incident_commander, DOWN, buff=0.5)
        grid_center = grid_copy.get_center()
        grid_top = grid_copy.get_top()[1]
        grid_bottom = grid_copy.get_bottom()[1]
        grid_left = grid_copy.get_left()[0]
        grid_right = grid_copy.get_right()[0]
        quad_w = (grid_right - grid_left) / 2
        quad_h = (grid_top - grid_bottom) / 2

        rects = []
        labels = []
        offsets = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        fill_colors = [YELLOW, GREEN, RED, BLUE]
        # Adjusting label font size to be more readable on smaller quadrants
        for idx, (dx, dy) in enumerate(offsets, start=1):
            rect = Rectangle(
                width=quad_w,
                height=quad_h,
                stroke_color=BLACK,
                stroke_width=1,
                fill_color=fill_colors[idx - 1],
                fill_opacity=0.8,
            )
            rect.move_to(grid_center + np.array([dx * quad_w / 2, dy * quad_h / 2, 0]))
            lbl = Text(str(idx), font_size=18).move_to(rect.get_center())
            rects.append(rect)
            labels.append(lbl)
        quadrant_overlays = VGroup(*rects, *labels)

        # Sector manager views: each sees its own quadrant
        H, W = self.fire_state.shape
        mid_row, mid_col = H // 2, W // 2
        sectors = [
            self.fire_state[0:mid_row, 0:mid_col],  # top-left
            self.fire_state[0:mid_row, mid_col:W],  # top-right
            self.fire_state[mid_row:H, mid_col:W],  # bottom-right
            self.fire_state[mid_row:H, 0:mid_col],  # bottom-left
        ]
        sector_groups = []
        for idx, sector in enumerate(sectors, start=1):
            h_s, w_s = sector.shape
            # Build the sector grid
            sqs = []
            for i in range(h_s):
                for j in range(w_s):
                    sq = Square(side_length=self.cell_size)
                    sq.set_stroke(BLACK, width=0.5)
                    st = int(sector[i, j])
                    col = self.state_color.get(st, DARK_GREY)
                    sq.set_fill(col, opacity=1)
                    sqs.append(sq)
            sec_grid = VGroup(*sqs).arrange_in_grid(rows=h_s, cols=w_s, buff=0.03)

            # Background overlay rectangle
            sec_w = sec_grid.get_width()
            sec_h = sec_grid.get_height()
            bg_rect = Rectangle(
                width=sec_w,
                height=sec_h,
                stroke_color=BLACK,
                stroke_width=1,
                fill_color=fill_colors[idx - 1],
                fill_opacity=0.2,
            )
            bg_rect.move_to(sec_grid.get_center())

            # Overlay region number
            num_lbl = Text(str(idx), font_size=18)
            num_lbl.move_to(sec_grid.get_center())

            # Group grid, background, and number
            sec_with_bg = VGroup(bg_rect, sec_grid, num_lbl)

            # Label below
            label = Text(f"Sector Manager {idx}", font_size=18)
            sec_vg = VGroup(sec_with_bg, label).arrange(DOWN, buff=0.1)

            sector_groups.append(sec_vg)
        sectors_vg = VGroup(*sector_groups).arrange(RIGHT, buff=1)
        sectors_vg.next_to(grid_copy, DOWN, buff=1)

        # Tactical grid for Worker with local observation
        t_H, t_W = sector.shape
        t_H = t_H // 2
        t_W = t_W // 2
        t_sqs = []
        for i in range(t_H):
            for j in range(t_W):
                sq = Square(side_length=self.cell_size)
                sq.set_stroke(BLACK, width=0.5)
                sq.set_fill(DARK_GREY, opacity=0.3)
                t_sqs.append(sq)
        t_grid = VGroup(*t_sqs).arrange_in_grid(rows=t_H, cols=t_W, buff=0.03)
        # place in bottom-right corner
        t_grid.to_corner(DOWN + RIGHT, buff=1)
        worker_label = Text("Worker", font_size=18).next_to(t_grid, DOWN, buff=0.1)
        tactical_vg = VGroup(t_grid, worker_label)

        # Store components for staged animation
        self.grid = grid
        self.forecast_vg = forecast_vg
        self.res_label = res_label
        self.resources_vg = resources_vg
        self.incident_commander = incident_commander
        self.arrow_to_commander = arrow_to_commander
        self.grid_copy = grid_copy
        self.quadrant_overlays = quadrant_overlays
        self.sectors_vg = sectors_vg
        # Store tactical view
        self.tactical_vg = tactical_vg

        return VGroup(
            grid,
            forecast_vg,
            res_label,
            resources_vg,
            incident_commander,
            arrow_to_commander,
            grid_copy,
            quadrant_overlays,
            sectors_vg,
            tactical_vg,
        )

    def run(self):
        """
        Play the pipeline animation in stages with waits.
        """
        # Ensure mobjects are created and stored
        self.get_mobjects()

        # 1. Show the main grid
        self.scene.play(Create(self.grid))
        self.scene.next_slide()

        # 2. Show forecast
        self.scene.play(Create(self.forecast_vg))
        self.scene.next_slide()

        # 3. Show resources
        self.scene.play(Create(self.res_label), Create(self.resources_vg))
        self.scene.next_slide()

        # Draw surrounding rectangle for fire state, forecast and resources
        # surrounding_rect = Rectangle(
        #     width=self.grid.get_width() + self.forecast_vg.get_width() + self.resources_vg.get_width() + 3,
        #     height=max(self.grid.get_height(), self.forecast_vg.get_height(), self.resources_vg.get_height()) + 1,
        #     stroke_color=YELLOW,
        #     stroke_width=1,
        #     fill_color=YELLOW,
        #     fill_opacity=0.2
        # )
        # self.scene.bring_to_back(surrounding_rect)
        # surrounding_rect.move_to(
        #     self.grid.get_center() + RIGHT * (self.forecast_vg.get_width() / 2 + self.resources_vg.get_width() / 2 + 0.5)
        # )
        # self.scene.play(Create(surrounding_rect))

        # 4. Announce Incident Commander
        self.scene.play(
            Write(self.incident_commander),
            Create(self.arrow_to_commander),
            Create(self.grid_copy),
        )
        self.scene.next_slide()

        # Move the resources next to the commander's grid
        self.scene.play(
            self.resources_vg.animate.next_to(self.grid_copy, LEFT, buff=0.5)
        )

        # 7. Highlight quadrants
        self.scene.play(Create(self.quadrant_overlays))
        self.scene.next_slide()

        # 8. Transform each quadrant into its sector view
        for idx, sec_vg in enumerate(self.sectors_vg):
            src_rect = self.quadrant_overlays[idx].copy()
            self.scene.add(src_rect)
            self.scene.play(Transform(src_rect, sec_vg), run_time=1)
            self.scene.wait(0.5)

        # Animate how incident commander distribute reocurse
        # one goes to sector 1 and onw goes to sector 3

        self.scene.play(
            # Move resources to sector 1
            self.resources_vg[0].animate.next_to(self.sectors_vg[0], UP, buff=0.5),
            # Move resources to sector 3
            self.resources_vg[1].animate.next_to(self.sectors_vg[2], UP, buff=0.5),
            run_time=1,
        )

        self.scene.bring_to_front(self.resources_vg)
        self.scene.next_slide()
        # Animate how the resource gets deploy on one grid cell
        # Move first resource to sector 1
        self.scene.play(
            self.resources_vg[0].animate.move_to(
                self.sectors_vg[0].get_center() + UP * 0.2
            ),
            # Move second resource to sector 3
            self.resources_vg[1].animate.move_to(
                self.sectors_vg[2].get_center() + UP * 0.2
            ),
            run_time=1,
        )

        self.scene.next_slide()

        # 9. Show worker grids
        worker1 = self.tactical_vg
        worker2 = self.tactical_vg.copy()
        worker1.next_to(self.sectors_vg[0], DOWN, buff=0.5)
        worker2.next_to(self.sectors_vg[2], DOWN, buff=0.5)

        # Prepare invisible resource copies at each worker center
        resource1 = self.resources_vg[0].copy().move_to(worker1.get_center() + UP * 0.2)
        resource2 = self.resources_vg[1].copy().move_to(worker2.get_center() + UP * 0.2)

        self.scene.add(resource1, resource2)

        self.scene.play(
            Create(worker1),
            Create(worker2),
            TransformFromCopy(self.resources_vg[0], resource1),
            TransformFromCopy(self.resources_vg[1], resource2),
        )

        self.scene.next_slide()

