from manim import *
import numpy as np

class WildfireCAExplanationModule:
    """
    Module to explain the CA wildfire model in a slide.
    This is a placeholder for the actual implementation.
    """

    BURNED_COLOR = DARK_GREY
    UNBURNED_COLOR = GREEN
    BURNING_COLOR = RED

    def __init__(self, scene):
        self.scene = scene

    def run(self):
        """
        Show a single cell status transitions, then display the full neighborhood.
        """
        # 1. Single cell in center
        self.square_side_length = 1.0
        sq = Square(side_length=self.square_side_length)
        sq.set_fill(self.UNBURNED_COLOR, opacity=0)
        sq.set_stroke(WHITE, width=2)
        sq.move_to(ORIGIN)
        self.scene.play(FadeIn(sq), run_time=0.5)
        self.scene.next_slide()

        # Add initial label
        label = Text("Fire State", font_size=24).next_to(sq, LEFT, buff=0.5)
        self.scene.play(Write(label), run_time=0.5)
        self.scene.next_slide()
     
        text_font_size = 24
        unburned_label = Text(
            "Unburned", font_size=text_font_size, color=self.UNBURNED_COLOR
        ).next_to(sq, LEFT, buff=0.5)
        self.scene.play(
            Transform(label, unburned_label),
            sq.animate.set_fill(self.UNBURNED_COLOR, opacity=1),
            run_time=0.5,
        )
        self.scene.next_slide()

        # 4. Animate cell to Burning, update label
        burning_label = Text(
            "Burning", font_size=text_font_size, color=self.BURNING_COLOR
        ).next_to(sq, LEFT, buff=0.5)
        self.scene.play(
            sq.animate.set_fill(self.BURNING_COLOR, opacity=1),
            Transform(label, burning_label),
            run_time=0.5,
        )
        self.scene.next_slide()

        # 5. Animate cell to Burned, update label
        burned_label = Text(
            "Burned", font_size=text_font_size, color=self.BURNED_COLOR
        ).next_to(sq, LEFT, buff=0.5)
        self.scene.play(
            sq.animate.set_fill(self.BURNED_COLOR, opacity=1),
            Transform(label, burned_label),
            run_time=0.5,
        )
        self.scene.next_slide()
        self.scene.play(FadeOut(label), run_time=0.5)
        self.scene.next_slide()

        # --- Explain cell’s data: wind speed & direction ---

        wind_text = Text("Wind", font_size=40, color=BLUE).next_to(sq, UP, buff=1)
        self.scene.play(Write(wind_text), run_time=0.5)

        self.scene.next_slide()
        arrow = Arrow(start=ORIGIN, end=RIGHT, buff=0, color=BLUE)
        speed_label = Text("Wind Speed: 10 m/s", font_size=20, color=BLUE).next_to(
            arrow, DOWN, buff=0.5
        )
        self.scene.play(GrowArrow(arrow), Write(speed_label), run_time=0.5)
        self.scene.play(
            Rotate(arrow, angle=PI / 4, about_point=arrow.get_start()), run_time=0.5
        )
        self.scene.play(
            Rotate(arrow, angle=-PI / 4, about_point=arrow.get_start()), run_time=0.5
        )
        self.scene.wait(1)
        self.scene.play(FadeOut(arrow), FadeOut(speed_label), run_time=0.5)
        self.scene.next_slide()

        # --- Explain topography (slope) in 3×3 ---
        slope_cells = []
        for i in range(3):
            row = []
            for j in range(3):
                c = (
                    Square(side_length=self.square_side_length)
                    .set_fill(GREY_B, opacity=0.5)
                    .set_stroke(BLACK, width=1)
                )
                slope_text = Text(f"{(i - j) * 5}°", font_size=12).move_to(
                    c.get_center()
                )
                row.append(VGroup(c, slope_text))
            slope_cells.append(row)
        slope_grid = (
            VGroup(*[VGroup(*row).arrange(RIGHT, buff=0.05) for row in slope_cells])
            .arrange(DOWN, buff=0.05)
            .move_to(ORIGIN)
        )
        slope_grid.set_opacity(0.6)
        slope_text = Text("Topography", font_size=40, color=YELLOW).next_to(
            slope_grid, UP, buff=0.5
        )
        self.scene.play(
            FadeIn(slope_grid),
            wind_text.animate.to_corner(UP + LEFT, buff=0.5),
            Write(slope_text),
            run_time=0.5,
        )

        self.scene.next_slide()
        self.scene.play(FadeOut(slope_grid), run_time=0.5)
        self.scene.wait(0.5)

        # --- Explain vegetation types ---
        vegetation_text = Text("Vegetation", font_size=40, color=GREEN).next_to(
            sq, UP, buff=2
        )
        

        # --- Show vegetation classes with shortened names below icons ---
        veg_list = [
            ("Tree", "#006400"),  # Tree cover
            ("Shrub", "#FFD700"),  # Shrubland
            ("Grass", "#ADFF2F"),  # Grassland
            ("Crop", "#FF69B4"),  # Cropland
            ("Urban", "#8B0000"),  # Built-up
            ("Sparse", "#D3D3D3"),  # Bare/sparse vegetation
            ("Snow", "#FFFFFF"),  # Snow and ice
            ("Water", "#0000CD"),  # Permanent water bodies
            ("Wetland", "#7FFFD4"),  # Herbaceous wetland
            ("Mangrove", "#2E8B57"),  # Mangroves
            ("Moss", "#9ACD32"),  # Moss and lichen
        ]
        veg_items = []
        for name, color in veg_list:
            box = (
                Square(side_length=self.square_side_length)
                .set_fill(color, opacity=1)
                .set_stroke(BLACK, width=1)
            )
            label = Text(name, font_size=14).next_to(box, DOWN, buff=0.1)
            veg_items.append(VGroup(box, label))
        # Arrange in two rows (6 items first, 5 next) for readability
        veg_grid = (
            VGroup(*veg_items)
            .arrange_in_grid(n_rows=2, n_cols=6, buff=(0.1, 0.1))
            .move_to(ORIGIN)
        )

        self.scene.play(
            FadeIn(veg_grid),
            FadeOut(sq),
            slope_text.animate.next_to(wind_text, DOWN, buff=0.5, aligned_edge=LEFT),
            sq.animate.set_fill(GREEN, opacity=1),
            Write(vegetation_text),
            run_time=0.5,
        )
        self.scene.next_slide()

        self.scene.play(
            FadeOut(veg_grid),
            vegetation_text.animate.next_to(
                slope_text, DOWN, buff=0.5, aligned_edge=LEFT
            ),
            run_time=0.5,
        )
        self.scene.wait(0.5)

        # Now show how fire spreads
        # 1. Show a single cell in the center
        self.scene.play(
            FadeIn(sq),
            sq.animate.set_fill(self.UNBURNED_COLOR, opacity=1),
            run_time=0.5,
        )
        self.scene.next_slide()

        # Add the neighborhood grid
        # 2. Show the neighborhood grid around the cell

        # 5. Show 3x3 neighborhood grid
        cells = []
        for i in range(3):
            row = []
            for j in range(3):
                cell = Square(side_length=self.square_side_length)
                cell.set_fill(self.UNBURNED_COLOR, opacity=1)
                cell.set_stroke(BLACK, width=1)
                row.append(cell)
            cells.append(row)

        burn_indices = [(2, 1), (1, 0), (2, 2)]

        for i, j in burn_indices:
            cells[i][j].set_fill(self.BURNING_COLOR, opacity=1)

        row_groups = VGroup(*[VGroup(*row).arrange(RIGHT, buff=0) for row in cells])
        grid_group = VGroup(*row_groups).arrange(DOWN, buff=0).move_to(ORIGIN)
        self.scene.play(Create(grid_group), run_time=0.5)
        self.scene.wait(1)

        # Show an arrow pointing from burngin to the center cell
        arrows = VGroup()
        for i, j in burn_indices:
            arrow = Arrow(
                start=cells[i][j].get_center(),
                end=sq.get_center(),
                buff=0,
                color=WHITE,
            )
            arrows.add(arrow)
        self.scene.play(*[GrowArrow(arrow) for arrow in arrows], run_time=0.5)
        self.scene.wait(1)
        # Show the burning cells

        # write p_ignite
        p_ignite = Tex(r"$p_\text{ignite}$", font_size=40)
        p_ignite.next_to(row_groups, UP, buff=0.5)

        self.scene.play(Write(p_ignite), run_time=0.5)
        self.scene.wait(1)

    
