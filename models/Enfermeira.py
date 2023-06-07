from models.Endereco import Endereco


class Enfermeira():
    def __init__(self, coren:str, cpf:str, nome:str, endereco:Endereco):
        self.coren = coren
        self.cpf = cpf
        self.nome = nome
        self.endereco = endereco  