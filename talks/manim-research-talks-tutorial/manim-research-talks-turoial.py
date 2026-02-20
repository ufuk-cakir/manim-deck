"""Tutorial presentation built on the manim_deck template."""

from __future__ import annotations

from manim import *  # noqa: F401,F403

from manim_deck import TemplateSlide
from manim_deck.templates import DARK_THEME

HAS_RESEARCH_MODULES = True

from manim_deck.animations.custom.wildfire_management_pipeline import HierarhchicalPipelineModule

from manim_deck.animations.custom.cellular_automata import WildfireCAExplanationModule
from manim_deck.animations.custom.airtanker import AirtankerModule
from manim_deck.animations.custom.jwf import FireSpreadModule

class TutorialPresentation(TemplateSlide):
	section_titles = [
		"About me",
		"What is Manim?",
		"Why should you care?",
		"Thinking in Manim",
		"Our first animation",
		"Manim Slides",
		"Custom Templates",
		"Conclusion",
	]
	theme = DARK_THEME

	def construct(self):
		# TITLE SLIDE
		# ─────────────────────────────────────────────
		self.title_slide(
			"Making Cool Animations\n& Presentations with Manim",
			logos=["images/ori-logo.png", "images/ie-logo.png", "images/goals-logo.png"],
			occasion="A2I Research Group Tutorial",
			scale_title=0.65,
			scale_occasion=0.9,
		)

		# SECTION 1: WHO AM I?
		# ─────────────────────────────────────────────
		self.section_slide(1, "About me")

		name = self.author or "Your Name"
		self.list_slide(
			"About Me",
			[
                                "(Astro)Physics in Heidelberg, Germany",
				f"DPhil at GOALS (next door!)",
				"Research Reinforcement Learning for wildfire management",
				"Bradley is my best friend.",
			],
			lagged_start=True,
		)

		self.statement_slide("What I am interested in...")

		if HAS_RESEARCH_MODULES:
			self._research_demo_slides()
		else:
			self._research_placeholder_slides()

		self.statement_slide("All of this was made with Manim.")

		self.list_slide(
			"What I will cover",
			[
				"I will NOT give an exhaustive API tutorial",
				"I will motivate why you should try it",
				"I will give you a starting point to get into it",
				"I will share my template and code for you to reuse",
			],
		)

		# SECTION 2: WHAT IS MANIM?
		# ─────────────────────────────────────────────
		self.section_slide(2, "What is Manim?")

		self.statement_slide("A Python library for creating\nmathematical animations.")

		self.list_slide(
			"What is Manim?",
			[
				"Created by Grant Sanderson (3Blue1Brown)",
				"Open Source Community edition: pip install manim",
				"Programmatic: everythin is code!",
			],
		)

		self._what_is_manim_demo()

		# SECTION 3: WHY SHOULD YOU CARE?
		# ─────────────────────────────────────────────
		self.section_slide(3, "Why should you care?")

		self.statement_slide("You want your audience to enjoy the talk.")

		self.list_slide(
			"Why Manim?",
			[
				"Engaging visuals keep your audience focused",
				"Building the animation forces you to distil your message",
				"Everything is customizable and reusable",
			],
		)

		self._boring_vs_animated()

		# SECTION 4: THINKING IN MANIM
		# ─────────────────────────────────────────────
		self.section_slide(4, "Thinking in Manim")

		self._thinking_in_manim()

		# SECTION 5: OUR FIRST ANIMATION
		# ─────────────────────────────────────────────
		self.section_slide(5, "Our first animation")

		self._first_animation_demo()

		# SECTION 6: MANIM SLIDES
		self.section_slide(6, "Manim Slides")

		self.statement_slide("This talk is a Manim Slides presentation!")

		self.list_slide(
			"Manim Slides",
			[
				"pip install manim-slides",
				"Extends Manim with Slide class and next\\_slide()",
				"Uses Reveal.js under the hood",
				"Export to HTML, PDF, or present live",
			],
		)

		self._manim_slides_demo()

		# SECTION 7: CUSTOM TEMPLATES
		self.section_slide(7, "Custom Templates")

		self.statement_slide("This is where the fun begins.")

		self.list_slide(
			"Why templates?",
			[
				"Everything is programmable!",
				"Define reusable layouts: title, list, statement, section",
				"Consistent styling across your whole talk",
				"Add progress bars, footers, logos automatically",
			],
		)

		self._template_walkthrough()

		# SECTION 8: CONCLUSION
		# ─────────────────────────────────────────────
		self.section_slide(8, "Conclusion")

		self.list_slide(
			"Getting Started",
			[
				"Install: pip install manim manim-slides",
				"Check manim docs or manim subreddit!",
				"will send you my template + code",
				"drop me a slack message!",
			],
		)

		self.statement_slide("Questions?")

	# HELPERS

	def _code_block(self, code_text: str, *, font_size: int = 20, line_numbers: bool = False):
		return Code(
			code_string=code_text,
			language="python",
			background="window",
			add_line_numbers=line_numbers,
			paragraph_config={
				"font_size": font_size,
				"font": self.theme.code_font,
			},
			background_config={"fill_color": self.theme.panel},
		)

	def _research_demo_slides(self):
		self.update_canvas()
		self.statement_slide("Wildfire Management Problem")
		self.update_canvas()

		# here we loud our custom animations and run it with .run()
		HierarhchicalPipelineModule(self,resources=2).run()
		self.next_slide()

		

		self.statement_slide("JaxWildfire")

		self.update_canvas()
		wildfire_ca = WildfireCAExplanationModule(self)
		wildfire_ca.run()

		self.statement_slide("Simulating Fire Spread")
		self.next_slide()
		self.update_canvas()

		FireSpreadModule(self, agent_interaction=False).run()

		self.statement_slide("Single Agent Airtanker")
		self.update_canvas()
		AirtankerModule(self).run()
		self.next_slide()




	def _what_is_manim_demo(self):
		"""Show a simple Manim example: code on left, result on right."""
		self.update_canvas()

		header = Text("The simplest Manim scene", font_size=48, color=self.theme.accent).to_edge(UP)
		code_text = '''from manim import *

		class MyScene(Scene):
			def construct(self):
				circle = Circle(
					radius=1,
					color=BLUE
				)
				self.play(Create(circle))'''

		code = self._code_block(code_text, font_size=20).scale(0.9)

		result_circle = Circle(radius=1, color=BLUE)
		result_label = Text("Output", font_size=24, color=self.theme.text)

		left_group = VGroup(code).shift(LEFT * 3)
		right_group = VGroup(result_label, result_circle).arrange(DOWN, buff=0.3).shift(RIGHT * 3)

		self.play(FadeIn(header), run_time=0.5)
		self.play(FadeIn(left_group), run_time=0.7)
		self.next_slide()

		self.play(FadeIn(result_label), run_time=0.3)
		self.play(Create(result_circle), run_time=1.0)
		self.next_slide()

	def _boring_vs_animated(self):
		"""Contrast a static bullet point vs an animated reveal."""
		self.update_canvas()

		header = Text("Static vs Animated", font_size=48, color=self.theme.accent).to_edge(UP)

		boring_title = Text("The classic way", font_size=28, color=self.theme.text)
		boring_bullets = VGroup(
			Text("• Point A", font_size=24, color=self.theme.text),
			Text("• Point B", font_size=24, color=self.theme.text),
			Text("• Point C", font_size=24, color=self.theme.text),
		).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
		boring_group = VGroup(boring_title, boring_bullets).arrange(DOWN, buff=0.4).shift(LEFT * 3.5)

		animated_title = Text("The Manim way", font_size=28, color=self.theme.accent)
		shape_a = Circle(radius=0.4, color=BLUE, fill_opacity=0.5)
		shape_b = Square(side_length=0.8, color=GREEN, fill_opacity=0.5)
		shape_c = Triangle(fill_opacity=0.5, color=RED).scale(0.5)
		shapes = VGroup(shape_a, shape_b, shape_c).arrange(DOWN, buff=0.3)
		animated_group = VGroup(animated_title, shapes).arrange(DOWN, buff=0.4).shift(RIGHT * 3.5)

		divider = DashedLine(UP * 2, DOWN * 2, color=self.theme.text, dash_length=0.1).set_opacity(0.3)

		self.play(FadeIn(header), run_time=0.5)
		self.play(FadeIn(boring_group), run_time=0.3)
		self.next_slide()

		self.play(FadeIn(divider), FadeIn(animated_title), run_time=0.4)
		self.play(GrowFromCenter(shape_a), run_time=0.5)
		self.play(SpinInFromNothing(shape_b), run_time=0.5)
		self.play(DrawBorderThenFill(shape_c), run_time=0.5)
		self.next_slide()

	def _thinking_in_manim(self):
		"""Explain the 3 core concepts: Mobjects, Animations, Scenes."""
		self.update_canvas()
		header = Text("Core Concept 1: Mobjects", font_size=48, color=self.theme.accent).to_edge(UP)
		sub = Text(
			"Everything on screen is a Mobject (Mathematical Object)",
			font_size=28,
			color=self.theme.text,
		).next_to(header, DOWN, buff=0.4)

		circ = Circle(radius=0.5, color=BLUE)
		sq = Square(side_length=0.8, color=GREEN)
		txt = Text("Hello", font_size=36, color=YELLOW)
		arrow = Arrow(LEFT, RIGHT, color=RED)
		tex = MathTex(r"E = mc^2", font_size=48)
		num_line = NumberLine(x_range=[-2, 2], length=3, include_numbers=True, font_size=20)

		examples = VGroup(circ, sq, txt, arrow, tex, num_line).arrange_in_grid(
			rows=2, cols=3, buff=0.8
		).shift(DOWN * 0.5)
		labels = VGroup(
			Text("Circle", font_size=18, color=self.theme.text).next_to(circ, DOWN, buff=0.15),
			Text("Square", font_size=18, color=self.theme.text).next_to(sq, DOWN, buff=0.15),
			Text("Text", font_size=18, color=self.theme.text).next_to(txt, DOWN, buff=0.15),
			Text("Arrow", font_size=18, color=self.theme.text).next_to(arrow, DOWN, buff=0.15),
			Text("MathTex", font_size=18, color=self.theme.text).next_to(tex, DOWN, buff=0.15),
			Text("NumberLine", font_size=18, color=self.theme.text).next_to(num_line, DOWN, buff=0.15),
		)

		self.play(FadeIn(header), FadeIn(sub), run_time=0.6)
		self.play(
			LaggedStart(*[GrowFromCenter(m) for m in examples], lag_ratio=0.15),
			LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.15),
			run_time=1.5,
		)
		self.next_slide()

		self.update_canvas()
		header2 = Text("Core Concept 2: Animations", font_size=48, color=self.theme.accent).to_edge(UP)
		sub2 = Text("Animations transform Mobjects over time", font_size=28, color=self.theme.text).next_to(
			header2, DOWN, buff=0.4
		)

		demo_shape = Square(side_length=1.5, color=BLUE, fill_opacity=0.5).shift(DOWN * 0.5)
		anim_label = Text("self.play( ... )", font_size=28, color=self.theme.accent).next_to(
			demo_shape, UP, buff=0.8
		)

		self.play(FadeIn(header2), FadeIn(sub2), run_time=0.5)
		self.play(FadeIn(anim_label), Create(demo_shape), run_time=0.7)
		self.next_slide()

		# Animation demonstrations with side-by-side code
		anim_demos = [
			{
				"name": "Rotate",
				"code": "self.play(\n  Rotate(shape,\n    angle=PI/2),\n  run_time=0.7\n)",
				"animation": lambda: Rotate(demo_shape, angle=PI / 2),
			},
			{
				"name": "Transform",
				"code": "new_shape = Circle(\n  radius=0.75,\n  color=GREEN\n)\nself.play(\n  Transform(shape,\n    new_shape)\n)",
				"needs_update": True,
			},
			{
				"name": "Scale",
				"code": "self.play(\n  shape.animate.scale(1.5),\n  run_time=0.7\n)",
				"animation": lambda: demo_shape.animate.scale(1.5),
			},
			{
				"name": "FadeOut + FadeIn",
				"code": "self.play(FadeOut(shape))\nnew_shape = Star(n=5)\nself.play(FadeIn(new_shape))",
				"needs_replace": True,
			},
		]
  
		# fade out the header2 and sub2 to make room for the code blocks
		self.play(FadeOut(header2), FadeOut(sub2), FadeOut(anim_label), run_time=0.5)

		for i, demo in enumerate(anim_demos):
			# Create code block for this animation
			code_block = self._code_block(demo["code"], font_size=18).scale(0.85)
			code_block.to_edge(LEFT, buff=0.5)
			
			# Create title + label
			name_text = Text(demo["name"], font_size=24, color=self.theme.accent).to_edge(UP, buff=1)

			# Show code and title
			self.play(FadeIn(name_text), FadeIn(code_block), run_time=0.5)
			self.next_slide()

			# Run the animation
			if i == 0:
				# Rotate
				self.play(Rotate(demo_shape, angle=PI / 2), run_time=0.7)
			elif i == 1:
				# Transform to circle
				new_shape = Circle(radius=0.75, color=GREEN, fill_opacity=0.5).shift(DOWN * 0.5)
				self.play(Transform(demo_shape, new_shape), run_time=0.7)
			elif i == 2:
				# Scale
				self.play(demo_shape.animate.scale(1.5), run_time=0.7)
			elif i == 3:
				# FadeOut and replace with star
				self.play(FadeOut(demo_shape), run_time=0.4)
				demo_shape2 = Star(n=5, fill_opacity=0.5, color=YELLOW).shift(DOWN * 0.5)
				self.play(FadeIn(demo_shape2), run_time=0.4)
				demo_shape = demo_shape2

			self.next_slide()
			self.play(FadeOut(name_text), FadeOut(code_block), run_time=0.3)

		self.update_canvas()
		header3 = Text("Core Concept 3: Scenes", font_size=48, color=self.theme.accent).to_edge(UP)
		sub3 = Text(
			"A Scene is a canvas that holds and animates Mobjects",
			font_size=28,
			color=self.theme.text,
		).next_to(header3, DOWN, buff=0.4)

		frame = Rectangle(width=8, height=4, color=self.theme.text, stroke_width=1).shift(DOWN * 0.5)
		frame_label = Text("Scene / construct(self)", font_size=20, color=self.theme.accent).next_to(
			frame, UP, buff=0.15
		)

		inner_shapes = VGroup(
			Circle(radius=0.3, color=BLUE, fill_opacity=0.5).shift(LEFT * 2 + DOWN * 0.5),
			Square(side_length=0.5, color=GREEN, fill_opacity=0.5).shift(DOWN * 0.5),
			Triangle(fill_opacity=0.5, color=RED).scale(0.3).shift(RIGHT * 2 + DOWN * 0.5),
		)

		timeline = Arrow(LEFT * 3, RIGHT * 3, color=self.theme.accent, stroke_width=2).shift(DOWN * 2.5)
		time_label = Text("self.play() calls → time", font_size=20, color=self.theme.text).next_to(
			timeline, DOWN, buff=0.1
		)

		self.play(FadeIn(header3), FadeIn(sub3), run_time=0.5)
		self.play(Create(frame), FadeIn(frame_label), run_time=0.5)
		self.play(LaggedStart(*[GrowFromCenter(s) for s in inner_shapes], lag_ratio=0.2), run_time=0.8)
		self.play(GrowArrow(timeline), FadeIn(time_label), run_time=0.6)
		self.next_slide()

		self.update_canvas()
		header4 = Text("Positioning of Objects", font_size=48, color=self.theme.accent).to_edge(UP)

		demo_sq = Square(side_length=0.6, color=BLUE, fill_opacity=0.5)
		methods = [
			(".move_to(ORIGIN)", ORIGIN),
			(".to_edge(UP)", UP * 2.2),
			(".to_corner(UR)", UR * 2.2 + RIGHT * 1.5),
			(".shift(LEFT * 2)", LEFT * 2 + DOWN * 0.5),
		]

		self.play(FadeIn(header4), run_time=0.4)
		for method_str, pos in methods:
			label = Text(method_str, font_size=22, color=self.theme.accent)
			target = demo_sq.copy().move_to(pos)
			label.next_to(target, DOWN, buff=0.15)
			self.play(demo_sq.animate.move_to(pos), FadeIn(label), run_time=0.5)
			self.next_slide()
			self.play(FadeOut(label), run_time=0.2)
		
		# Special slide for .next_to() with an anchor object
		self.update_canvas()
		header_next_to = Text("Positioning relative to objects", font_size=42, color=self.theme.accent).to_edge(UP)
		code_next_to = self._code_block(
			'''anchor = Circle(radius=0.3)
anchor.move_to(ORIGIN)

obj = Square(side_length=0.5)
obj.next_to(anchor, RIGHT, buff=0.3)''', font_size=20
		).scale(0.9).to_edge(LEFT, buff=0.5)
		
		self.play(FadeIn(header_next_to), FadeIn(code_next_to), run_time=0.5)
		self.next_slide()
		
		# Show the anchor and object
		anchor = Circle(radius=0.3, color=GREEN, fill_opacity=0.5)
		anchor.move_to(ORIGIN)
		obj_sq = Square(side_length=0.5, color=RED, fill_opacity=0.5)
		obj_sq.next_to(anchor, RIGHT, buff=0.3)
		
		anchor_label = Text("anchor", font_size=16, color=self.theme.text).next_to(anchor, DOWN, buff=0.2)
		obj_label = Text("obj", font_size=16, color=self.theme.text).next_to(obj_sq, DOWN, buff=0.2)
		
		self.play(Create(anchor), FadeIn(anchor_label), run_time=0.5)
		self.play(Create(obj_sq), FadeIn(obj_label), run_time=0.5)
		self.next_slide()
		
		# Show different directions
		directions = [
			(LEFT, "LEFT"),
			(RIGHT, "RIGHT"),
			(UP, "UP"),
			(DOWN, "DOWN"),
		]
		
		for direction, dir_name in directions:
			dir_text = Text(f".next_to(anchor, {dir_name})", font_size=18, color=self.theme.accent)
			new_pos = anchor.copy()
			new_pos_obj = obj_sq.copy()
			new_pos_obj.next_to(new_pos, direction, buff=0.3)
			
			self.play(obj_sq.animate.next_to(anchor, direction, buff=0.3), run_time=0.5)
			self.play(FadeIn(dir_text.to_edge(DOWN, buff=0.5)), run_time=0.3)
			self.next_slide()
			self.play(FadeOut(dir_text), run_time=0.2)
		
		self.play(FadeOut(anchor), FadeOut(anchor_label), FadeOut(obj_sq), FadeOut(obj_label), FadeOut(code_next_to), FadeOut(header_next_to), run_time=0.5)
		self.next_slide()

	def _first_animation_demo(self):
		"""Walk through building a first useful animation: a pipeline diagram step by step."""
		labels_list = ["Data", "Model", "Train"]
		colors_list = [BLUE, GREEN, YELLOW]
		DEMO_X = RIGHT * 3.5  # center of the right panel for demos

		# ── Intro ──
		self.update_canvas()
		header = Text("Let us build something cool", font_size=48, color=self.theme.accent).to_edge(UP)
		sub = Text("A simple pipeline diagram", font_size=28, color=self.theme.text).next_to(
			header, DOWN, buff=0.3
		)
		self.play(FadeIn(header), FadeIn(sub), run_time=0.5)
		self.next_slide()

		# ── Complete animation first (centered, full screen) ──
		self.update_canvas()
		complete_header = Text("The finished result", font_size=42, color=self.theme.accent).to_edge(UP)

		full_boxes = VGroup()
		for lbl, col in zip(labels_list, colors_list):
			b = RoundedRectangle(
				width=1.8, height=1.0, corner_radius=0.15,
				fill_color=col, fill_opacity=0.2, stroke_color=col
			)
			t = Text(lbl, font_size=20, color=self.theme.text)
			full_boxes.add(VGroup(b, t))
		full_boxes.arrange(RIGHT, buff=1.2)

		full_arrows = VGroup()
		for i in range(len(full_boxes) - 1):
			arr = Arrow(
				full_boxes[i][0].get_right(),
				full_boxes[i + 1][0].get_left(),
				color=self.theme.text, buff=0.1, stroke_width=2
			)
			full_arrows.add(arr)
		VGroup(full_boxes, full_arrows).move_to(ORIGIN + DOWN * 0.3)

		self.play(FadeIn(complete_header), run_time=0.4)
		self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in full_boxes], lag_ratio=0.2), run_time=1.0)
		self.play(LaggedStart(*[GrowArrow(a) for a in full_arrows], lag_ratio=0.2), run_time=0.8)
		self.next_slide()

		for box in full_boxes:
			self.play(
				box.animate.scale(1.3),
				box[0].animate.set_fill(opacity=0.6),
				box[0].animate.set_stroke(width=3),
				run_time=0.3,
			)
			self.play(
				box.animate.scale(1.0 / 1.3),
				box[0].animate.set_fill(opacity=0.2),
				box[0].animate.set_stroke(width=1),
				run_time=0.3,
			)
		self.next_slide()

		# ── Step-by-step breakdown ──
		# Helper to build a code block positioned in the left panel
		def _left_code(code_text, fs=18):
			return self._code_block(code_text, font_size=fs).scale(0.85).move_to(LEFT * 3.5)

		# Step 1: Initialize
		self.update_canvas()
		step1 = Text("Step 1: Initialize", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code1 = _left_code("boxes = VGroup()", fs=22)
		self.play(FadeIn(step1), FadeIn(code1), run_time=0.5)
		self.next_slide()

		# Step 2: Create a box
		self.update_canvas()
		step2 = Text("Step 2: Create a box", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code2 = _left_code(
			'''box = RoundedRectangle(
  width=1.8, height=1.0,
  corner_radius=0.15,
  fill_color=BLUE,
  fill_opacity=0.2
)'''
		)
		box_demo = RoundedRectangle(
			width=1.8, height=1.0, corner_radius=0.15,
			fill_color=BLUE, fill_opacity=0.2, stroke_color=BLUE
		).move_to(DEMO_X)

		self.play(FadeIn(step2), FadeIn(code2), run_time=0.5)
		self.play(Create(box_demo), run_time=0.7)
		self.next_slide()

		# Step 3: Add text
		self.update_canvas()
		step3 = Text("Step 3: Add text", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code3 = _left_code(
			'''txt = Text("Data", font_size=22)
box_group = VGroup(box, txt)'''
		)
		box_demo3 = RoundedRectangle(
			width=1.8, height=1.0, corner_radius=0.15,
			fill_color=BLUE, fill_opacity=0.2, stroke_color=BLUE
		)
		txt_demo = Text("Data", font_size=22, color=self.theme.text)
		VGroup(box_demo3, txt_demo).move_to(DEMO_X)

		self.play(FadeIn(step3), FadeIn(code3), Create(box_demo3), run_time=0.5)
		self.play(FadeIn(txt_demo), run_time=0.5)
		self.next_slide()

		# Steps 4-7 share a canvas — demo builds progressively on the right

		# Step 4: Create multiple boxes
		self.update_canvas()
		step4 = Text("Step 4: Multiple boxes", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code4 = _left_code(
			'''labels = ["Data", "Model", "Train"]
colors = [BLUE, GREEN, YELLOW]

for lbl, col in zip(labels, colors):
  box = RoundedRectangle(...)
  txt = Text(lbl, ...)
  boxes.add(VGroup(box, txt))''', fs=16
		)

		boxes_demo = VGroup()
		for lbl, col in zip(labels_list, colors_list):
			b = RoundedRectangle(
				width=1.2, height=0.75, corner_radius=0.15,
				fill_color=col, fill_opacity=0.2, stroke_color=col
			)
			t = Text(lbl, font_size=16, color=self.theme.text)
			boxes_demo.add(VGroup(b, t))
		boxes_demo.arrange(RIGHT, buff=0.2).move_to(DEMO_X)

		self.play(FadeIn(step4), FadeIn(code4), run_time=0.5)
		self.play(LaggedStart(*[FadeIn(b) for b in boxes_demo], lag_ratio=0.2), run_time=1.0)
		self.next_slide()

		# Step 5: Arrange with more spacing (no clear — keep the boxes)
		step5 = Text("Step 5: Arrange", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code5 = _left_code('''boxes.arrange(RIGHT, buff=1.0)''', fs=20)

		# Compute target positions with wider spacing
		boxes_target = VGroup()
		for lbl, col in zip(labels_list, colors_list):
			b = RoundedRectangle(
				width=1.2, height=0.75, corner_radius=0.15,
				fill_color=col, fill_opacity=0.2, stroke_color=col
			)
			t = Text(lbl, font_size=16, color=self.theme.text)
			boxes_target.add(VGroup(b, t))
		boxes_target.arrange(RIGHT, buff=0.5).move_to(DEMO_X)

		self.play(
			FadeOut(step4), FadeOut(code4),
			FadeIn(step5), FadeIn(code5),
			run_time=0.5,
		)
		self.play(
			*[boxes_demo[i].animate.move_to(boxes_target[i]) for i in range(len(boxes_demo))],
			run_time=0.7,
		)
		self.next_slide()

		# Step 6: Add arrows (no clear — keep the boxes)
		step6 = Text("Step 6: Add arrows", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code6 = _left_code(
			'''for i in range(len(boxes) - 1):
  arr = Arrow(
    boxes[i].get_right(),
    boxes[i+1].get_left(),
    color=WHITE
  )
  arrows.add(arr)''', fs=16
		)

		arrows_demo = VGroup()
		for i in range(len(boxes_demo) - 1):
			arr = Arrow(
				boxes_demo[i][0].get_right(),
				boxes_demo[i + 1][0].get_left(),
				color=self.theme.text, buff=0.1, stroke_width=2
			)
			arrows_demo.add(arr)

		self.play(
			FadeOut(step5), FadeOut(code5),
			FadeIn(step6), FadeIn(code6),
			run_time=0.5,
		)
		self.play(LaggedStart(*[GrowArrow(a) for a in arrows_demo], lag_ratio=0.2), run_time=0.8)
		self.next_slide()

		# Step 7: Animate highlights (no clear — keep boxes + arrows)
		step7 = Text("Step 7: Animate highlights", font_size=32, color=self.theme.accent).to_edge(UP, buff=0.8)
		code7 = _left_code(
			'''for box in boxes:
  self.play(
    box.animate.scale(1.3),
    box[0].animate.set_fill(
      opacity=0.6
    ),
    run_time=0.3
  )
  # then scale back...''', fs=16
		)

		self.play(
			FadeOut(step6), FadeOut(code6),
			FadeIn(step7), FadeIn(code7),
			run_time=0.5,
		)
		self.next_slide()

		for box in boxes_demo:
			self.play(
				box.animate.scale(1.3),
				box[0].animate.set_fill(opacity=0.6),
				box[0].animate.set_stroke(width=3),
				run_time=0.3,
			)
			self.play(
				box.animate.scale(1.0 / 1.3),
				box[0].animate.set_fill(opacity=0.2),
				box[0].animate.set_stroke(width=1),
				run_time=0.3,
			)
		self.next_slide()

		# ── Final: Complete code ──
		self.update_canvas()
		code_header = Text("Complete Code", font_size=42, color=self.theme.accent).to_edge(UP)
		code_text = '''boxes = VGroup()
for label, color in zip(labels, colors):
	box = RoundedRectangle(
		width=1.8, height=1.0,
		fill_color=color, fill_opacity=0.2
	)
	txt = Text(label, font_size=22)
	boxes.add(VGroup(box, txt))
boxes.arrange(RIGHT, buff=1.0)

# Animate with highlighting
for box in boxes:
	self.play(box.animate.scale(1.4), run_time=0.3)
	self.play(box.animate.scale(1/1.4), run_time=0.3)'''
		code_block = self._code_block(code_text, font_size=16, line_numbers=True).shift(DOWN * 0.3)

		self.play(FadeIn(code_header), FadeIn(code_block), run_time=0.7)
		self.next_slide()

	def _manim_slides_demo(self):
		"""Show how manim-slides works."""
		self.update_canvas()
		header = Text("How Manim Slides Works", font_size=48, color=self.theme.accent).to_edge(UP)

		code_text = '''from manim_slides import Slide

class MyPresentation(Slide):
	def construct(self):
		title = Text("Hello!")
		self.play(Write(title))

		self.next_slide()  # pause here

		self.play(FadeOut(title))
		new = Text("Next slide!")
		self.play(FadeIn(new))'''

		code_block = self._code_block(code_text, font_size=20).shift(DOWN * 0.3)

		self.play(FadeIn(header), run_time=0.4)
		self.play(FadeIn(code_block), run_time=0.6)
		self.next_slide()

		note = Text(
			"next_slide() creates a pause point\n→ advance with arrow keys or click",
			font_size=22,
			color=self.theme.accent,
		).next_to(code_block, DOWN, buff=0.4)

		self.play(FadeIn(note), run_time=0.6)
		self.next_slide()

		self.update_canvas()
		header2 = Text("Running & Exporting", font_size=48, color=self.theme.accent).to_edge(UP)

		commands = VGroup(
			self._command_block("Render", "manim render presentation.py MyPresentation"),
			self._command_block("Present live", "manim-slides MyPresentation"),
			self._command_block("Export to HTML", "manim-slides convert MyPresentation slides.html"),
			self._command_block("Export to PDF", "manim-slides convert MyPresentation slides.pdf"),
		).arrange(DOWN, buff=0.35).shift(DOWN * 0.3)

		self.play(FadeIn(header2), run_time=0.4)
		self.play(
			LaggedStart(*[FadeIn(c, shift=LEFT * 0.3) for c in commands], lag_ratio=0.2),
			run_time=1.2,
		)
		self.next_slide()

	def _command_block(self, label_text: str, command_text: str) -> VGroup:
		"""Create a styled terminal command block."""
		label = Text(label_text, font_size=20, color=self.theme.accent)
		cmd = Text(f"$ {command_text}", font_size=18, color=self.theme.text, font=self.theme.code_font)
		bg = RoundedRectangle(
			width=10,
			height=0.7,
			corner_radius=0.1,
			fill_color=self.theme.panel,
			fill_opacity=0.8,
			stroke_color=self.theme.accent,
			stroke_width=0.5,
		)
		cmd.move_to(bg).shift(RIGHT * 0.2)
		label.next_to(bg, LEFT, buff=0.3)
		return VGroup(label, bg, cmd)

	def _template_walkthrough(self):
		"""Walk through the custom template concept."""
		self.update_canvas()
		header = Text("My Template Setup", font_size=48, color=self.theme.accent).to_edge(UP)

		base_box = RoundedRectangle(width=3, height=0.8, corner_radius=0.1, color=BLUE, fill_opacity=0.15)
		base_label = Text("Slide (manim-slides)", font_size=20, color=self.theme.text).move_to(base_box)
		base = VGroup(base_box, base_label)

		template_box = RoundedRectangle(width=3.5, height=0.8, corner_radius=0.1, color=GREEN, fill_opacity=0.15)
		template_label = Text("TemplateSlide (yours)", font_size=20, color=self.theme.accent).move_to(
			template_box
		)
		template = VGroup(template_box, template_label)

		pres_box = RoundedRectangle(width=4, height=0.8, corner_radius=0.1, color=YELLOW, fill_opacity=0.15)
		pres_label = Text("YourPresentation", font_size=20, color=self.theme.text).move_to(pres_box)
		pres = VGroup(pres_box, pres_label)

		hierarchy = VGroup(base, template, pres).arrange(DOWN, buff=0.8).shift(LEFT * 2.5 + DOWN * 0.3)

		arr1 = Arrow(base_box.get_bottom(), template_box.get_top(), color=self.theme.text, buff=0.1)
		arr2 = Arrow(template_box.get_bottom(), pres_box.get_top(), color=self.theme.text, buff=0.1)

		features_title = Text("Built-in methods:", font_size=22, color=self.theme.accent).shift(
			RIGHT * 3 + UP * 1
		)
		features = VGroup(
			Text("• title_slide()", font_size=18, color=self.theme.text),
			Text("• section_slide()", font_size=18, color=self.theme.text),
			Text("• list_slide()", font_size=18, color=self.theme.text),
			Text("• statement_slide()", font_size=18, color=self.theme.text),
			Text("• text_slide()", font_size=18, color=self.theme.text),
			Text("• get_progress_mobject()", font_size=18, color=self.theme.text),
		).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(
			features_title, DOWN, buff=0.3, aligned_edge=LEFT
		)

		self.play(FadeIn(header), run_time=0.4)
		self.play(FadeIn(base), run_time=0.4)
		self.play(GrowArrow(arr1), FadeIn(template), run_time=0.5)
		self.play(GrowArrow(arr2), FadeIn(pres), run_time=0.5)
		self.next_slide()

		self.play(
			FadeIn(features_title),
			LaggedStart(*[FadeIn(f) for f in features], lag_ratio=0.1),
			run_time=0.8,
		)
		self.next_slide()

		self.update_canvas()
		header2 = Text("Progress Bar (built into template)", font_size=42, color=self.theme.accent).to_edge(UP)
		self.play(FadeIn(header2), run_time=0.4)

		prev_progress = None
		for i in range(1, len(self.section_titles)):
			progress = self.get_progress_mobject(i, add_label=True)
			if prev_progress is None:
				self.play(FadeIn(progress), run_time=0.5)
			else:
				self.play(FadeOut(prev_progress), FadeIn(progress), run_time=0.4)
			prev_progress = progress
			if i <= 3:
				self.next_slide()
		self.next_slide()



		self.statement_slide("I will share the full template\nand this presentation's source code.")
