def imprime_titulo(titulo: str, tamanho=24):
    linha = (tamanho - len(titulo))
    if linha % 2 == 0:
        linha = int(linha / 2)
        print(('-' * linha) + f'{titulo}' + ('-' * linha))
    else:
        linha = int((linha - 1) / 2)
        print(('-' * linha) + f'{titulo}' + ('-' * (linha + 1)))  

def imprime_linha(tamanho=24):
    print('-' * tamanho)