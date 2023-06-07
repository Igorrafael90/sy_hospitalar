import sqlite3 as sqlite

from utils.system_events import pausa

DB_PATH = 'db/resources/database.db'
DB_INITIAL_STRUCTURE_COMAND = 'db/resources/init_db_commands.txt'

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
