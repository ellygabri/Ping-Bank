from cliente import clientes
contas = []

def criar_conta() :   

    titulares = [] #Lista de apoio para o cadastro dos titulares da conta.
    num_agencia = input("Informe o número da agência: ")
    tipo_conta = int(input("Informe o tipo de conta (1 - Individual, 2 - Conjunta): "))
    if tipo_conta == 2:
        qtd_titulares = int(input("Informe a quantidade de titulares da conta: "))
    else:
        qtd_titulares = 1
    tentativas = 0 

    while tentativas < qtd_titulares: #Loop de cadastro dos titulares, tolerante à erros de digitação.
        cpf = input("Informe o CPF do titular da conta: ")
        for cliente in clientes: #Checagem da existência do cliente no banco de dados.
            if cliente[1] == cpf:
                titulares.append(cpf)
                tentativas += 1
            else:
                print("Cliente não encontrado. Por favor, tente novamente.")

    for agencia in agencias: #Checagem da existência da agência no banco de dados.
        if agencia[0] == num_agencia:
            resultado = agencia
        else:
            resultado = 1
    num_conta = resultado[0][1] + 1 #Adição do número da conta considerando a sequência de números de conta já existentes na agência digitada.
            
    opcao_valor_inicial = int(input("Deseja informar um valor inicial para a conta? (1 - Sim, 2 - Não): "))
    if opcao_valor_inicial == 1:
        saldo = float(input("Informe o valor inicial da conta: "))
    else:
        saldo = 0

    conta = [num_conta, num_agencia, tipo_conta, saldo, titulares]
    contas.append(conta)
    
    return (conta) 



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



