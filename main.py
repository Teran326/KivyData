from kivymd.app import MDApp
from kivy.lang import Builder
from module.test import Povolani

class Test(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        builder = Builder.load_file('main.kv')
        self.povolani = Povolani()
        builder.ids.navigation.ids.tab_manager.screens[0].add_widget(self.povolani)
        return builder


Test().run()
