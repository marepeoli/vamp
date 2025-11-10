from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle
from database.db_manager import DBManager

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Cor de fundo bege clara da logo
        with self.canvas.before:
            Color(0.941, 0.929, 0.91, 1)  # #F0EDE8 
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.size_hint = (0.8, 0.8)
        layout.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

        # Logo
        logo = Image(source='assets/vamp_logo.png', size_hint=(1, 0.3))
        layout.add_widget(logo)

        # Campo de email
        self.username_input = TextInput(
            hint_text='Email',
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(self.username_input)

        # Campo de senha
        self.password_input = TextInput(
            hint_text='Senha',
            password=True,
            multiline=False,
            size_hint=(1, 0.1),
            background_color=(1, 1, 1, 1),
            foreground_color=(0.2, 0.2, 0.2, 1)
        )
        layout.add_widget(self.password_input)

        # Botão de login com bordô escuro (cor do contorno da logo)
        login_button = Button(
            text='ENTRAR',
            size_hint=(1, 0.15),
            background_normal='',  # ESSENCIAL para usar background_color direto
            background_color=(0.455, 0.216, 0.231, 1),  # #74373B
            color=(1, 1, 1, 1)  # texto branco
        )
        login_button.bind(on_press=self.verificar_login)
        layout.add_widget(login_button)

        # Mensagem de erro
        self.error_label = Label(
            text='',
            color=(1, 0, 0, 1),
            size_hint=(1, 0.1)
        )
        layout.add_widget(self.error_label)

        self.add_widget(layout)

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def verificar_login(self, instance):
        email = self.username_input.text.strip()
        senha = self.password_input.text.strip()

        if not email or not senha:
            self.error_label.text = 'Preencha todos os campos.'
            return

        db = DBManager()
        usuario = db.validate_login(email, senha)
        db.close()

        if usuario:
            self.manager.current = 'admin_home'
        else:
            self.error_label.text = 'Email ou senha incorretos.'
