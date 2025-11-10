from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, Rectangle, Line
from database.db_manager import DBManager

class ModalidadesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager()
        self.modalidade_widgets = {}

        with self.canvas.before:
            Color(0.941, 0.929, 0.91, 1)
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_bg, pos=self._update_bg)

        self.layout = BoxLayout(orientation='vertical', spacing=20, padding=40, size_hint=(0.8, None))
        self.layout.pos_hint = {'center_x': 0.5}
        self.layout.bind(minimum_height=self.layout.setter('height'))

        title = Label(text='Modalidades', font_size=24, color=(0.2, 0.2, 0.2, 1), size_hint=(1, None), height=40)
        self.layout.add_widget(title)

        self.modalidades_container = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, None))
        self.modalidades_container.bind(minimum_height=self.modalidades_container.setter('height'))
        self.layout.add_widget(self.modalidades_container)

        self.new_modalidade_input = TextInput(hint_text='Nova modalidade', multiline=False, size_hint=(1, None), height=40)
        self.layout.add_widget(self.new_modalidade_input)

        add_btn = Button(
            text='Adicionar',
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.455, 0.216, 0.231, 1),
            color=(1, 1, 1, 1)
        )
        add_btn.bind(on_press=self.adicionar_modalidade)
        self.layout.add_widget(add_btn)

        voltar_btn = Button(
            text='Voltar',
            size_hint=(1, None),
            height=40,
            background_normal='',
            background_color=(0.941, 0.929, 0.91, 1),
            color=(0.455, 0.216, 0.231, 1)
        )
        voltar_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin_home'))
        self.layout.add_widget(voltar_btn)

        with voltar_btn.canvas.after:
            Color(0.455, 0.216, 0.231, 1)
            self.borda_voltar = Line(rectangle=(voltar_btn.x, voltar_btn.y, voltar_btn.width, voltar_btn.height), width=2)

        def update_voltar_border(instance, value):
            self.borda_voltar.rectangle = (voltar_btn.x, voltar_btn.y, voltar_btn.width, voltar_btn.height)

        voltar_btn.bind(pos=update_voltar_border, size=update_voltar_border)

        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(self.layout)
        self.add_widget(scroll)

        self.carregar_modalidades()

    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    def carregar_modalidades(self):
        self.modalidades_container.clear_widgets()
        self.modalidade_widgets.clear()
        modalidades = self.db.get_modalidades()
        for mid, nome in modalidades:
            box = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40, spacing=10)
            nome_input = TextInput(text=nome, multiline=False, size_hint=(0.6, None), height=40)
            editar_btn = Button(text='Editar', size_hint=(0.2, None), height=40)
            excluir_btn = Button(text='Excluir', size_hint=(0.2, None), height=40)

            editar_btn.bind(on_press=lambda instance, m_id=mid, input=nome_input: self.editar_modalidade(m_id, input.text))
            excluir_btn.bind(on_press=lambda instance, m_id=mid: self.excluir_modalidade(m_id))

            box.add_widget(nome_input)
            box.add_widget(editar_btn)
            box.add_widget(excluir_btn)
            self.modalidades_container.add_widget(box)
            self.modalidade_widgets[mid] = box

    def adicionar_modalidade(self, instance):
        nome = self.new_modalidade_input.text.strip()
        if nome:
            self.db.add_modalidade(nome)
            self.new_modalidade_input.text = ''
            self.carregar_modalidades()

    def editar_modalidade(self, modalidade_id, novo_nome):
        if novo_nome:
            self.db.update_modalidade(modalidade_id, novo_nome)
            self.carregar_modalidades()

    def excluir_modalidade(self, modalidade_id):
        self.db.delete_modalidade(modalidade_id)
        self.carregar_modalidades()
