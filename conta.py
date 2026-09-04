#RESPONSABILIDADES: N CONTA, AGENCIA, DADOS SOBRE SALDO, EXTRATO, DEPÓSITO, SAQUE.

def criar_conta_agencia() :      #Atribui o número da conta em sua criação junto à uma
                                    #agência, que, por questão de simplicidade, será sempre a mesma.
    num_conta = 123456
    num_agencia = 2
    return (num_conta, num_agencia, 0) #Obs.: 0 -> Saldo inicial da conta.

def deposito(saldo, valor_deposito) : #Aumenta o saldo da conta com o valor do depósito.
    if valor_deposito > 0:
        saldo = saldo + valor_deposito
        return saldo
    else:
      return False

def saque(saldo, valor_saque) : #Diminui o saldo da conta com o valor do saque.
     if saldo >= valor_saque:
      saldo = saldo - valor_saque
      return saldo
     else:
       return False

#Adicionado a função: Consultar Saldo

def consultar_saldo(saldo):
   print("Saldo atual: R$", saldo)



