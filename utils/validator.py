from datetime import date
from db.controllers.db_events_controller import pega_info_db


def validate_nome(nome: str):
    for letra in nome:
        if not letra.isalpha() and not letra.isspace():
            return False
    return True


def validate_cpf(cpf: str):
    # Mask -> xxx.xxx.xxx-xx
    if len(cpf) != 14:
        return False

    for i in range(len(cpf)):
        if i not in [3, 7, 11]:
            if not cpf[i].isdigit():
                return False
        elif i in [3, 7] and cpf[i] != '.':
            return False
        elif i == 10 and cpf[i] != '-':
            return False

    return True


def validate_cnpj(cnpj: str):
    # xx.xxx.xxx/xxxx-xx
    if len(cnpj) != 18:
        return False

    for i in range(len(cnpj)):
        if i not in [2, 6, 10, 15]:
            if not cnpj[i].isdigit():
                return False
        elif i in [2, 6] and cnpj[i] != '.':
            return False
        elif i == 10 and cnpj[i] != '/':
            return False
        elif i == 15 and cnpj[i] != '-':
            return False

    return True


def validate_telefone(telefone: str):
    # Mask -> XXXXX-XXXX
    if len(telefone) != 10:
        return False

    for i in range(len(telefone)):
        if i == 5:
            if telefone[i] != '-':
                return False
        else:
            if not telefone[i].isdigit():
                return False

    return True


def validate_cep(cep: str):
    # Mask -> xxxxx-xxx
    if len(cep) != 9:
        return False

    for i in range(len(cep)):
        if i == 5:
            if cep[i] != '-':
                return False
        else:
            if not cep[i].isdigit:
                return False

    return True


def validate_crm(crm: str):
    # Mask ->  xxxx/UF
    if len(crm) != 7:
        return False

    for i in range(len(crm)):
        if i < 4 and not crm[i].isdigit():
            return False
        if i == 4 and crm[i] != '/':
            return False
        if i > 4 and not crm[i].isalpha():
            return False

    if not validate_uf(f'{crm[5]}{crm[6]}'):
        return False

    return True


def validate_rg(rg: str):
    # Mask -> x.xxx.xxx-x
    if len(rg) != 11:
        return False

    for i in range(len(rg)):
        if i not in [1, 5, 9]:
            if not rg[i].isdigit():
                return False
        if i in [1, 5] and rg[i] != '.':
            return False
        if i == 9 and rg[i] != '-':
            return False

    return True


def validate_coren(coren: str):
    # Mask ->  xxx.xxx.xxx
    if len(coren) != 11:
        return False

    for i in range(len(coren)):
        if i in [3, 7]:
            if coren[i] != '.':
                return False
        else:
            if not coren[i].isdigit():
                return False

    return True


def validate_cid(cid: str):
    if len(cid) != 3:
        return False

    if not cid[0].isalpha():
        return False

    if not cid[1].isdigit() or not cid[2].isdigit():
        return False

    return True


def validate_uf(uf: str):
    estados = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE',
               'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
               'PA', 'PB', 'PR', 'PE', 'PI', 'RJ',
               'RN', 'RS', 'RO', 'RR', 'SC', 'SP',
               'SE', 'TO', 'DF']

    return uf.upper() in estados


def validate_data(data: str):
    # Mask -> dd/mm/aaaa
    if len(data) != 10:
        return False

    for i in range(len(data)):
        if i not in [2, 5]:
            if not data[i].isdigit():
                return False
        else:
            if data[i] != '/':
                return False

    try:
        dia = int(f'{data[0]}{data[1]}')
        mes = int(f'{data[3]}{data[4]}')
        ano = int(f'{data[6]}{data[7]}{data[8]}{data[9]}')
    except ValueError:
        return False

    ano_atual = date.today().year
    if ano > ano_atual:
        return False

    try:
        date(ano, mes, dia)
    except ValueError:
        return False

    return True


def validate_dado_ja_cadastrado(tabela: str, nome_dado: str, dado):
    comando = f'SELECT {nome_dado} FROM {tabela}'
    registros = pega_info_db(comando)

    cadastrados = []
    for registro in registros:
        cadastrados.append(registro[0])

    return True if dado in cadastrados else False
