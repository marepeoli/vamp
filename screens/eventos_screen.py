
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from database.db_manager import DBManager

class EventosScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager()

        with self.canvas.before:
            Color(0.941, 0.929, 0.91, 1)  # fundo bege
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40, size_hint=(0.9, None))
        layout.pos_hint = {'center_x': 0.5}
        layout.bind(minimum_height=layout.setter('height'))

        title = Label(text='Eventos do Mês', font_size=24, color=(0.2, 0.2, 0.2, 1), size_hint=(1, None), height=40)
        layout.add_widget(title)

        eventos = self.db.get_eventos() if hasattr(self.db, 'get_eventos') else []

        if eventos:
            for evento in eventos:
                box = BoxLayout(orientation='vertical', size_hint=(1, None), height=100, padding=10, spacing=5)
                box.add_widget(Label(text=f"Tipo: {evento[1]}", color=(0, 0, 0, 1), size_hint=(1, None), height=30))
                box.add_widget(Label(text=f"Valor: R$ {evento[2]:.2f}", color=(0, 0, 0, 1), size_hint=(1, None), height=30))
                box.add_widget(Label(text=f"Status: {evento[3]}", color=(0, 0, 0, 1), size_hint=(1, None), height=30))
                layout.add_widget(box)
        else:
            layout.add_widget(Label(text='Nenhum evento encontrado.', color=(0.5, 0, 0, 0.8), size_hint=(1, None), height=30))

        voltar_btn = Button(
            text='Voltar',
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.941, 0.929, 0.91, 1),
            color=(0.455, 0.216, 0.231, 1)
        )
        voltar_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin_home'))
        layout.add_widget(voltar_btn)

        with voltar_btn.canvas.after:
            Color(0.455, 0.216, 0.231, 1)
            self.borda_voltar = Line(rectangle=(voltar_btn.x, voltar_btn.y, voltar_btn.width, voltar_btn.height), width=2)

        def update_voltar_border(instance, value):
            self.borda_voltar.rectangle = (voltar_btn.x, voltar_btn.y, voltar_btn.width, voltar_btn.height)

        voltar_btn.bind(pos=update_voltar_border, size=update_voltar_border)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(layout)
        self.add_widget(scroll)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
