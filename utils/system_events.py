import os

def limpa_tela():
    os.system('cls') if os.name == 'nt' else os.system('clear')

def pausa():
    input('\nPressione Enter. . .')