from manim import *


class AirtankerModule:
    """
    Module to demonstrate a small forest grid, an airtanker at center,
    its local observation, possible moves, and valve control.
    """

    def __init__(
        self,
        scene,
        rows: int = 7,
        cols: int = 7,
        cell_size: float = 0.6,
    ):
        self.scene = scene
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.spacing = cell_size + 0.1

        self.squares = []
        self.grid_group = VGroup()
        x0 = -(cols - 1) * self.spacing / 2
        y0 = (rows - 1) * self.spacing / 2
        for i in range(rows):
            row = []
            for j in range(cols):
                sq = Square(side_length=self.cell_size)
                sq.set_stroke(BLACK, width=1)
                sq.set_fill(GREEN, opacity=0.8)
                sq.move_to([x0 + j * self.spacing, y0 - i * self.spacing, 0])
                self.grid_group.add(sq)
                row.append(sq)
            self.squares.append(row)

    def run(self):
        """
        Plays the airtanker demonstration on the provided scene.
        """
        self.scene.add(self.grid_group)
        self.scene.next_slide()

        mid_i, mid_j = self.rows // 2, self.cols // 2
        tanker = SVGMobject("images/airplane.svg").scale(0.3)
        tanker.set_color(YELLOW).set_stroke(BLACK, width=1)
        tanker.move_to(self.squares[mid_i][mid_j].get_center())
        self.tanker = tanker
        self.scene.play(FadeIn(tanker))
        self.scene.next_slide()

        view_radius = 1
        obs_cells = [
            self.squares[i][j]
            for i in range(
                max(0, mid_i - view_radius), min(self.rows, mid_i + view_radius + 1)
            )
            for j in range(
                max(0, mid_j - view_radius), min(self.cols, mid_j + view_radius + 1)
            )
        ]
        obs_box = SurroundingRectangle(
            VGroup(*obs_cells), color=PURPLE, buff=0, stroke_width=8
        )
        self.scene.play(Create(obs_box))
        self.scene.next_slide()

        arrows = []
        for di, dj in [
            (-1, 0),
            (1, 0),
            (0, -1),
            (0, 1),
            (-1, -1),
            (-1, 1),
            (1, -1),
            (1, 1),
        ]:
            ni, nj = mid_i + di, mid_j + dj
            if 0 <= ni < self.rows and 0 <= nj < self.cols:
                arr = Arrow(
                    start=tanker.get_center(),
                    end=self.squares[ni][nj].get_center(),
                    buff=0,
                )
                arrows.append(arr)
        self.scene.play(*[GrowArrow(a) for a in arrows])
        self.scene.next_slide()

        self.scene.play(*[FadeOut(a) for a in arrows])
        self.scene.next_slide()

        valve_text = Text("Valve Open", font_size=24).next_to(
            VGroup(*obs_cells), DOWN, buff=0.5
        )
        self.scene.play(Write(valve_text))
        self.scene.wait(0.1)

        self.scene.play(self.squares[mid_i][mid_j].animate.set_fill(BLUE, opacity=1))
        self.scene.wait(0.5)

        close_text = Text("Valve Closed", font_size=24).next_to(
            VGroup(*obs_cells), DOWN, buff=0.5
        )
        self.scene.play(Transform(valve_text, close_text))
        self.scene.wait(0.5)

        current_i, current_j = mid_i, mid_j
        trajectory = [
            (1, 0),
            (1, 0),
            (1, 0),
            (-1, -1),
            (-1, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1),
            (-1, 1),
            (0, 1),
            (1, 1),
            (1, 0),
            (1, -1),
            (1, -1),
            (1, -1),
        ]

        valve_states = [
            False,
            False,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            True,
        ]

        current_i, current_j = mid_i, mid_j
        for (di, dj), valve in zip(trajectory, valve_states):
            anims = []
            current_i += di
            current_j += dj
            target = self.squares[current_i][current_j].get_center()

            new_obs_cells = VGroup(
                *[
                    self.squares[i][j]
                    for i in range(
                        max(0, current_i - view_radius),
                        min(self.rows, current_i + view_radius + 1),
                    )
                    for j in range(
                        max(0, current_j - view_radius),
                        min(self.cols, current_j + view_radius + 1),
                    )
                ]
            )
            new_obs_box = SurroundingRectangle(
                new_obs_cells, color=PURPLE, buff=0, stroke_width=8
            )
            anims.append(Transform(obs_box, new_obs_box))

            anims.append(self.tanker.animate.move_to(target))

            new_text_content = "Valve Open" if valve else "Valve Closed"
            new_valve_text = Text(new_text_content, font_size=24).next_to(
                new_obs_box, DOWN, buff=0.5
            )
            anims.append(Transform(valve_text, new_valve_text))

            if valve:
                anims.append(
                    self.squares[current_i][current_j].animate.set_fill(BLUE, opacity=1)
                )

            self.scene.play(*anims, run_time=0.1)
            self.scene.wait(0.1)
