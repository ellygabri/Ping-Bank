from clientes import buscar_cliente, normalizar_cpf
from agencias import buscar_agencia

class Conta:

    __contas = {}

    def __init__(self, saldo, num_conta, tipo_conta):
        self.__saldo = saldo
        self.__num_conta = num_conta
        self.__tipo_conta = tipo_conta
        self.__contas[self.__num_conta] = {"saldo": saldo,
                                            "tipo_conta": self.__tipo_conta }
    @property
    def saldo(self):
        return self.__saldo  
    def validacao_valor(self, valor, validar_saida= True):
        if valor <= 0:
            raise ValueError("Valor inválido.") 
        elif validar_saida and valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
    def depositar(self, valor):
        self.validacao_valor(valor, False)
        self.__saldo += valor
    def sacar(self, valor):
        self.validacao_valor(valor)
        self.__saldo -= valor
    def transferencia(self, valor, conta_destino):
        self.validacao_valor(valor)
        self.sacar(valor)
        conta_destino.depositar(valor)

        

