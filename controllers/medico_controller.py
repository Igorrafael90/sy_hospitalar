from db.controllers.db_events_controller import *
from models.Medico import Medico
from models.Endereco import Endereco
from utils.system_events import *
from utils.filters import *
from utils.validator import *


def menu_insercao_Medico():
    quant_opcoes = 3
    qnt_linhas = 36
    valido = True
    while True:
        limpa_tela()

        imprime_titulo('INSERCAO MEDICO', qnt_linhas)
        print('1 - Inserir Medico')
        print('2 - Adicionar Hospital (Trabalho)')
        print('3 - Adicionar enfermeiro (Auxilia)')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            insere_Medico()
        elif opcao == 2:
            associa_Medico_hospital()
        elif opcao == 3:
            associa_Medico_medico()
        elif opcao == 0:
            break
        else:
            valido = False


def insere_Medico():
    titulo = 'INSERIR Medico'

    while True:
        nome = filter_nome(titulo)
        if not nome:
            break

        cpf = filter_cpf(titulo)
        if not cpf:
            break

        coren = filter_coren(titulo)
        if not coren:
            break

        endereco = filter_endereco(titulo)
        if not endereco:
            break

        Medico = Medico(coren, cpf, nome, endereco)

        if confirma_dados(titulo, Medico):
            comando = '''INSERT INTO Medico (coren, cpf, nome, rua, bairro, cidade, cep) 
                        VALUES (:coren, :cpf, :nome, :rua, :bairro, :cidade, :cep);'''
            dados = {"coren": Medico.coren,
                     "cpf": Medico.cpf,
                     "nome": Medico.nome,
                     "rua": Medico.endereco.rua,
                     "bairro": Medico.endereco.bairro,
                     "cidade": Medico.endereco.cidade,
                     "cep": Medico.endereco.cep}

            Medico_inserida = altera_db(comando, dados)

            if Medico_inserida:
                mensagem_sucesso(titulo, 'Medico', 'Inserida')
                break
            else:
                mensagem_erro(titulo, 'Medico', 'Inserir')
                break


def confirma_dados(titulo: str, Medico: Medico):
    tam_linha = 36

    valido = True
    while True:
        limpa_tela()

        imprime_titulo(titulo, tam_linha)
        print(f'Nome: {Medico.nome}')
        print(f'CPF: {Medico.cpf}')
        print(f'COREN: {Medico.crm}')
        print('Endereco:')
        print(f'         Rua: {Medico.endereco.rua}')
        print(f'         Bairro: {Medico.endereco.bairro}')
        print(f'         Cidade: {Medico.endereco.cidade}')
        print(f'         CEP: {Medico.endereco.cep}')
        imprime_linha(tam_linha)

        if not valido:
            mensagem_input_invalido('Opcao Inválida!', tam_linha)
            valido = True

        confirma = input('Os dados estão corretos? (s/n): ').upper()

        if confirma in ['S', 'N']:
            return True if confirma == 'S' else False
        else:
            valido = False


