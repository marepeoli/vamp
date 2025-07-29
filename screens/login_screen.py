from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from database.db_manager import DBManager  # Importa o gerenciador de banco de dados

class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.username_input = TextInput(hint_text='Email')
        self.password_input = TextInput(hint_text='Senha', password=True)
        self.error_label = Label(text='', color=(1, 0, 0, 1))
        login_button = Button(text='Entrar')
        login_button.bind(on_press=self.verificar_login)

        layout.add_widget(self.username_input)
        layout.add_widget(self.password_input)
        layout.add_widget(login_button)
        layout.add_widget(self.error_label)

        self.add_widget(layout)

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
