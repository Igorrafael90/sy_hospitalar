from db.controllers.db_events_controller import *
from models.Paciente import Paciente
from models.Endereco import Endereco
from utils.system_events import *
from utils.filters import *
from utils.validator import *


def menu_insercao_Paciente():
    quant_opcoes = 3
    qnt_linhas = 36
    valido = True
    while True:
        limpa_tela()

        imprime_titulo('INSERCAO PACIENTE', qnt_linhas)
        print('1 - Inserir Paciente')
        print('2 - Adicionar Hospital (Trabalho)')
        print('3 - Adicionar Medico (Auxilia)')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            insere_Paciente()
        elif opcao == 2:
            associa_Paciente_hospital()
        elif opcao == 3:
            associa_Paciente_medico()
        elif opcao == 0:
            break
        else:
            valido = False


def insere_Paciente():
    titulo = 'INSERIR Paciente'

    while True:
        nome = filter_nome(titulo)
        if not nome:
            break

        cpf = filter_cpf(titulo)
        if not cpf:
            break

        RG = filter_rg(titulo)
        if not RG:
            break

        endereco = filter_endereco(titulo)
        if not endereco:
            break

        Paciente = Paciente(RG, cpf, nome, endereco)

        if confirma_dados(titulo, Paciente):
            comando = '''INSERT INTO Paciente (RG, cpf, nome, rua, bairro, cidade, cep) 
                        VALUES (:RG, :cpf, :nome, :rua, :bairro, :cidade, :cep);'''
            dados = {"RG": Paciente.RG,
                     "cpf": Paciente.cpf,
                     "nome": Paciente.nome,
                     "rua": Paciente.endereco.rua,
                     "bairro": Paciente.endereco.bairro,
                     "cidade": Paciente.endereco.cidade,
                     "cep": Paciente.endereco.cep}

            Paciente_inserida = altera_db(comando, dados)

            if Paciente_inserida:
                mensagem_sucesso(titulo, 'Paciente', 'Inserida')
                break
            else:
                mensagem_erro(titulo, 'Paciente', 'Inserir')
                break


def confirma_dados(titulo: str, Paciente: Paciente):
    tam_linha = 36

    valido = True
    while True:
        limpa_tela()

        imprime_titulo(titulo, tam_linha)
        print(f'Nome: {Paciente.nome}')
        print(f'CPF: {Paciente.cpf}')
        print(f'RG: {Paciente.RG}')
        print('Endereco:')
        print(f'         Rua: {Paciente.endereco.rua}')
        print(f'         Bairro: {Paciente.endereco.bairro}')
        print(f'         Cidade: {Paciente.endereco.cidade}')
        print(f'         CEP: {Paciente.endereco.cep}')
        imprime_linha(tam_linha)

        if not valido:
            mensagem_input_invalido('Opcao Inválida!', tam_linha)
            valido = True

        confirma = input('Os dados estão corretos? (s/n): ').upper()

        if confirma in ['S', 'N']:
            return True if confirma == 'S' else False
        else:
            valido = False


