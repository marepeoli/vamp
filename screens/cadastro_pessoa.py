
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.image import Image
from kivy.graphics import Color, Rectangle, Line
from kivy.uix.scrollview import ScrollView

from database.db_manager import DBManager

class CadastroPessoaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager()

        with self.canvas.before:
            Color(0.941, 0.929, 0.91, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        layout = BoxLayout(orientation='vertical', spacing=20, padding=40)
        layout.size_hint = (0.8, None)
        layout.pos_hint = {'center_x': 0.5}
        layout.bind(minimum_height=layout.setter('height'))

        logo = Image(source='assets/vamp_logo.png', size_hint=(1, 0.4))
        layout.add_widget(logo)

        title = Label(text='Cadastro de Pessoa', font_size=24, color=(0.2, 0.2, 0.2, 1), size_hint=(1, None), height=40)
        layout.add_widget(title)

        self.nome_input = TextInput(hint_text='Nome', multiline=False, size_hint=(1, None), height=40)
        self.idade_input = TextInput(hint_text='Idade', multiline=False, size_hint=(1, None), height=40)
        self.tipo_spinner = Spinner(text='Tipo de Cadastro', values=['Atleta', 'Treinador'], size_hint=(1, None), height=40)
        self.dados_tecnicos_input = TextInput(hint_text='Dados Técnicos', multiline=False, size_hint=(1, None), height=40)

        layout.add_widget(self.nome_input)
        layout.add_widget(self.idade_input)
        layout.add_widget(self.tipo_spinner)
        layout.add_widget(self.dados_tecnicos_input)

        layout.add_widget(Label(text='Modalidades:', color=(0.2, 0.2, 0.2, 1), size_hint=(1, None), height=30))
        self.modalidade_checkboxes = []
        modalidades = self.db.get_modalidades()
        for mid, nome in modalidades:
            box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=30, spacing=10)
            cb = CheckBox(size_hint=(None, None), size=(30, 30))
            label = Label(text=nome, color=(0, 0, 0, 1), halign='left', valign='middle')
            label.bind(size=lambda instance, value: setattr(instance, 'text_size', value))
            box.add_widget(cb)
            box.add_widget(label)
            layout.add_widget(box)
            self.modalidade_checkboxes.append((cb, mid))

        self.status_label = Label(text='', color=(1, 0, 0, 1), size_hint=(1, None), height=30)
        layout.add_widget(self.status_label)

        salvar_btn = Button(
            text='Salvar',
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.455, 0.216, 0.231, 1),
            color=(1, 1, 1, 1)
        )
        salvar_btn.bind(on_press=self.salvar_pessoa)
        layout.add_widget(salvar_btn)

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

    def _update_voltar_border(self, *args):
        self.borda_voltar.rectangle = (
            self.children[0].children[0].x,
            self.children[0].children[0].y,
            self.children[0].children[0].width,
            self.children[0].children[0].height
        )

    def salvar_pessoa(self, instance):
        nome = self.nome_input.text.strip()
        idade = self.idade_input.text.strip()
        tipo = self.tipo_spinner.text
        dados_tecnicos = self.dados_tecnicos_input.text.strip()
        modalidades_selecionadas = [mid for cb, mid in self.modalidade_checkboxes if cb.active]

        if not nome or not idade or tipo == 'Tipo de Cadastro':
            self.status_label.text = "Preencha todos os campos obrigatórios."
            return

        try:
            idade_int = int(idade)
        except ValueError:
            self.status_label.text = "Idade deve ser um número."
            return

        try:
            if tipo == 'Atleta':
                if not modalidades_selecionadas:
                    self.status_label.text = "Selecione pelo menos uma modalidade."
                    return
                for modalidade_id in modalidades_selecionadas:
                    self.db.add_atleta(nome, idade_int, modalidade_id, dados_tecnicos)
                self.status_label.text = "Atleta cadastrado com sucesso!"
            elif tipo == 'Treinador':
                if not modalidades_selecionadas:
                    self.status_label.text = "Selecione pelo menos uma modalidade."
                    return
                for modalidade_id in modalidades_selecionadas:
                    self.db.add_treinador(nome, modalidade_id)
                self.status_label.text = "Treinador cadastrado com sucesso!"
            else:
                self.status_label.text = "Tipo de cadastro inválido."
        except Exception as e:
            self.status_label.text = f"Erro ao salvar: {str(e)}"
