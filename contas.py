from abc import ABC, abstractmethod

from clientes import buscar_cliente, normalizar_cpf
from agencias import buscar_agencia

class Conta(ABC):

    #__contas = {} <------------- ISSO É DA AGÊNCIA, NÃO É PRA SALVAR AQUI! ver com gabs a chamada para salvar

    def __init__(self, saldo, num_conta):
        if saldo < 0:
            self.__saldo = 0
        else:    
            self.__saldo = saldo
        self.__num_conta = num_conta #<---- aqui é melhor puxar da lista de contas existente em Agência, a fim de evitar duplicação
        #self.__cliente = Cliente.cpf, lembrar de passar no init
        #self.__contas[self.__num_conta] = {"saldo": saldo,
                                            #"tipo_conta": self.__tipo_conta}
    def __str__(self):
        return f"""
    ---- DADOS DA CONTA ----
    Número da conta: {self.__num_conta}
    Tipo da conta: {self.tipo_conta}
    Saldo disponível: {self.saldo}
    """
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
        if self.__num_conta == conta_destino:
            raise ValueError("As contas de origem e destino são a mesma.")
        self.validacao_valor(valor)
        self.sacar(valor)
        conta_destino.depositar(valor)
    @abstractmethod
    def tipo_conta(self):
        pass

class ContaCorrente(Conta):

    def __init__(self, saldo, num_conta):
        super().__init__(saldo, num_conta)
        self._cheque_especial = 200
    def __str__(self):
        base = super().__str__() 
        return f"{base}\nCheque especial disponível: {self._cheque_especial}"

    def sacar(self, valor):
        if valor > self.__saldo:
            excedente = valor - self.saldo 
            self.validacao_valor((self._cheque_especial - excedente))
            self.__saldo = 0
            self._cheque_especial -= excedente
        self.__saldo -= valor
    def tipo_conta(self):
        print('Conta do tipo "Corrente."')

class ContaPoupanca(Conta):

    def __init__(self, saldo, num_conta):
        super().__init__(saldo, num_conta)
    def __str__(self):
        base = super().__str__() 
        return f"{base}\nRendimento: {self._rendimento}"
    #def aplicar_rendimento(self):
        
    def tipo_conta(self):
        print('Conta do tipo "Poupança."')
        


    