def associa_Paciente_hospital():
    titulo = 'Paciente X HOSPITAL'
    tam_linha = 36

    comando = '''SELECT RG, nome FROM Paciente'''
    Pacientes = pega_info_db(comando)

    comando = '''SELECT cnpj, nome FROM Hospital'''
    hospitais = pega_info_db(comando)

    qnt_Pacientes = len(Pacientes)
    qnt_hospitais = len(hospitais)
    hospitais_associados = []

    if qnt_Pacientes != 0 and qnt_hospitais != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Paciente?')
                imprime_linha(tam_linha)
                for i, Paciente in enumerate(Pacientes):
                    print(f'{i + 1} - {Paciente[1]} ({Paciente[0]})')
            else:
                if hospitais_associados == []:
                    comando = '''SELECT h.cnpj FROM Hospital h JOIN Hospital_x_Paciente h_e ON h.cnpj = h_e.cnpj WHERE h_e.RG = :RG'''
                    registro = pega_info_db(
                        comando, {'RG': RG_Paciente})
                    if len(registro) != 0:
                        for hospital in registro:
                            hospitais_associados.append(hospital[0])

                if len(hospitais_associados) == qnt_hospitais:
                    mensagem = 'Paciente Ja Cadastrada em Todos os Hospitais!'
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
                opcao = filter_opcao(qnt_Pacientes)
            else:
                opcao = filter_opcao(qnt_hospitais)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    RG_Paciente = Pacientes[opcao - 1][0]
                    alterna += 1
                else:
                    cnpj_hospital = hospitais[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Hospital_x_Paciente (cnpj, RG) VALUES (:cnpj, :RG)'''
            associa = altera_db(
                comando, {'cnpj': cnpj_hospital, 'RG': RG_Paciente})

            if associa:
                mensagem_sucesso(titulo, 'Paciente', 'Associada')
            else:
                mensagem_erro(titulo, 'Paciente', 'Associar')
    else:
        if qnt_hospitais == 0 and qnt_Pacientes == 0:
            mensagem = 'Ainda não há Pacientes e Hospitais Cadastrados!'
        elif qnt_Pacientes == 0:
            mensagem = 'Ainda não há Pacientes Cadastrados!'
        else:
            mensagem = 'Ainda não há Hospitais Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def associa_Paciente_medico():
    titulo = 'Paciente X MEDICO'
    tam_linha = 36

    comando = '''SELECT RG, nome FROM Paciente'''
    Pacientes = pega_info_db(comando)

    comando = '''SELECT crm, nome FROM Medico'''
    medicos = pega_info_db(comando)

    qnt_Pacientes = len(Pacientes)
    qnt_medicos = len(medicos)
    medicos_associados = []

    if qnt_Pacientes != 0 and qnt_medicos != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Paciente?')
                imprime_linha(tam_linha)
                for i, Paciente in enumerate(Pacientes):
                    print(f'{i + 1} - {Paciente[1]}')
            else:
                if medicos_associados == []:
                    comando = '''SELECT m.crm FROM Medico m JOIN Medico_x_Paciente m_e ON m.crm = m_e.crm WHERE m_e.RG = :RG'''
                    registro = pega_info_db(
                        comando, {'RG': RG_Paciente})
                    if len(registro) != 0:
                        for medico in registro:
                            medicos_associados.append(medico[0])
                if len(medicos_associados) == qnt_medicos:
                    mensagem = 'Paciente Ja Associada a todos os Medicos!'
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
                opcao = filter_opcao(qnt_Pacientes)
            else:
                opcao = filter_opcao(qnt_medicos)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    RG_Paciente = Pacientes[opcao - 1][0]
                    alterna += 1
                else:
                    crm_medico = medicos[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Medico_x_Paciente (crm, RG) VALUES (:crm, :RG)'''
            associa = altera_db(
                comando, {'crm': crm_medico, 'RG': RG_Paciente})

            if associa:
                mensagem_sucesso(titulo, 'Paciente', 'Associada')
            else:
                mensagem_erro(titulo, 'Paciente', 'Associar')
    else:
        if qnt_medicos == 0 and qnt_Pacientes == 0:
            mensagem = 'Ainda não há Pacientes e Medicos Cadastrados!'
        elif qnt_Pacientes == 0:
            mensagem = 'Ainda não há Pacientes Cadastrados!'
        else:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def altera_Paciente():
    titulo = 'ALTERA Paciente'

    comando = '''SELECT * FROM Paciente'''
    Pacientes = pega_info_db(comando)

    qnt_Pacientes = len(Pacientes)

    if qnt_Pacientes != 0:
        valido = True
        RG_Paciente = ''
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, Paciente in enumerate(Pacientes):
                print(f'{i + 1} - {Paciente[2]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Pacientes)

            if opcao == 0:
                break

            if opcao == -1:
                valido = False
            else:
                RG_Paciente = Pacientes[opcao - 1][0]
                cpf_Paciente = Pacientes[opcao - 1][1]
                nome_Paciente = Pacientes[opcao - 1][2]
                rua_Paciente = Pacientes[opcao - 1][3]
                bairro_Paciente = Pacientes[opcao - 1][4]
                cidade_Paciente = Pacientes[opcao - 1][5]
                cep_Paciente = Pacientes[opcao - 1][6]
                break

        if opcao != 0:
            tipo_dado = ''
            dado = ''
            while True:  # obtem dado
                limpa_tela()

                imprime_titulo(titulo)
                print('Qual dado deseja alterar?')
                imprime_linha()
                print(f'1 - Nome ({nome_Paciente})')
                print(f'2 - CPF ({cpf_Paciente})')
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
                            print(f'1 - Rua ({rua_Paciente})')
                            print(f'2 - Bairro ({bairro_Paciente})')
                            print(f'3 - Cidade ({cidade_Paciente})')
                            print(f'4 - CEP ({cep_Paciente})')
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
                comando = '''UPDATE Paciente SET {coluna} = :dado WHERE RG = :RG'''.format(
                    coluna=tipo_dado)
                dados = {'RG': RG_Paciente, 'dado': dado}

                atualizado = altera_db(comando, dados)
                if atualizado:
                    mensagem_sucesso(titulo, 'Paciente', 'Alterada')
                else:
                    mensagem_erro(titulo, 'Paciente', 'Alterar')
    else:
        mensagem = 'Ainda não há Pacientes Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def menu_relatorios_Paciente():
    quant_opcoes = 3
    qnt_linhas = 46

    valido = True
    while True:
        limpa_tela()

        imprime_titulo('RELATORIOS Paciente', qnt_linhas)
        print('1 - Listar Pacientes')
        print('2 - Listar Hospitais que a Paciente trabalha')
        print('3 - Listar Medicos que a Paciente auxilia')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            lista_Pacientes()
        elif opcao == 2:
            lista_hospitais_Paciente()
        elif opcao == 3:
            lista_medicos_Paciente()
        elif opcao == 0:
            break
        else:
            valido = False


def lista_Pacientes():
    titulo = 'LISTA DE PacienteS'
    qnt_linhas = 36

    comando = '''SELECT * FROM Paciente'''
    Paciente = pega_info_db(comando)

    if len(Paciente) != 0:
        limpa_tela()
        imprime_titulo(titulo, qnt_linhas)
        for Paciente in Paciente:
            print(f'Nome: {Paciente[2]}')
            print(f'CPF: {Paciente[1]}')
            print(f'RG: {Paciente[0]}')
            print('Endereco:')
            print(f'         Rua: {Paciente[3]}')
            print(f'         Bairro: {Paciente[4]}')
            print(f'         Cidade: {Paciente[5]}')
            print(f'         CEP: {Paciente[6]}')
            imprime_linha(qnt_linhas)
        pausa()
    else:
        mensagem = 'Ainda não ha Paciente Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def lista_hospitais_Paciente():
    titulo = 'Paciente X HOSPITAIS'
    tam_linha = 37

    comando = '''SELECT RG, nome FROM Paciente'''
    Pacientes = pega_info_db(comando)

    if len(Pacientes) != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, Paciente in enumerate(Pacientes):
                print(f'{i + 1} - {Paciente[1]} ({Paciente[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(len(Pacientes))

            if opcao == -1:
                valido = False
            else:
                RG = Pacientes[opcao - 1][0]
                break

        if opcao != 0:
            comando = '''SELECT h.cnpj, h.nome, h.telefone FROM Hospital h JOIN Hospital_x_Paciente h_e ON h.cnpj = h_e.cnpj WHERE h_e.RG = :RG;'''
            hospitais = pega_info_db(comando, {"RG": RG})

            if hospitais != []:
                limpa_tela()
                imprime_titulo(titulo, tam_linha)
                for hospital in hospitais:
                    print(f'Hospital: {hospital[1]} ({hospital[0]})')
                    print(f'Telefone: {hospital[2]}')
                    imprime_linha(tam_linha)
                pausa()
            else:
                mensagem = 'Ainda não há Hospitais Cadastrados para esta Paciente!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Pacientes Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def lista_medicos_Paciente():
    titulo = 'MEDICOS AUXILIADOS'
    tam_linha = 37

    comando = '''SELECT RG, nome FROM Paciente'''
    Pacientes = pega_info_db(comando)

    qnt_Pacientes = len(Pacientes)

    if qnt_Pacientes != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, Paciente in enumerate(Pacientes):
                print(f'{i + 1} - {Paciente[1]} ({Paciente[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Pacientes)

            if opcao == -1:
                valido = False
            else:
                RG = Pacientes[opcao - 1][0]
                Paciente = Pacientes[opcao - 1]
                break

        if opcao != 0:
            comando = '''SELECT m.crm, m.nome FROM Medico m JOIN Medico_x_Paciente m_e ON m.crm = m_e.crm WHERE m_e.RG = :RG'''
            medicos = pega_info_db(comando, {"RG": RG})

            if medicos != []:
                limpa_tela()

                imprime_titulo(titulo, tam_linha)
                print(f'Medicos auxiliados por {Paciente[1]}:')
                imprime_linha(tam_linha)
                for medico in medicos:
                    print(f'-> {medico[1]} ({medico[0]})')
                imprime_linha(tam_linha)

                pausa()
            else:
                mensagem = 'Ainda não ha medicos auxiliados por esta Paciente!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Pacientes Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def exclui_dependencias(RG: str):
    comando = '''DELETE FROM Hospital_x_Paciente WHERE RG=:RG'''
    altera_db(comando, {'RG': RG})
    comando = '''DELETE FROM Medico_x_Paciente WHERE RG=:RG'''
    altera_db(comando, {'RG': RG})


def exclui_Paciente():
    titulo = 'EXCLUIR Paciente'

    comando = '''SELECT RG, nome FROM Paciente'''
    Pacientes = pega_info_db(comando)

    qnt_Pacientes = len(Pacientes)

    if qnt_Pacientes != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, Paciente in enumerate(Pacientes):
                print(f'{i + 1} - {Paciente[1]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_Pacientes)

            if opcao == -1:
                valido = False
            else:
                RG_Paciente = Pacientes[opcao - 1][0]
                break

        if opcao != 0:

            exclui_dependencias(RG_Paciente)

            comando = '''DELETE FROM Paciente WHERE RG=:RG'''
            excluido = altera_db(comando, {'RG': RG_Paciente})

            if excluido:
                mensagem_sucesso(titulo, 'Paciente', 'Excluida')
            else:
                mensagem_erro(titulo, 'Paciente', 'Excluir')
    else:
        mensagem = 'Ainda não há Pacientes Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)
