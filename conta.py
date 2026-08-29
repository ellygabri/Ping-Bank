#RESPONSABILIDADES: N CONTA, AGENCIA, DADOS SOBRE SALDO, EXTRATO, DEPÓSITO, SAQUE.

def n_conta_agencia(nc) : #Atribui o número da conta em sua criação junto à uma
                  #agência, que, por questão de simplicidade, será sempre a mesma.
    nc = nc + 1;
    na = 2;
    return (nc, na, 0) #Obs.: 0 -> Saldo inicial da conta.

def deposito(saldo, valor) : #Aumenta o saldo da conta com o valor do depósito.
    saldo = saldo + valor;
    return saldo

def saque(saldo, valor) : #Diminui o saldo da conta com o valor do saque.
    saldo = saldo - valor;
    return saldo