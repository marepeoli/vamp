from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login_screen import LoginScreen
from screens.admin_home import AdminHomeScreen
from screens.cadastro_pessoa import CadastroPessoaScreen

class VampClubApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(AdminHomeScreen(name='admin_home'))
        sm.add_widget(CadastroPessoaScreen(name='cadastro_pessoa'))
        return sm

if __name__ == '__main__':
    VampClubApp().run()
