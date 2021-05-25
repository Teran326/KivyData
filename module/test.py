from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivymd.uix.button import MDFlatButton, MDFillRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import MDList, TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from module.database import *


class RasaContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class RasaDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super(RasaDialog, self).__init__(
            type="custom",
            content_cls=RasaContent(),
            title='Nová rasa',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        rasa = Rasa()
        rasa.nazev_rasy = self.content_cls.ids.rasa.text
        app.povolani.database.create_rasa(rasa)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PovolaniContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if id:
            povolani = vars(app.povolani.database.read_by_id(id))
        else:
            povolani = {"id": "", "nazev_povolani": "Název povolani", "popis_id": "popis", "rasa_id": "rasa"}

        self.ids.nazev_povolani.text = povolani['nazev_povolani']
        rasy = app.povolani.database.read_rasa()

        menu_items_rasy = [{"viewclass": "OneLineListItem", "text": f"{rasa.nazev_rasy}",
                               "on_release": lambda x=f"{rasa.nazev_rasy}": self.set_item(x)} for rasa in rasy]
        self.menu_rasy = MDDropdownMenu(
            caller=self.ids.rasa_item,
            items=menu_items_rasy,
            position="center",
            width_mult=5,
        )
        self.ids.rasa_item.set_item(povolani['rasa_id'])
        self.ids.rasa_item.text = povolani['rasa_id']

        def set_item(self, text_item):
            self.ids.rasa_item.set_item(text_item)
            self.ids.rasa_item.text = text_item
            self.menu_rasy.dismiss()


class PovolaniDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super(PovolaniDialog, self).__init__(
            type="custom",
            content_cls=PovolaniContent(),
            title='Nové povolání',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        povolani = {'nazev_povolani': self.content_cls.ids.nazev_povolani.text, 'rasa_id': self.content_cls.ids.rasa_item.text}
        if self.id:
            povolani["id"] = self.id
            app.books.update(povolani)
        else:
            app.books.create(povolani)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class PopisContent(BoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)


class PopisDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super(PopisDialog, self).__init__(
            type="custom",
            content_cls=PopisContent(),
            title='Popis povolání',
            size_hint=(.8, 1),
            buttons=[
                MDFlatButton(text='Uložit', on_release=self.save_dialog),
                MDFlatButton(text='Zrušit', on_release=self.cancel_dialog)
            ]
        )

    def save_dialog(self, *args):
        popis = Popis()
        popis.full_name = self.content_cls.ids.popis.text
        app.test.database.create_popis(popis)
        self.dismiss()

    def cancel_dialog(self, *args):
        self.dismiss()


class MyItem(TwoLineAvatarIconListItem):
    # Konstruktoru se předává parametr item - datový objekt jedné osoby
    def __init__(self, item, *args, **kwargs):
        super(MyItem, self).__init__()
        # Předání informací o osobě do parametrů widgetu
        self.id = item['id']
        #self.text = item['povolani']
        self._no_ripple_effect = True

    def on_delete(self, *args):
        """
        Metoda je vyvolána po kliknutí na ikonu koše - vymazání záznamu
        """
        yes_button = MDFlatButton(text='Ano', on_release=self.yes_button_release)
        no_button = MDFlatButton(text='Ne', on_release=self.no_button_release)
        self.dialog_confirm = MDDialog(type="confirmation", title='Smazání záznamu',
                                       text="Chcete opravdu smazat tento záznam?", buttons=[yes_button, no_button])
        self.dialog_confirm.open()

    # Reakce na stisknutí tlačítka Ano
    def yes_button_release(self, *args):
        # Vyvolána metoda zajišťující vymazání záznamu podle předaného id
        app.povolani.delete(self.id)
        self.dialog_confirm.dismiss()

    # Reakce na stisknutí tlačítka Ne
    def no_button_release(self, *args):
        self.dialog_confirm.dismiss()


class Povolani(BoxLayout):
    # Metoda konstruktoru
    def __init__(self, *args, **kwargs):
        super(Povolani, self).__init__(orientation="vertical")
        # Globální proměnná - obsahuje kontext aplikace
        global app
        app = App.get_running_app()
        # Vytvoření rolovacího seznamu
        scrollview = ScrollView()
        self.list = MDList()
        # Volání metody, která vytvoří databázový objekt
        self.database = Database(dbtype='sqlite', dbname='data.db')
        # Volání metody, která načte a přepíše seznam osob na obrazovku
        self.rewrite_list()
        scrollview.add_widget(self.list)
        self.add_widget(scrollview)
        # Vytvoření nového boxu pro tlačítka Nová osoba a Nový stát
        button_box = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        # Přidání tlačítka pro vložení nové osoby
        new_povolani_btn = MDFillRoundFlatIconButton()
        new_povolani_btn.text = "Nové povolání"
        new_povolani_btn.icon = "plus"
        new_povolani_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_povolani_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_povolani_btn.md_bg_color = [0, 0.5, 0.8, 1]
        new_povolani_btn.font_style = "Button"
        new_povolani_btn.pos_hint = {"center_x": .5}
        new_povolani_btn.on_release = self.on_create_povolani
        button_box.add_widget(new_povolani_btn)
        # Přidání tlačítka pro vložení nového státu
        new_rasa_btn = MDFillRoundFlatIconButton()
        new_rasa_btn.text = "Nová rasa"
        new_rasa_btn.icon = "plus"
        new_rasa_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_rasa_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_rasa_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_rasa_btn.font_style = "Button"
        new_rasa_btn.pos_hint = {"center_x": .6}
        new_rasa_btn.on_release = self.on_create_rasa
        button_box.add_widget(new_rasa_btn)

        new_popis_btn = MDFillRoundFlatIconButton()
        new_popis_btn.text = "Nový popis"
        new_popis_btn.icon = "plus"
        new_popis_btn.icon_color = [0.9, 0.9, 0.9, 1]
        new_popis_btn.text_color = [0.9, 0.9, 0.9, 1]
        new_popis_btn.md_bg_color = [0.8, 0.5, 0, 1]
        new_popis_btn.font_style = "Button"
        new_popis_btn.pos_hint = {"center_x": .6}
        new_popis_btn.on_release = self.on_create_popis
        button_box.add_widget(new_popis_btn)
        self.add_widget(button_box)


    def rewrite_list(self):
        """
        Metoda přepíše seznam osob na obrazovce
        """
        # Odstraní všechny stávající widgety (typu MyItem) z listu
        self.list.clear_widgets()
        # Načte všechny osoby z databáze
        povolani2 = self.database.read_all()
        # Pro všechny osoby v seznamu persons vytváří widget MyItem
        for povolani in povolani2:
            print(vars(povolani))
            self.list.add_widget(MyItem(item=vars(povolani)))

    def on_create_povolani(self, *args):
        """
        Metoda reaguje na tlačítko Nová osoba a vyvolá dialogové okno PersonDialog
        """
        self.dialog = PovolaniDialog(id=None)
        self.dialog.open()

    def on_create_rasa(self, *args):
        """
        Metoda reaguje na tlačítko Nový stát a vyvolá dialogové okno StateDialog
        """
        self.dialog = RasaDialog()
        self.dialog.open()

    def on_create_popis(self, *args):
        """
        Metoda reaguje na tlačítko Nový stát a vyvolá dialogové okno StateDialog
        """
        self.dialog = PopisDialog()
        self.dialog.open()

    def create(self, povolani):
        """
        Metoda vytvoří nový záznam o osobě
        """
        create_povolani = Povolani()
        create_povolani.name = povolani['name']
        create_povolani.rasa = povolani['rasa']
        self.database.create(create_povolani)
        self.rewrite_list()

    def update(self, povolani):
        """
        Metoda aktualizuje záznam osoby
        """
        update_person = self.database.read_by_id(povolani['id'])
        update_person.name = povolani['name']
        update_person.state_short = povolani['rasa']
        self.database.update()
        self.rewrite_list()

    def delete(self, id):
        """
        Metoda smaže záznam o osobě - podle předaného id
        """
        self.database.delete(id)
        self.rewrite_list()
