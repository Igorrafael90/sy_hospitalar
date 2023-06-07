from models.Endereco import Endereco

class Medico():
    def __init__(self, nome, cpf, crm, endereco: Endereco, especialidade):
        self.nome = nome
        self.cpf = cpf
        self.crm = crm
        self.endereco = endereco
        self.especialidade = especialidade