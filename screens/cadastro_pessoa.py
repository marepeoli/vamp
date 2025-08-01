from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from database.db_manager import DBManager

class CadastroPessoaScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = DBManager()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=20)

        self.nome_input = TextInput(hint_text='Nome')
        self.idade_input = TextInput(hint_text='Idade')
        self.tipo_spinner = Spinner(text='Tipo de Cadastro', values=['Atleta', 'Treinador'])
        self.dados_tecnicos_input = TextInput(hint_text='Dados Técnicos')

        layout.add_widget(self.nome_input)
        layout.add_widget(self.idade_input)
        layout.add_widget(self.tipo_spinner)
        layout.add_widget(self.dados_tecnicos_input)

        # Simulação de modalidades com checkboxes
        self.modalidade_checkboxes = []
        modalidades = self.db.get_modalidades()
        for mid, nome in modalidades:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
            cb = CheckBox()
            box.add_widget(cb)
            box.add_widget(Label(text=str(nome)))
            layout.add_widget(box)
            self.modalidade_checkboxes.append((cb, mid))

        self.status_label = Label(text='')
        layout.add_widget(self.status_label)

        voltar_button = Button(text='Voltar')
        voltar_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'admin_home'))
        layout.add_widget(voltar_button)


        salvar_button = Button(text='Salvar')
        salvar_button.bind(on_press=self.salvar_pessoa)
        layout.add_widget(salvar_button)

        self.add_widget(layout)

    def salvar_pessoa(self, instance):
        nome = self.nome_input.text.strip()
        idade_text = self.idade_input.text.strip()
        tipo = self.tipo_spinner.text
        dados_tecnicos = self.dados_tecnicos_input.text.strip()
        modalidade_ids = [mid for cb, mid in self.modalidade_checkboxes if cb.active]

        if not nome:
            self.status_label.text = 'Nome é obrigatório.'
            return

        if tipo not in ['Atleta', 'Treinador']:
            self.status_label.text = 'Selecione o tipo de cadastro.'
            return

        if not modalidade_ids:
            self.status_label.text = 'Selecione ao menos uma modalidade.'
            return

        if tipo == 'Atleta':
            if not idade_text:
                self.status_label.text = 'Idade é obrigatória para atletas.'
                return
            try:
                idade = int(idade_text)
                if idade <= 0:
                    raise ValueError
            except ValueError:
                self.status_label.text = 'Idade inválida.'
                return

            self.db.cursor.execute(
                "INSERT INTO atleta (nome, idade, dados_tecnicos) VALUES (?, ?, ?)",
                (nome, idade, dados_tecnicos)
            )
            atleta_id = self.db.cursor.lastrowid
            self.db.add_modalidades_atleta(atleta_id, modalidade_ids)
            self.status_label.text = 'Atleta cadastrado com sucesso!'

        else:  # Treinador
            self.db.cursor.execute(
                "INSERT INTO treinador (nome) VALUES (?)",
                (nome,)
            )
            treinador_id = self.db.cursor.lastrowid
            self.db.add_modalidades_treinador(treinador_id, modalidade_ids)
            self.status_label.text = 'Treinador cadastrado com sucesso!'

        self.db.conn.commit()

        # Limpar os campos
        self.nome_input.text = ''
        self.idade_input.text = ''
        self.dados_tecnicos_input.text = ''
        self.tipo_spinner.text = 'Tipo de Cadastro'
        for cb, _ in self.modalidade_checkboxes:
            cb.active = False
