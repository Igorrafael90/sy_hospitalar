 from db.controllers.db_events_controller import *
from models.Hospital import Hospital
from models.Endereco import Endereco
from utils.system_events import *
from utils.filters import *
from utils.validator import *


def menu_insercao_hospital():
    quant_opcoes = 3
    qnt_linhas = 36
    valido = True
    while True:
        limpa_tela()

        imprime_titulo('INSERCAO HOSPITAL', qnt_linhas)
        print('1 - Inserir Hospital')
        print('2 - Adicionar hospital (Trabalho)')
        print('3 - Adicionar Medico (Auxilia)')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            insere_hospital()
        elif opcao == 2:
            associa_hospital_hospital()
        elif opcao == 3:
            associa_hospital_medico()
        elif opcao == 0:
            break
        else:
            valido = False


def insere_hospital():
    titulo = 'INSERIR HOSPITAL'

    while True:
        CNPJ = filter_cnpj(titulo)
        if not CNPJ:
            break

        NomeH = filter_nome(titulo)
        if not NomeH:
            break

        Rua = filter_rua(titulo)
        if not Rua:
            break

        Bairro = filter_bairro(titulo)
        if not Bairro:
            break

        Cidade = filter_cidade(titulo)
        if not Cidade:
            break

        CEP = filter_cep(titulo)
        if not CEP:
            break

        Telefone = filter_telefone(titulo)
        if not Telefone:
            break
        
        hospital = Hospital(CNPJ, NomeH, Rua, Bairro, Cidade, CEP,)

        if confirma_dados(titulo, hospital):
            comando = '''INSERT INTO hospital (CNPJ, NomeH, Rua, Bairro, Cidade, CEP) 
                        VALUES (:CNPJ, :NomeH, :Rua, :Bairro, :Cidade, :CEP);'''
            dados = {"CNPJ": hospital.cnpj,
                     "Nome": hospital.nome,
                     "Rua": hospital.endereco.rua,
                     "Bairro": hospital.endereco.bairro,
                     "Cidade": hospital.endereco.cidade,
                     "CEP": hospital.endereco.cep}

            hospital_inserida = altera_db(comando, dados)

            if hospital_inserida:
                mensagem_sucesso(titulo, 'hospital', 'Inserida')
                break
            else:
                mensagem_erro(titulo, 'hospital', 'Inserir')
                break


def confirma_dados(titulo: str, hospital: Hospital):
    tam_linha = 36

    valido = True
    while True:
        limpa_tela()

        imprime_titulo(titulo, tam_linha)
        print(f'CNPJ: {hospital.cnpj}')
        print(f'Nome: {hospital.nome}')
        print('Endereco:')
        print(f'         Rua: {hospital.endereco.rua}')
        print(f'         Bairro: {hospital.endereco.bairro}')
        print(f'         Cidade: {hospital.endereco.cidade}')
        print(f'         CEP: {hospital.endereco.cep}')
        imprime_linha(tam_linha)

        if not valido:
            mensagem_input_invalido('Opcao Inválida!', tam_linha)
            valido = True

        confirma = input('Os dados estão corretos? (s/n): ').upper()

        if confirma in ['S', 'N']:
            return True if confirma == 'S' else False
        else:
            valido = False


