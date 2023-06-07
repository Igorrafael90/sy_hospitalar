from db.controllers.db_events_controller import *
from models import Endereco, Enfermeira
from utils.system_events import *
from utils.filters import *
from utils.validator import *

def menu_insercao_enfermeira():
    quant_opcoes = 3
    qnt_linhas = 36
    valido = True
    while True:
        limpa_tela()
        
        imprime_titulo('INSERCAO ENFERMEIRA', qnt_linhas)
        print('1 - Inserir Enfermeira')
        print('2 - Adicionar Hospital (Trabalho)')
        print('3 - Adicionar Medico (Auxilia)')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)
           
        opcao = filter_opcao(quant_opcoes)
            
        if opcao == 1:
            insere_enfermeira()
        elif opcao == 2:
            associa_enfermeira_hospital()
        elif opcao == 3:
            associa_enfermeira_medico()
        elif opcao == 0:
            break
        else:
            valido = False

def insere_enfermeira():
    titulo = 'INSERIR ENFERMEIRA'
    
    while True:
        nome = filter_nome(titulo)
        if not nome: break
        
        cpf = filter_cpf(titulo)
        if not cpf: break
        
        coren = filter_coren(titulo)
        if not coren: break
        
        endereco = filter_endereco(titulo)
        if not endereco: break
        
        enfermeira = Enfermeira(coren, cpf, nome, endereco)
        
        if confirma_dados(titulo, enfermeira):
            comando = '''INSERT INTO Enfermeira (coren, cpf, nome, rua, bairro, cidade, cep) 
                        VALUES (:coren, :cpf, :nome, :rua, :bairro, :cidade, :cep);'''
            dados = {"coren": enfermeira.coren,
                     "cpf": enfermeira.cpf,
                     "nome": enfermeira.nome,
                     "rua": enfermeira.endereco.rua,
                     "bairro": enfermeira.endereco.bairro,
                     "cidade": enfermeira.endereco.cidade,
                     "cep": enfermeira.endereco.cep}
            
            enfermeira_inserida = altera_db(comando, dados)
            
            if enfermeira_inserida:
                mensagem_sucesso(titulo, 'Enfermeira', 'Inserida')
                break
            else:
                mensagem_erro(titulo, 'Enfermeira', 'Inserir')
                break

def confirma_dados(titulo:str, enfermeira:Enfermeira):
    tam_linha = 36
    
    valido = True
    while True:
        limpa_tela()
        
        imprime_titulo(titulo, tam_linha)
        print(f'Nome: {enfermeira.nome}')
        print(f'CPF: {enfermeira.cpf}')
        print(f'COREN: {enfermeira.coren}')
        print('Endereco:')
        print(f'         Rua: {enfermeira.endereco.rua}')
        print(f'         Bairro: {enfermeira.endereco.bairro}')
        print(f'         Cidade: {enfermeira.endereco.cidade}')
        print(f'         CEP: {enfermeira.endereco.cep}')
        imprime_linha(tam_linha)
        
        if not valido:
            mensagem_input_invalido('Opcao Inválida!', tam_linha)
            valido = True
            
        confirma = input('Os dados estão corretos? (s/n): ').upper()
        
        if confirma in ['S', 'N']:
            return True if confirma == 'S' else False
        else:
            valido = False

