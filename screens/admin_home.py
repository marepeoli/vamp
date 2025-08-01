from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class AdminHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        btn = Button(text='Cadastrar Atleta/Treinador')
        btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'cadastro_pessoa'))
        layout.add_widget(btn)

        layout.add_widget(Button(text='Gerenciar Modalidades'))
        layout.add_widget(Button(text='Criar Treino'))
        layout.add_widget(Button(text='Registrar Presença'))
        layout.add_widget(Button(text='Visualizar Eventos'))

        # Botão Voltar (volta para a tela de login, ou outra se preferir)
        voltar_button = Button(text='Voltar')
        voltar_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))  # ou outra tela
        layout.add_widget(voltar_button)

        logout_button = Button(text='Sair', background_color=(1, 0.2, 0.2, 1))
        logout_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'login'))
        layout.add_widget(logout_button)

        self.add_widget(layout)
