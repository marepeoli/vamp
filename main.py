from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.admin_home import AdminHomeScreen
from screens.cadastro_pessoa import CadastroPessoaScreen
from screens.modalidades_screen import ModalidadesScreen
from screens.eventos_screen import EventosScreen
from kivy.core.window import Window
from kivy.uix.spinner import Spinner


# Define o ícone da janela
Window.set_icon("assets/vamp_logo.png")  # idealmente 32x32 ou 64x64
# Define o título da janela
Window.title = "VAMP Performance"

class VampClubApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminHomeScreen(name='admin_home'))
        sm.add_widget(CadastroPessoaScreen(name='cadastro_pessoa'))
        sm.add_widget(ModalidadesScreen(name='modalidades'))
        sm.add_widget(EventosScreen(name='eventos'))
        return sm

if __name__ == '__main__':
    VampClubApp().run()
