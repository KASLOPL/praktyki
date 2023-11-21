from kivy.lang import Builder
from kivymd.app import MDApp
import main

# Main klasa
class Build(MDApp):

    def build(self):
        # Ustawienia aplikacji i zwracanie wyglądu z pliku kv
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"
        return Builder.load_file('lobby.kv')
    
    def press_PvP(self):
        Builder.unload_file('lobby.kv')
        main.Code().run()
    
Build().run()