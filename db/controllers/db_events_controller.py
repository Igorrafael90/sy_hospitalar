import sqlite3 as sqlite
from db.resources.db_config import DB_PATH

from utils.system_events import *


def altera_db(comando:str, dados={}):
    conexao = None
    cursor = None
    resultado = True
    try:
        conexao = sqlite.connect(DB_PATH)
        cursor = conexao.cursor()
        
        cursor.execute(comando, dados)
        
        conexao.commit()
        
        resultado = True
    except sqlite.IntegrityError as erro:
        limpa_tela()
        print(f'Dado já cadastrado: {erro}')
        pausa()
        resultado = False
    except sqlite.DatabaseError as erro:
        limpa_tela()
        print(f'Erro Inesperado: {erro}')
        pausa()
        resultado = False
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
        return resultado

def pega_info_db(comando:str, dados={}):
    conexao = None
    cursor = None
    registros = []
    try:
        conexao = sqlite.connect(DB_PATH)
        cursor = conexao.cursor()
        
        if dados == {}:
            cursor.execute(comando)
        else:
            cursor.execute(comando, dados)
        
        registros = cursor.fetchall()
        
    except sqlite.DatabaseError as erro:
        print(erro)
        pausa()
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
        return registros
