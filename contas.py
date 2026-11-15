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
    def depositar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido.")
        self.saldo += valor
    def sacar(self, valor):
        if valor <= 0:
            raise ValueError("Valor inválido.") 
        elif valor > self.saldo:
            raise ValueError("Saldo insuficiente.")
        self.saldo -= valor
    
