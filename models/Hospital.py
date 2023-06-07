from models.Endereco import Endereco

class Hospital():
    def __init__(self, nome, telefone, endereco: Endereco, cnpj):
        self.nome = nome
        self.telefone = telefone
        self.endereco = endereco
        self.cnpj = cnpj
