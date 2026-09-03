#RESPONSABILIDADES: N CONTA, AGENCIA, DADOS SOBRE SALDO, EXTRATO, DEPÓSITO, SAQUE.

def cria_conta_agencia() :      #Atribui o número da conta em sua criação junto à uma
                                    #agência, que, por questão de simplicidade, será sempre a mesma.
    num_conta = 1
    num_agencia = 2
    return (num_conta, num_agencia, 0) #Obs.: 0 -> Saldo inicial da conta.

def deposito(saldo, deposito) : #Aumenta o saldo da conta com o valor do depósito.
    if deposito > 0:
        saldo = saldo + deposito
        return saldo
    else:
      return False

def saque(saldo, saque) : #Diminui o saldo da conta com o valor do saque.
     if saldo <= saque:
      saldo = saldo - saque
      return saldo
     else:
       return False



