from db.connection.connection import inicializa_database
from utils.system_events import *
from utils.console_utils.crud_menus import *

def main():
    inicializa_database()

    quant_opcoes = 4
    valido = True
    while True:
        limpa_tela()
        
        imprime_menu_principal()
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!')
            valido = True
        opcao = filter_opcao(quant_opcoes)
            
        # if opcao == 1:
            # TODO: crud_hospital()
        # elif opcao == 2:
            # TODO: crud_medico()
        if opcao == 3:
            crud_enfermeira()
        # elif opcao == 4:
            # TODO: crud_paciente()
        elif opcao == 0:
            break
        else:
            valido = False
    
    mensagem_finalizacao()

def imprime_menu_principal():
    imprime_titulo('MENU PRINCIPAL')
    print('1 - Hospitais')
    print('2 - Medicos')
    print('3 - Enfermeiras')
    print('4 - Pacientes')
    imprime_linha()
    print('0 - Sair')
    imprime_linha()

def mensagem_finalizacao():
    limpa_tela()
    imprime_titulo('SISTEMA HOSPITALAR', 48)
    print("Obrigado por utilizar o programa. Até a próxima!")
    imprime_linha(48)
    pausa()
    limpa_tela()

if __name__ == '__main__':
    main()