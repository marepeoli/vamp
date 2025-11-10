from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line

class AdminHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Fundo bege claro
        with self.canvas.before:
            Color(0.941, 0.929, 0.91, 1)  # #F0EDE8
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.size_hint = (0.8, 0.8)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Logo centralizada no topo
        logo = Image(source='assets/vamp_logo.png', size_hint=(1, 0.3))
        layout.add_widget(logo)

        # Título
        title = Label(text='Bem-vindo ao VAMP Performance', font_size=24, color=(0.2, 0.2, 0.2, 1), size_hint=(1, 0.2))
        layout.add_widget(title)

        # Botões de navegação
        botoes = [
            ('Cadastrar Pessoa', 'cadastro_pessoa'),
            ('Modalidades', 'modalidades'),
            ('Eventos', 'eventos'),
            ('Treinos', 'treinos')
        ]

        for texto, destino in botoes:
            btn = Button(
                text=texto,
                size_hint=(1, 0.15),
                background_normal='',
                background_color=(0.455, 0.216, 0.231, 1),  # #74373B
                color=(1, 1, 1, 1)  # texto branco
            )
            btn.bind(on_press=lambda instance, dest=destino: setattr(self.manager, 'current', dest))
            layout.add_widget(btn)

        # Botão Sair estilo negativo
        sair_btn = Button(
            text='Sair',
            size_hint=(1, 0.15),
            background_normal='',
            background_color=(0.941, 0.929, 0.91, 1),  # fundo bege
            color=(0.455, 0.216, 0.231, 1)  # texto bordô
        )
        sair_btn.bind(on_press=lambda instance: setattr(self.manager, 'current', 'login'))
        layout.add_widget(sair_btn)

        # Adiciona borda bordô ao botão "Sair"
        with sair_btn.canvas.after:
            Color(0.455, 0.216, 0.231, 1)  # bordô
            self.borda_sair = Line(rectangle=(sair_btn.x, sair_btn.y, sair_btn.width, sair_btn.height), width=2)

        def update_border(instance, value):
            self.borda_sair.rectangle = (sair_btn.x, sair_btn.y, sair_btn.width, sair_btn.height)

        sair_btn.bind(pos=update_border, size=update_border)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
