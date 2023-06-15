from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen

kv = Builder.load_file("test.kv")


class MainScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        Window.size = [300, 600]
        # screens
        sm = ScreenManager()
        sm.add_widget(MainScreen(name="main_screen"))
        root = ScrollView(size_hint=(1, None), size=(
            Window.width, Window.height))
        for i in range(50):
            button = Button(text=str(i))
            MainScreen.add_widget(button)
        root.add_widget(MainScreen(name="main_screen"))
        return sm


if __name__ == '__main__':
    MainApp().run()
