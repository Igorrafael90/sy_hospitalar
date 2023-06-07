from controllers.enfermeira_controller import *
from utils.system_events import *
from utils.filters import *

def crud_enfermeira():
    quant_opcoes = 4
    valido = True
    while True:
        limpa_tela()
        
        imprime_menu_crud("ENFERMEIRA")
        
        if not valido:
            mensagem_input_invalido('Opcao Invalida!')
            valido = True
            
        opcao = filter_opcao(quant_opcoes)
            
        if opcao == 1:
            menu_insercao_enfermeira()
        elif opcao == 2:
            altera_enfermeira()
        elif opcao == 3:
            menu_relatorios_enfermeira()
        elif opcao == 4:
            exclui_enfermeira()
        elif opcao == 0:
            break
        else:
            valido = False

def imprime_menu_crud(titulo: str):
    imprime_titulo(f'CRUD {titulo}')
    print('1 - Inserir')
    print('2 - Alterar')
    print('3 - Relatorios')
    print('4 - Excluir')
    imprime_linha()
    print('0 - Voltar')
    imprime_linha()