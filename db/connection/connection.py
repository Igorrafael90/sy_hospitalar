import sqlite3 as sqlite
from db.resources.db_config import *
from utils.system_events import pausa



def inicializa_database():
    conexao = None
    cursor = None
    try:
        conexao = sqlite.connect(DB_PATH)
        conexao.execute('PRAGMA foreign_keys = on')
        cursor = conexao.cursor()

        try:
            with open(DB_INITIAL_STRUCTURE_COMAND) as arquivo_comandos:
                for comando in arquivo_comandos:
                    cursor.execute(comando)
        except FileNotFoundError as erro1:
            print(f'ERRO: {erro1}')

        conexao.commit()
    except sqlite.DatabaseError as erro:
        print(f'ERRO: {erro}')
        pausa()
    finally:
        if cursor:
            cursor.close()
        if conexao:
            conexao.close()
