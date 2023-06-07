from db.controllers import *
from db.controllers.db_events_controller import altera_db
from models.Endereco import Endereco
from models.Handling import Handling
# from models.Handling import Handling
from utils.console_utils.console_prints import *
from utils.console_utils.messages_prints import *
from utils.system_events import *
from utils.validator import *

def filter_opcao(quant_opcoes):
    try:
        opcao = input('Opcao: ')
        
        if opcao.isdigit():
            opcao = int(opcao)
            if opcao < 0 or opcao > quant_opcoes:
                return -1
        elif opcao == '+':
            return opcao
        else:
            return -1
               
        return opcao
    except ValueError:
        return -1

def titulo_obtencao(titulo, tam=24):
    imprime_titulo(titulo, tam)
    print('0 - Cancelar')
    imprime_linha(tam)

def filter_rua(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('Rua Inválida!')
            valido = True
        rua = input('Insira a rua (endereco): ').strip().title()
        
        if rua != '0':
            if validate_nome(rua):
                return rua
            else:
                valido = False
        else:
            return False

def filter_bairro(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('Bairro Inválido!')
            valido = True
        bairro = input('Insira o bairro (endereco): ').strip().title()
        
        if bairro != '0':
            if validate_nome(bairro):
                return bairro
            else:
                valido = False
        else:
            return False  

def filter_cidade(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('Cidade Inválida!')
            valido = True
        cidade = input('Insira a Cidade (endereco): ').strip().title()
        
        if cidade != '0':
            if validate_nome(cidade):
                return cidade
            else:
                valido = False
        else:
            return False

def filter_cep(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('CEP Inválido!')
            valido = True
            
        cep = input('Insira o CEP (XXXXX-XXX): ').strip()
        
        if cep != '0':
            if validate_cep(cep.strip()):
                return cep
            else:
                valido = False        
        else:
            return False

def filter_nome(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('Nome Invalido!')
            valido = True
        nome = input('Insira o Nome: ').strip().title()
        
        if nome != '0':
            if validate_nome(nome):
                return nome
            else:
                valido = False
        else:
            return False
        
def filter_cnpj(titulo:str):
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam=36)
        if not valido:
            mensagem_input_invalido('CNPJ Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('CNPJ Ja Cadastrado!', 36)
            ja_cadastrado = False
        cnpj = input('Insira o CNPJ (XX.XXX.XXX/YYYY-ZZ): ').strip()
        
        if cnpj != '0':
            if validate_cnpj(cnpj):
                ja_cadastrado = validate_dado_ja_cadastrado('Hospital', 'cnpj', cnpj)
                if not ja_cadastrado:
                    return cnpj
            else:
                valido = False
        else:
            return False

def filter_crm(titulo:str):
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam=36)
        if not valido:
            mensagem_input_invalido('CRM Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('CRM Ja Cadastrado!', 36)
            ja_cadastrado = False
        crm = input('Insira o CRM (XXXX/UF): ').strip().upper()
        
        if crm != '0':
            if validate_crm(crm):
                ja_cadastrado = validate_dado_ja_cadastrado('Medico', 'crm', crm)
                if not ja_cadastrado:
                    return crm
            else:
                valido = False
        else:
            return False

def filter_coren(titulo:str):
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam=36)
        if not valido:
            mensagem_input_invalido('COREN Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('COREN Ja Cadastrado!', 36)
            ja_cadastrado = False
        coren = input('Insira o COREN (xxx.xxx.xxx): ').strip()
        
        if coren != '0':
            if validate_coren(coren):
                ja_cadastrado = validate_dado_ja_cadastrado('Enfermeira', 'coren', coren)
                if not ja_cadastrado:
                    return coren
            else:
                valido = False
        else:
            return False

def filter_cpf(titulo:str):
    entidades = ['Medico', 'Enfermeira', 'Paciente']
    
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam=36)
        
        if not valido:
            mensagem_input_invalido('CPF Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('CPF Ja Cadastrado!', 36)
            ja_cadastrado = False
            
        cpf = input('Insira o CPF (xxx.xxx.xxx-xx): ').strip()
        
        if cpf != '0':
            if validate_cpf(cpf):
                
                for entidade in entidades:
                    if validate_dado_ja_cadastrado(entidade, 'cpf', cpf):
                        ja_cadastrado = True
                        break
                
                if not ja_cadastrado:
                    return cpf
            else:
                valido = False
        else:
            return False

def filter_rg(titulo:str):
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam=36)
        
        if not valido:
            mensagem_input_invalido('RG Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('RG Ja Cadastrado!', 36)
            ja_cadastrado = False
            
        rg = input('Insira o RG (x.xxx.xxx-x): ').strip()
        
        if rg != '0':
            if validate_rg(rg):
                
                if validate_dado_ja_cadastrado('Paciente', 'rg', rg):
                    ja_cadastrado = True
                
                if not ja_cadastrado:
                    return rg
            else:
                valido = False
        else:
            return False

def filter_especialidade(titulo:str):
    valido = True
    checar = True
    while True:
        if checar:
            comando = '''SELECT * FROM Especialidade'''
            especialidades = pega_info_db(comando)
            
            qnt_especialidades = len(especialidades)
            
            if qnt_especialidades == 0:
                inserido = cadastrar_especialidade()
                if not inserido: return False
            checar = False
        
        limpa_tela()
        
        imprime_titulo(titulo, 36)
        print('Qual a especialidade do Medico?')
        imprime_linha(36)
        for i, espec in enumerate(especialidades):
            print(f'{i + 1} - {espec[1]}')
        imprime_linha(36)
        print('+ - Cadastrar Especialidade')
        print('0 - Cancelar')
        imprime_linha(36)
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!', 36)
            valido = True
        opcao = filter_opcao(qnt_especialidades)
        
        if opcao == 0:
            return False
        
        if opcao == '+':
            inserido = cadastrar_especialidade()
            if not inserido: return False
            checar = True
        else:
            if opcao != -1:
                especialidade = especialidades[opcao - 1][1]
                break 
            else:
                valido = False
    
    comando = '''SELECT * FROM Especialidade e WHERE e.titulo = :titulo'''
    especialidade = list(pega_info_db(comando, {'titulo': especialidade})[0])
    
    return especialidade

def cadastrar_especialidade():
    titulo_op = 'CADASTRAR ESPECIALIDADE'
    
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo_op, 36)
        
        if not valido:
            mensagem_input_invalido('Titulo Invalido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('Especialidade Ja Cadastrada!', 36)
            ja_cadastrado = False
        
        especialidade = input('Insira o Titulo: ').strip().title()
        
        if especialidade != '0':
            if validate_nome(especialidade):
                ja_cadastrado = validate_dado_ja_cadastrado('Especialidade', 'titulo', especialidade)
                if not ja_cadastrado:
                    comando = '''INSERT INTO Especialidade (titulo) VALUES (:titulo)'''
                    inserido = altera_db(comando, {'titulo': especialidade})
                    if inserido:
                        mensagem_sucesso(titulo_op, 'Especialidade', 'Inserida')
                        return True
                    else:
                        mensagem_erro(titulo_op, 'Especialidade', 'Inserir')
                        return False

            else:
                valido = False
        else:
            return False

def filter_telefone(titulo_op:str):
    valido = True
    ja_cadastrado = False
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo_op, tam=36)
        if not valido:
            mensagem_input_invalido('Telefone Inválido!', 36)
            valido = True
        if ja_cadastrado:
            mensagem_input_invalido('Telefone Ja Cadastrado!', 36)
            ja_cadastrado = False
        telefone = input('Insira o Telefone (XXXXX-XXXX): ').strip()
        
        if telefone != '0':
            if validate_telefone(telefone):
                ja_cadastrado = validate_dado_ja_cadastrado('Hospital', 'telefone', telefone)
                if not ja_cadastrado:
                    return telefone
            else:
                valido = False
        else:
            return False

def filter_endereco(titulo_op:str):
    rua = filter_rua(titulo_op)
    if not rua: return False
    
    bairro = filter_bairro(titulo_op)
    if not bairro: return False
          
    cidade = filter_cidade(titulo_op)
    if not cidade: return False
        
    cep = filter_cep(titulo_op)
    if not cep: return False
    
    return Endereco(rua, bairro, cidade, cep)

def filter_data(titulo:str):
    tam_linha = 43
    
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo, tam_linha)
        if not valido:
            mensagem_input_invalido('Data Invalida!', tam_linha)
            valido = True
            
        data = input('Insira a Data do Atendimento (dd/mm/aaaa): ').strip()
        
        if data != '0':
            if validate_data(data.strip()):
                return data
            else:
                valido = False        
        else:
            return False

def filter_cid(titulo:str):
    valido = True
    while True:
        limpa_tela()
        
        titulo_obtencao(titulo)
        if not valido:
            mensagem_input_invalido('CID Inválido!')
            valido = True
            
        cid = input('Insira o CID ([A...Z]XX): ').strip()
        
        if cid != '0':
            if validate_cid(cid):
                return cid
            else:
                valido = False        
        else:
            return False

def filter_handling(titulo:str, cpf_paciente:str):
    comando = '''SELECT crm, nome FROM Medico'''
    medicos = pega_info_db(comando)
    
    qnt_medicos = len(medicos)
    
    valido = True
    while True:
        limpa_tela()
        
        imprime_titulo(titulo, 36)
        print('Qual Medico Atendeu?')
        imprime_linha(36)
        for i, medico in enumerate(medicos):
            print(f'{i + 1} - {medico[1]} ({medico[0]})')
        imprime_linha(36)
        print('0 - Cancelar')
        imprime_linha(36)
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!', 36)
            valido = True
        opcao = filter_opcao(qnt_medicos)
        
        if opcao == 0:
            return False
        else:
            if opcao != -1:
                crm_medico = medicos[opcao - 1][0]
                break 
            else:
                valido = False
    
    cid = filter_cid(titulo)
    if not cid: return False
    
    data = filter_data(titulo)
    if not data: return False
    
    handling = Handling(cpf_paciente, crm_medico, cid, data)
    
    return handling