def associa_hospital_hospital():
    titulo = 'hospital X HOSPITAL'
    tam_linha = 36

    comando = '''SELECT CNPJ, nome FROM hospital'''
    hospitals = pega_info_db(comando)

    comando = '''SELECT cnpj, nome FROM Hospital'''
    hospitais = pega_info_db(comando)

    qnt_hospitals = len(hospitals)
    qnt_hospitais = len(hospitais)
    hospitais_associados = []

    if qnt_hospitals != 0 and qnt_hospitais != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual hospital?')
                imprime_linha(tam_linha)
                for i, hospital in enumerate(hospitals):
                    print(f'{i + 1} - {hospital[1]} ({hospital[0]})')
            else:
                if hospitais_associados == []:
                    comando = '''SELECT h.cnpj FROM Hospital h JOIN Hospital_x_hospital h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren'''
                    registro = pega_info_db(
                        comando, {'coren': coren_hospital})
                    if len(registro) != 0:
                        for hospital in registro:
                            hospitais_associados.append(hospital[0])

                if len(hospitais_associados) == qnt_hospitais:
                    mensagem = 'hospital Ja Cadastrada em Todos os Hospitais!'
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
                opcao = filter_opcao(qnt_hospitals)
            else:
                opcao = filter_opcao(qnt_hospitais)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_hospital = hospitals[opcao - 1][0]
                    alterna += 1
                else:
                    cnpj_hospital = hospitais[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Hospital_x_hospital (cnpj, coren) VALUES (:cnpj, :coren)'''
            associa = altera_db(
                comando, {'cnpj': cnpj_hospital, 'coren': coren_hospital})

            if associa:
                mensagem_sucesso(titulo, 'hospital', 'Associada')
            else:
                mensagem_erro(titulo, 'hospital', 'Associar')
    else:
        if qnt_hospitais == 0 and qnt_hospitals == 0:
            mensagem = 'Ainda não há hospitals e Hospitais Cadastrados!'
        elif qnt_hospitals == 0:
            mensagem = 'Ainda não há hospitals Cadastrados!'
        else:
            mensagem = 'Ainda não há Hospitais Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def associa_hospital_medico():
    titulo = 'hospital X MEDICO'
    tam_linha = 36

    comando = '''SELECT coren, nome FROM hospital'''
    hospitals = pega_info_db(comando)

    comando = '''SELECT crm, nome FROM Medico'''
    medicos = pega_info_db(comando)

    qnt_hospitals = len(hospitals)
    qnt_medicos = len(medicos)
    medicos_associados = []

    if qnt_hospitals != 0 and qnt_medicos != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual hospital?')
                imprime_linha(tam_linha)
                for i, hospital in enumerate(hospitals):
                    print(f'{i + 1} - {hospital[1]}')
            else:
                if medicos_associados == []:
                    comando = '''SELECT m.crm FROM Medico m JOIN Medico_x_hospital m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
                    registro = pega_info_db(
                        comando, {'coren': coren_hospital})
                    if len(registro) != 0:
                        for medico in registro:
                            medicos_associados.append(medico[0])
                if len(medicos_associados) == qnt_medicos:
                    mensagem = 'hospital Ja Associada a todos os Medicos!'
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
                opcao = filter_opcao(qnt_hospitals)
            else:
                opcao = filter_opcao(qnt_medicos)

            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_hospital = hospitals[opcao - 1][0]
                    alterna += 1
                else:
                    crm_medico = medicos[opcao - 1][0]
                    break

        if opcao != 0:
            comando = '''INSERT INTO Medico_x_hospital (crm, cnpj) VALUES (:crm, :cnpj)'''
            associa = altera_db(
                comando, {'crm': crm_medico, 'coren': coren_hospital})

            if associa:
                mensagem_sucesso(titulo, 'hospital', 'Associada')
            else:
                mensagem_erro(titulo, 'hospital', 'Associar')
    else:
        if qnt_medicos == 0 and qnt_hospitals == 0:
            mensagem = 'Ainda não há hospitals e Medicos Cadastrados!'
        elif qnt_hospitals == 0:
            mensagem = 'Ainda não há hospitals Cadastrados!'
        else:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def altera_hospital():
    titulo = 'ALTERA hospital'

    comando = '''SELECT * FROM hospital'''
    hospitals = pega_info_db(comando)

    qnt_hospitals = len(hospitals)

    if qnt_hospitals != 0:
        valido = True
        coren_hospital = ''
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, hospital in enumerate(hospitals):
                print(f'{i + 1} - {hospital[2]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_hospitals)

            if opcao == 0:
                break

            if opcao == -1:
                valido = False
            else:
                CNPJ_hospital = hospitals[opcao - 1][0]
                nome_hospital = hospitals[opcao - 1][1]
                rua_hospital = hospitals[opcao - 1][2]
                bairro_hospital = hospitals[opcao - 1][3]
                cidade_hospital = hospitals[opcao - 1][4]
                cep_hospital = hospitals[opcao - 1][5]
                break

        if opcao != 0:
            tipo_dado = ''
            dado = ''
            while True:  # obtem dado
                limpa_tela()

                imprime_titulo(titulo)
                print('Qual dado deseja alterar?')
                imprime_linha()
                print(f'1 - Nome ({nome_hospital})')
                print(f'2 - CNPJ ({CNPJ_hospital})')
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
                        tipo_dado = 'cnpj'
                        dado = filter_cnpj(titulo)
                        break
                    elif opcao == 3:
                        valido = True
                        while True:
                            limpa_tela()

                            imprime_titulo(titulo)
                            print('Qual dado do Endereco?')
                            imprime_linha()
                            print(f'1 - Rua ({rua_hospital})')
                            print(f'2 - Bairro ({bairro_hospital})')
                            print(f'3 - Cidade ({cidade_hospital})')
                            print(f'4 - CEP ({cep_hospital})')
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
                comando = '''UPDATE hospital SET {coluna} = :dado WHERE coren = :coren'''.format(
                    coluna=tipo_dado)
                dados = {'coren': coren_hospital, 'dado': dado}

                atualizado = altera_db(comando, dados)
                if atualizado:
                    mensagem_sucesso(titulo, 'hospital', 'Alterada')
                else:
                    mensagem_erro(titulo, 'hospital', 'Alterar')
    else:
        mensagem = 'Ainda não há hospitals Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def menu_relatorios_hospital():
    quant_opcoes = 3
    qnt_linhas = 46

    valido = True
    while True:
        limpa_tela()

        imprime_titulo('RELATORIOS hospital', qnt_linhas)
        print('1 - Listar hospitals')
        print('2 - Listar Hospitais que a hospital trabalha')
        print('3 - Listar Medicos que a hospital auxilia')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)

        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)

        opcao = filter_opcao(quant_opcoes)

        if opcao == 1:
            lista_hospitals()
        elif opcao == 2:
            lista_hospitais_hospital()
        elif opcao == 3:
            lista_medicos_hospital()
        elif opcao == 0:
            break
        else:
            valido = False


