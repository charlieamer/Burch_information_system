import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from login import LoginScreen, LoginProvider
from login import LoginScreen, LoginProvider
import login
from kivy.uix.widget import Widget
from kivy.core.window import Window
from hoverwidget import HoverWidget

class PongGame(Widget):
    pass
	
class BurchApp(App):
	screenmanager = None
	def build(self):
		"""
		root = ScreenManager()
		root.add_widget(LoginScreen())
		return root
		"""
		Window.clearcolor = (1,1,1,1)
		Builder.load_file("theme.kv")
		Builder.load_file("gui.kv")
		return LoginScreen()

BurchApp().run()