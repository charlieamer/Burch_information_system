import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from login import LoginScreen, LoginProvider
import login
from kivy.uix.widget import Widget
from kivy.core.window import Window
from hoverwidget import HoverWidget
from MainScreen import MainScreen
from common import MainScreenManager
    
class BurchApp(App):
    screenmanager = None
    def build(self):
        Window.clearcolor = (1,1,1,1)
        Builder.load_file("theme.kv")
        Builder.load_file("gui.kv")
        MainScreenManager.add_widget(LoginScreen())
        return MainScreenManager

BurchApp().run()