def lista_hospitals():
    titulo = 'LISTA DE hospitalS'
    qnt_linhas = 36

    comando = '''SELECT * FROM hospital'''
    hospital = pega_info_db(comando)

    if len(hospital) != 0:
        limpa_tela()
        imprime_titulo(titulo, qnt_linhas)
        for hospital in hospital:
            print(f'Nome: {hospital[1]}')
            print(f'CNPJ: {hospital[0]}')
            print('Endereco:')
            print(f'         Rua: {hospital[2]}')
            print(f'         Bairro: {hospital[3]}')
            print(f'         Cidade: {hospital[4]}')
            print(f'         CEP: {hospital[5]}')
            imprime_linha(qnt_linhas)
        pausa()
    else:
        mensagem = 'Ainda não ha hospital Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def lista_hospitais_hospital():
    titulo = 'hospital X HOSPITAIS'
    tam_linha = 37

    comando = '''SELECT coren, nome FROM hospital'''
    hospitals = pega_info_db(comando)

    if len(hospitals) != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, hospital in enumerate(hospitals):
                print(f'{i + 1} - {hospital[1]} ({hospital[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(len(hospitals))

            if opcao == -1:
                valido = False
            else:
                coren = hospitals[opcao - 1][0]
                break

        if opcao != 0:
            comando = '''SELECT h.cnpj, h.nome, h.telefone FROM Hospital h JOIN Hospital_x_hospital h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren;'''
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
                mensagem = 'Ainda não há Hospitais Cadastrados para esta hospital!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há hospitals Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def lista_medicos_hospital():
    titulo = 'MEDICOS AUXILIADOS'
    tam_linha = 37

    comando = '''SELECT coren, nome FROM hospital'''
    hospitals = pega_info_db(comando)

    qnt_hospitals = len(hospitals)

    if qnt_hospitals != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo, tam_linha)
            for i, hospital in enumerate(hospitals):
                print(f'{i + 1} - {hospital[1]} ({hospital[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_hospitals)

            if opcao == -1:
                valido = False
            else:
                coren = hospitals[opcao - 1][0]
                hospital = hospitals[opcao - 1]
                break

        if opcao != 0:
            comando = '''SELECT m.crm, m.nome FROM Medico m JOIN Medico_x_hospital m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
            medicos = pega_info_db(comando, {"coren": coren})

            if medicos != []:
                limpa_tela()

                imprime_titulo(titulo, tam_linha)
                print(f'Medicos auxiliados por {hospital[1]}:')
                imprime_linha(tam_linha)
                for medico in medicos:
                    print(f'-> {medico[1]} ({medico[0]})')
                imprime_linha(tam_linha)

                pausa()
            else:
                mensagem = 'Ainda não ha medicos auxiliados por esta hospital!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há hospitals Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def exclui_dependencias(coren: str):
    comando = '''DELETE FROM Hospital_x_hospital WHERE coren=:coren'''
    altera_db(comando, {'coren': coren})
    comando = '''DELETE FROM Medico_x_hospital WHERE coren=:coren'''
    altera_db(comando, {'coren': coren})


def exclui_hospital():
    titulo = 'EXCLUIR hospital'

    comando = '''SELECT coren, nome FROM hospital'''
    hospitals = pega_info_db(comando)

    qnt_hospitals = len(hospitals)

    if qnt_hospitals != 0:
        valido = True
        while True:
            limpa_tela()

            imprime_titulo(titulo)
            for i, hospital in enumerate(hospitals):
                print(f'{i + 1} - {hospital[1]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()

            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True

            opcao = filter_opcao(qnt_hospitals)

            if opcao == -1:
                valido = False
            else:
                coren_hospital = hospitals[opcao - 1][0]
                break

        if opcao != 0:

            exclui_dependencias(coren_hospital)

            comando = '''DELETE FROM hospital WHERE coren=:coren'''
            excluido = altera_db(comando, {'coren': coren_hospital})

            if excluido:
                mensagem_sucesso(titulo, 'hospital', 'Excluida')
            else:
                mensagem_erro(titulo, 'hospital', 'Excluir')
    else:
        mensagem = 'Ainda não há hospitals Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)
