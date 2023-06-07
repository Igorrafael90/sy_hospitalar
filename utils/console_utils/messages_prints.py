from utils.system_events import *
from utils.console_utils.console_prints import *


def mensagem_input_invalido(mensagem:str, tamanho_total=24):
    quant_espacos = (tamanho_total - len(mensagem) - 8) 
    if quant_espacos % 2 == 0:
        quant_espacos = int(quant_espacos / 2)
        print(' ' * quant_espacos + f'>>> {mensagem} <<<')
    else:
        quant_espacos = int((quant_espacos - 1) / 2)
        print(' ' * quant_espacos + f'>>> {mensagem} <<<')
    imprime_linha(tamanho_total)
    
def mensagem_erro(titulo:str, entidade:str, operacao:str):
    limpa_tela()
    
    imprime_titulo(titulo, 36)
    print(f'Não foi possível {operacao} o {entidade}!')
    imprime_linha(36)
    
    pausa()

def mensagem_sucesso(titulo:str, entidade:str, operacao:str):
    limpa_tela()
    
    imprime_titulo(titulo, 36)
    print(f'{entidade} {operacao} com Sucesso!')
    imprime_linha(36)
    
    pausa()
    
def mensagem_query_vazia(titulo:str, mensagem:str):
    tam_linha = len(mensagem)
    
    limpa_tela()
    imprime_titulo(titulo, tam_linha)
    print(mensagem)
    imprime_linha(tam_linha)
    pausa()
    