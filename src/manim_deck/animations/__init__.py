"""Reusable animation modules.

Each module is a class that takes a TemplateSlide instance and has a .run() method.
This lets you compose complex animation sequences and reuse them across talks.

Example
-------
>>> from manim_deck.animations.pipeline import PipelineModule
>>> class MyTalk(TemplateSlide):
...     def construct(self):
...         PipelineModule(self, steps=["Data", "Train", "Eval"]).run()
"""
