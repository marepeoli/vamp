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