def associa_enfermeira_hospital():
    titulo = 'ENFERMEIRA X HOSPITAL'
    tam_linha = 36
    
    comando = '''SELECT coren, nome FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    comando = '''SELECT cnpj, nome FROM Hospital'''
    hospitais = pega_info_db(comando)
    
    qnt_enfermeiras = len(enfermeiras)
    qnt_hospitais = len(hospitais)
    hospitais_associados = []
    
    if qnt_enfermeiras != 0 and qnt_hospitais != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()
            
            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Enfermeira?')
                imprime_linha(tam_linha)
                for i, enfermeira in enumerate(enfermeiras):
                    print(f'{i + 1} - {enfermeira[1]} ({enfermeira[0]})')
            else:
                if hospitais_associados == []:
                    comando = '''SELECT h.cnpj FROM Hospital h JOIN Hospital_x_Enfermeira h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren'''
                    registro = pega_info_db(comando, {'coren': coren_enfermeira})
                    if len(registro) != 0:
                        for hospital in registro:
                            hospitais_associados.append(hospital[0])
                
                if len(hospitais_associados) == qnt_hospitais:
                    mensagem = 'Enfermeira Ja Cadastrada em Todos os Hospitais!'
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
                opcao = filter_opcao(qnt_enfermeiras)
            else:
                opcao = filter_opcao(qnt_hospitais)
            
            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_enfermeira = enfermeiras[opcao - 1][0]
                    alterna += 1
                else:
                    cnpj_hospital = hospitais[opcao - 1][0]
                    break
        
        if opcao != 0:
            comando = '''INSERT INTO Hospital_x_Enfermeira (cnpj, coren) VALUES (:cnpj, :coren)'''
            associa = altera_db(comando, {'cnpj':cnpj_hospital,'coren':coren_enfermeira})
            
            if associa:
                mensagem_sucesso(titulo, 'Enfermeira', 'Associada')
            else:
                mensagem_erro(titulo, 'Enfermeira', 'Associar')
    else:
        if qnt_hospitais == 0 and qnt_enfermeiras == 0:
            mensagem = 'Ainda não há Enfermeiras e Hospitais Cadastrados!'
        elif qnt_enfermeiras == 0:
            mensagem = 'Ainda não há Enfermeiras Cadastrados!'
        else:
            mensagem = 'Ainda não há Hospitais Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)

def associa_enfermeira_medico():
    titulo = 'ENFERMEIRA X MEDICO'
    tam_linha = 36
    
    comando = '''SELECT coren, nome FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    comando = '''SELECT crm, nome FROM Medico'''
    medicos = pega_info_db(comando)
    
    qnt_enfermeiras = len(enfermeiras)
    qnt_medicos = len(medicos)
    medicos_associados = []
    
    if qnt_enfermeiras != 0 and qnt_medicos != 0:
        valido = True
        alterna = 0
        while True:
            limpa_tela()
            
            imprime_titulo(titulo, tam_linha)
            if alterna == 0:
                print('Qual Enfermeira?')
                imprime_linha(tam_linha)
                for i, enfermeira in enumerate(enfermeiras):
                    print(f'{i + 1} - {enfermeira[1]}')
            else:
                if medicos_associados == []:
                    comando = '''SELECT m.crm FROM Medico m JOIN Medico_x_enfermeira m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
                    registro = pega_info_db(comando, {'coren': coren_enfermeira})
                    if len(registro) != 0:
                        for medico in registro:
                            medicos_associados.append(medico[0])
                if len(medicos_associados) == qnt_medicos:
                    mensagem = 'Enfermeira Ja Associada a todos os Medicos!'
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
                opcao = filter_opcao(qnt_enfermeiras)
            else:
                opcao = filter_opcao(qnt_medicos)
            
            if opcao == -1:
                valido = False
            else:
                if alterna == 0:
                    coren_enfermeira = enfermeiras[opcao - 1][0]
                    alterna += 1
                else:
                    crm_medico = medicos[opcao - 1][0]
                    break
        
        if opcao != 0:
            comando = '''INSERT INTO Medico_x_Enfermeira (crm, coren) VALUES (:crm, :coren)'''
            associa = altera_db(comando, {'crm':crm_medico,'coren':coren_enfermeira})
            
            if associa:
                mensagem_sucesso(titulo, 'Enfermeira', 'Associada')
            else:
                mensagem_erro(titulo, 'Enfermeira', 'Associar')
    else:
        if qnt_medicos == 0 and qnt_enfermeiras == 0:
            mensagem = 'Ainda não há Enfermeiras e Medicos Cadastrados!'
        elif qnt_enfermeiras == 0:
            mensagem = 'Ainda não há Enfermeiras Cadastrados!'
        else:
            mensagem = 'Ainda não há Medicos Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)


def altera_enfermeira():
    titulo = 'ALTERA ENFERMEIRA'
    
    comando = '''SELECT * FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    qnt_enfermeiras = len(enfermeiras)
    
    if qnt_enfermeiras != 0:
        valido = True
        coren_enfermeira = ''
        while True:
            limpa_tela()
            
            imprime_titulo(titulo)
            for i, enfermeira in enumerate(enfermeiras):
                print(f'{i + 1} - {enfermeira[2]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()
            
            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True
            
            opcao = filter_opcao(qnt_enfermeiras)
            
            if opcao == 0:
                break
            
            if opcao == -1:
                valido = False
            else:
                coren_enfermeira = enfermeiras[opcao - 1][0]
                cpf_enfermeira = enfermeiras[opcao - 1][1]
                nome_enfermeira = enfermeiras[opcao - 1][2]
                rua_enfermeira = enfermeiras[opcao - 1][3]
                bairro_enfermeira = enfermeiras[opcao - 1][4]
                cidade_enfermeira = enfermeiras[opcao - 1][5]
                cep_enfermeira = enfermeiras[opcao - 1][6]
                break
        
        if opcao != 0:
            tipo_dado = ''
            dado = ''
            while True: # obtem dado
                limpa_tela()
                
                imprime_titulo(titulo)
                print('Qual dado deseja alterar?')
                imprime_linha()
                print(f'1 - Nome ({nome_enfermeira})')
                print(f'2 - CPF ({cpf_enfermeira})')
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
                            print(f'1 - Rua ({rua_enfermeira})')
                            print(f'2 - Bairro ({bairro_enfermeira})')
                            print(f'3 - Cidade ({cidade_enfermeira})')
                            print(f'4 - CEP ({cep_enfermeira})')
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
                comando = '''UPDATE Enfermeira SET {coluna} = :dado WHERE coren = :coren'''.format(coluna=tipo_dado)
                dados = {'coren': coren_enfermeira, 'dado': dado}
                    
                atualizado = altera_db(comando, dados)
                if atualizado:
                    mensagem_sucesso(titulo, 'Enfermeira', 'Alterada')
                else:
                    mensagem_erro(titulo, 'Enfermeira', 'Alterar')
    else:
        mensagem = 'Ainda não há Enfermeiras Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def menu_relatorios_enfermeira():
    quant_opcoes = 3
    qnt_linhas = 46
    
    valido = True
    while True:
        limpa_tela()
        
        imprime_titulo('RELATORIOS ENFERMEIRA', qnt_linhas)
        print('1 - Listar Enfermeiras')
        print('2 - Listar Hospitais que a Enfermeira trabalha')
        print('3 - Listar Medicos que a Enfermeira auxilia')
        imprime_linha(qnt_linhas)
        print('0 - Voltar')
        imprime_linha(qnt_linhas)
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!', qnt_linhas)
           
        opcao = filter_opcao(quant_opcoes)
            
        if opcao == 1:
            lista_enfermeiras()
        elif opcao == 2:
            lista_hospitais_enfermeira()
        elif opcao == 3:
            lista_medicos_enfermeira()
        elif opcao == 0:
            break
        else:
            valido = False

def lista_enfermeiras():
    titulo = 'LISTA DE ENFERMEIRAS'
    qnt_linhas = 36
    
    comando = '''SELECT * FROM Enfermeira'''
    Enfermeira = pega_info_db(comando)
    
    if len(Enfermeira) != 0:
        limpa_tela()
        imprime_titulo(titulo, qnt_linhas)
        for enfermeira in Enfermeira:
            print(f'Nome: {enfermeira[2]}')
            print(f'CPF: {enfermeira[1]}')
            print(f'COREN: {enfermeira[0]}')
            print('Endereco:')
            print(f'         Rua: {enfermeira[3]}')
            print(f'         Bairro: {enfermeira[4]}')
            print(f'         Cidade: {enfermeira[5]}')
            print(f'         CEP: {enfermeira[6]}')
            imprime_linha(qnt_linhas)
        pausa()  
    else:
        mensagem = 'Ainda não ha Enfermeira Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)

def lista_hospitais_enfermeira():
    titulo = 'ENFERMEIRA X HOSPITAIS'
    tam_linha = 37
    
    comando = '''SELECT coren, nome FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    if len(enfermeiras) != 0:
        valido = True
        while True:
            limpa_tela()
            
            imprime_titulo(titulo, tam_linha)
            for i, enfermeira in enumerate(enfermeiras):
                print(f'{i + 1} - {enfermeira[1]} ({enfermeira[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)
            
            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True
            
            opcao = filter_opcao(len(enfermeiras))
            
            if opcao == -1:
                valido = False
            else:
                coren = enfermeiras[opcao - 1][0]
                break
        
        if opcao != 0:
            comando = '''SELECT h.cnpj, h.nome, h.telefone FROM Hospital h JOIN Hospital_x_Enfermeira h_e ON h.cnpj = h_e.cnpj WHERE h_e.coren = :coren;'''
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
                mensagem = 'Ainda não há Hospitais Cadastrados para esta Enfermeira!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Enfermeiras Cadastrados!'
        mensagem_query_vazia(titulo, mensagem)

def lista_medicos_enfermeira():
    titulo = 'MEDICOS AUXILIADOS'
    tam_linha = 37
    
    comando = '''SELECT coren, nome FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    qnt_enfermeiras = len(enfermeiras)
    
    if qnt_enfermeiras != 0:
        valido = True
        while True:
            limpa_tela()
            
            imprime_titulo(titulo, tam_linha)
            for i, enfermeira in enumerate(enfermeiras):
                print(f'{i + 1} - {enfermeira[1]} ({enfermeira[0]})')
            imprime_linha(tam_linha)
            print('0 - Voltar')
            imprime_linha(tam_linha)
            
            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True
            
            opcao = filter_opcao(qnt_enfermeiras)
            
            if opcao == -1:
                valido = False
            else:
                coren = enfermeiras[opcao - 1][0]
                enfermeira = enfermeiras[opcao - 1]
                break
        
        if opcao != 0:
            comando = '''SELECT m.crm, m.nome FROM Medico m JOIN Medico_x_Enfermeira m_e ON m.crm = m_e.crm WHERE m_e.coren = :coren'''
            medicos = pega_info_db(comando, {"coren": coren})
            
            if medicos != []:
                limpa_tela()
                
                imprime_titulo(titulo, tam_linha)
                print(f'Medicos auxiliados por {enfermeira[1]}:')
                imprime_linha(tam_linha)
                for medico in medicos:
                    print(f'-> {medico[1]} ({medico[0]})')
                imprime_linha(tam_linha)
                
                pausa()
            else:
                mensagem = 'Ainda não ha medicos auxiliados por esta Enfermeira!'
                mensagem_query_vazia(titulo, mensagem)
    else:
        mensagem = 'Ainda não há Enfermeiras Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)


def exclui_dependencias(coren:str):
    comando = '''DELETE FROM Hospital_x_Enfermeira WHERE coren=:coren'''
    altera_db(comando, {'coren':coren})
    comando = '''DELETE FROM Medico_x_Enfermeira WHERE coren=:coren'''
    altera_db(comando, {'coren':coren})

def exclui_enfermeira():
    titulo = 'EXCLUIR ENFERMEIRA'
    
    comando = '''SELECT coren, nome FROM Enfermeira'''
    enfermeiras = pega_info_db(comando)
    
    qnt_enfermeiras = len(enfermeiras)
    
    if qnt_enfermeiras != 0:
        valido = True
        while True:
            limpa_tela()
            
            imprime_titulo(titulo)
            for i, enfermeira in enumerate(enfermeiras):
                print(f'{i + 1} - {enfermeira[1]}')
            imprime_linha()
            print('0 - Voltar')
            imprime_linha()
            
            if not valido:
                mensagem_input_invalido('Opcao Invalida!')
                valido = True
            
            opcao = filter_opcao(qnt_enfermeiras)
            
            if opcao == -1:
                valido = False
            else:
                coren_enfermeira = enfermeiras[opcao - 1][0]
                break
        
        if opcao != 0:

            exclui_dependencias(coren_enfermeira)
                        
            comando = '''DELETE FROM Enfermeira WHERE coren=:coren'''
            excluido = altera_db(comando, {'coren':coren_enfermeira})
            
            if excluido:
                mensagem_sucesso(titulo, 'Enfermeira', 'Excluida')
            else:
                mensagem_erro(titulo, 'Enfermeira', 'Excluir')
    else:
        mensagem = 'Ainda não há Enfermeiras Cadastradas!'
        mensagem_query_vazia(titulo, mensagem)