def associa_Medico_hospital():
    titulo = 'Medico X HOSPITAL'
    tam_linha = 36

    comando = '''SELECT coren, nome FROM Medico'''
    Medicos = pega_info_db(comando)

    comando = '''SELECT cnpj, nome FROM Hospital'''
    hospitais = pega_info_db(comando)

    qnt_Medicos = len(Medicos)
    qnt_hospitais = len(hospitais)
    hospitais_associados = []

    if qnt_Medicos != 0 and qnt_hospitais != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Medico?')
                imprime_linha(tam_linha)
                for i, Medico in enumerate(Medicos):
                    print(f'{i + 1} - {Medico[1]} ({Medico[0]})')
            else:
                if hospitais_associados == []:
                    comando = '''SELECT h.cnpj FROM Hospital h JOIN Hospital_x_Medico h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren'''
                    registro = pega_info_db(
                        comando, {'coren': coren_Medico})
                    if len(registro) != 0:
                        for hospital in registro:
                            hospitais_associados.append(hospital[0])

                if len(hospitais_associados) == qnt_hospitais:
                    mensagem = 'Medico Ja Cadastrada em Todos os Hospitais!'
                    mensagem_query_vazia(titulo, mensagem)
                    return None
                else:
                    print('Trabalha em qual Hospital?')
                    imprime_linha(tam_linha)
                    for i, hospital in enumerate(hospitais):

                        ja_cadastrado = False
                        if hospital[0] in hospitais_associados:
                            ja_cadastrado = True

                        if not ja_cadastrado:
                            print(f'{i + 1} - {hospital[1]} {hospital[0]}')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            if alterna == 0:
                opcao = filter_opcao(qnt_Medicos)
            else:
                opcao = filter_opcao(qnt_hospitais)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_Medico = Medicos[opcao - 1][0]
                    alterna += 1
                else:
                    cnpj_hospital = hospitais[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Hospital_x_Medico (cnpj, coren) VALUES (:cnpj, :coren)'''
            associa = altera_db(
                comando, {'cnpj': cnpj_hospital, 'coren': coren_Medico})

            if associa:
                mensagem_sucesso(titulo, 'Medico', 'Associada')
            else:
                mensagem_erro(titulo, 'Medico', 'Associar')
    else:
        if qnt_hospitais == 0 and qnt_Medicos == 0:
            mensagem = 'Ainda não há Medicos e Hospitais Cadastrados!'
        elif qnt_Medicos == 0:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        else:
            mensagem = 'Ainda não há Hospitais Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def associa_Medico_medico():
    titulo = 'Medico X MEDICO'
    tam_linha = 36

    comando = '''SELECT coren, nome FROM Medico'''
    Medicos = pega_info_db(comando)

    comando = '''SELECT crm, nome FROM Medico'''
    medicos = pega_info_db(comando)

    qnt_Medicos = len(Medicos)
    qnt_medicos = len(medicos)
    medicos_associados = []

    if qnt_Medicos != 0 and qnt_medicos != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Medico?')
                imprime_linha(tam_linha)
                for i, Medico in enumerate(Medicos):
                    print(f'{i + 1} - {Medico[1]}')
            else:
                if medicos_associados == []:
                    comando = '''SELECT m.crm FROM Medico m JOIN Medico_x_Medico m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
                    registro = pega_info_db(
                        comando, {'coren': coren_Medico})
                    if len(registro) != 0:
                        for medico in registro:
                            medicos_associados.append(medico[0])
                if len(medicos_associados) == qnt_medicos:
                    mensagem = 'Medico Ja Associada a todos os Medicos!'
                    mensagem_query_vazia(titulo, mensagem)
                    return None
                else:
                    print('Qual Medico?')
                    imprime_linha(tam_linha)
                    for i, medico in enumerate(medicos):
                        ja_cadastrado = False
                        if medico[0] in medicos_associados:
                            ja_cadastrado = True

                        if not ja_cadastrado:
                            print(f'{i + 1} - {medico[1]}')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            if alterna == 0:
                opcao = filter_opcao(qnt_Medicos)
            else:
                opcao = filter_opcao(qnt_medicos)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_Medico = Medicos[opcao - 1][0]
                    alterna += 1
                else:
                    crm_medico = medicos[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Medico_x_Medico (crm, coren) VALUES (:crm, :coren)'''
            associa = altera_db(
                comando, {'crm': crm_medico, 'coren': coren_Medico})

            if associa:
                mensagem_sucesso(titulo, 'Medico', 'Associada')
            else:
                mensagem_erro(titulo, 'Medico', 'Associar')
    else:
        if qnt_medicos == 0 and qnt_Medicos == 0:
            mensagem = 'Ainda não há Medicos e Medicos Cadastrados!'
        elif qnt_Medicos == 0:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        else:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def altera_Medico():
    titulo = 'ALTERA Medico'

    comando = '''SELECT * FROM Medico'''
    Medicos = pega_info_db(comando)

    qnt_Medicos = len(Medicos)

    if qnt_Medicos != 0:
        valido = True
        coren_Medico = ''
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, Medico in enumerate(Medicos):
                print(f'{i + 1} - {Medico[2]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Medicos)

            if opcao == 0:
                break

            if opcao == -1:
                valido = False
            else:
                coren_Medico = Medicos[opcao - 1][0]
                cpf_Medico = Medicos[opcao - 1][1]
                nome_Medico = Medicos[opcao - 1][2]
                rua_Medico = Medicos[opcao - 1][3]
                bairro_Medico = Medicos[opcao - 1][4]
                cidade_Medico = Medicos[opcao - 1][5]
                cep_Medico = Medicos[opcao - 1][6]
                break

        if opcao != 0:
            tipo_dado = ''
            dado = ''
            while True:  # obtem dado
                limpa_tela()

                imprime_titulo(titulo)
                print('Qual dado deseja alterar?')
                imprime_linha()
                print(f'1 - Nome ({nome_Medico})')
                print(f'2 - CPF ({cpf_Medico})')
                print('3 - Endereco')
                imprime_linha()
                print('0 - Voltar')
                imprime_linha()

                if not valido:
                    mensagem_input_invalido('Opcao Invalida!')
                    valido = True

                opcao = filter_opcao(3)

                if opcao == -1:
                    valido = False
                else:
                    if opcao == 1:
                        tipo_dado = 'nome'
                        dado = filter_nome(titulo)
                        break
                    elif opcao == 2:
                        tipo_dado = 'cpf'
                        dado = filter_cpf(titulo)
                        break
                    elif opcao == 3:
                        valido = True
                        while True:
                            limpa_tela()

                            imprime_titulo(titulo)
                            print('Qual dado do Endereco?')
                            imprime_linha()
                            print(f'1 - Rua ({rua_Medico})')
                            print(f'2 - Bairro ({bairro_Medico})')
                            print(f'3 - Cidade ({cidade_Medico})')
                            print(f'4 - CEP ({cep_Medico})')
                            imprime_linha()
                            print('0 - Voltar')
                            imprime_linha()

                            if not valido:
                                mensagem_input_invalido('Opcao Invalida!')
                                valido = True

                            opcao = filter_opcao(4)

                            if opcao == -1:
                                valido = False
                            else:
                                if opcao == 1:
                                    tipo_dado = 'rua'
                                    dado = filter_rua(titulo)
                                    break
                                elif opcao == 2:
                                    tipo_dado = 'bairro'
                                    dado = filter_bairro(titulo)
                                    break
                                elif opcao == 3:
                                    tipo_dado = 'cidade'
                                    dado = filter_cidade(titulo)
                                    break
                                elif opcao == 4:
                                    tipo_dado = 'cep'
                                    dado = filter_cep(titulo)
                                    break
                                elif opcao == 0:
                                    break
                                else:
                                    valido = False

                        break
                    elif opcao == 0:
                        break
                    else:
                        valido = False

            if dado != 0 and opcao != 0:
                comando = '''UPDATE Medico SET {coluna} = :dado WHERE coren = :coren'''.format(
                    coluna=tipo_dado)
                dados = {'coren': coren_Medico, 'dado': dado}

                atualizado = altera_db(comando, dados)
                if atualizado:
                    mensagem_sucesso(titulo, 'Medico', 'Alterada')
                else:
                    mensagem_erro(titulo, 'Medico', 'Alterar')
    else:
        mensagem = 'Ainda não há Medicos Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def menu_relatorios_Medico():
    quant_opcoes = 3
    qnt_linhas = 46

    valido = True
    while True:
        limpa_tela()

        imprime_titulo('RELATORIOS Medico', qnt_linhas)
        print('1 - Listar Medicos')
        print('2 - Listar Hospitais que a Medico trabalha')
        print('3 - Listar Medicos que a Medico auxilia')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            lista_Medicos()
        elif opcao == 2:
            lista_hospitais_Medico()
        elif opcao == 3:
            lista_medicos_Medico()
        elif opcao == 0:
            break
        else:
            valido = False


def lista_Medicos():
    titulo = 'LISTA DE MedicoS'
    qnt_linhas = 36

    comando = '''SELECT * FROM Medico'''
    Medico = pega_info_db(comando)

    if len(Medico) != 0:
        limpa_tela()
        imprime_titulo(titulo, qnt_linhas)
        for Medico in Medico:
            print(f'Nome: {Medico[2]}')
            print(f'CPF: {Medico[1]}')
            print(f'COREN: {Medico[0]}')
            print('Endereco:')
            print(f'         Rua: {Medico[3]}')
            print(f'         Bairro: {Medico[4]}')
            print(f'         Cidade: {Medico[5]}')
            print(f'         CEP: {Medico[6]}')
            imprime_linha(qnt_linhas)
        pausa()
    else:
        mensagem = 'Ainda não ha Medico Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def lista_hospitais_Medico():
    titulo = 'Medico X HOSPITAIS'
    tam_linha = 37

    comando = '''SELECT coren, nome FROM Medico'''
    Medicos = pega_info_db(comando)

    if len(Medicos) != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, Medico in enumerate(Medicos):
                print(f'{i + 1} - {Medico[1]} ({Medico[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(len(Medicos))

            if opcao == -1:
                valido = False
            else:
                coren = Medicos[opcao - 1][0]
                break

        if opcao != 0:
            comando = '''SELECT h.cnpj, h.nome, h.telefone FROM Hospital h JOIN Hospital_x_Medico h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren;'''
            hospitais = pega_info_db(comando, {"coren": coren})

            if hospitais != []:
                limpa_tela()
                imprime_titulo(titulo, tam_linha)
                for hospital in hospitais:
                    print(f'Hospital: {hospital[1]} ({hospital[0]})')
                    print(f'Telefone: {hospital[2]}')
                    imprime_linha(tam_linha)
                pausa()
            else:
                mensagem = 'Ainda não há Hospitais Cadastrados para esta Medico!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Medicos Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def lista_medicos_Medico():
    titulo = 'MEDICOS AUXILIADOS'
    tam_linha = 37

    comando = '''SELECT coren, nome FROM Medico'''
    Medicos = pega_info_db(comando)

    qnt_Medicos = len(Medicos)

    if qnt_Medicos != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, Medico in enumerate(Medicos):
                print(f'{i + 1} - {Medico[1]} ({Medico[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Medicos)

            if opcao == -1:
                valido = False
            else:
                coren = Medicos[opcao - 1][0]
                Medico = Medicos[opcao - 1]
                break

        if opcao != 0:
            comando = '''SELECT m.crm, m.nome FROM Medico m JOIN Medico_x_Medico m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
            medicos = pega_info_db(comando, {"coren": coren})

            if medicos != []:
                limpa_tela()

                imprime_titulo(titulo, tam_linha)
                print(f'Medicos auxiliados por {Medico[1]}:')
                imprime_linha(tam_linha)
                for medico in medicos:
                    print(f'-> {medico[1]} ({medico[0]})')
                imprime_linha(tam_linha)

                pausa()
            else:
                mensagem = 'Ainda não ha medicos auxiliados por esta Medico!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Medicos Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def exclui_dependencias(coren: str):
    comando = '''DELETE FROM Hospital_x_Medico WHERE coren=:coren'''
    altera_db(comando, {'coren': coren})
    comando = '''DELETE FROM Medico_x_Medico WHERE coren=:coren'''
    altera_db(comando, {'coren': coren})


def exclui_Medico():
    titulo = 'EXCLUIR Medico'

    comando = '''SELECT coren, nome FROM Medico'''
    Medicos = pega_info_db(comando)

    qnt_Medicos = len(Medicos)

    if qnt_Medicos != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, Medico in enumerate(Medicos):
                print(f'{i + 1} - {Medico[1]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Medicos)

            if opcao == -1:
                valido = False
            else:
                coren_Medico = Medicos[opcao - 1][0]
                break

        if opcao != 0:

            exclui_dependencias(coren_Medico)

            comando = '''DELETE FROM Medico WHERE coren=:coren'''
            excluido = altera_db(comando, {'coren': coren_Medico})

            if excluido:
                mensagem_sucesso(titulo, 'Medico', 'Excluida')
            else:
                mensagem_erro(titulo, 'Medico', 'Excluir')
    else:
        mensagem = 'Ainda não há Medicos Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)
