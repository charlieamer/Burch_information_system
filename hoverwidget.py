from kivy.uix.widget import Widget
from kivy.properties import BooleanProperty
from kivy.core.window import Window
from kivy.uix.label import Label

class HoverWidget(Widget):
	hover = BooleanProperty(False)
	def __init__(self, **args):
		super(HoverWidget, self).__init__()
		Window.bind(mouse_pos=self.on_mouse_move)
	def on_mouse_move(self, cls, touch):
		self.hover = self.collide_point(touch[0], touch[1])