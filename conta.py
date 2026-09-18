from cliente import cpf_clientes
num_contas = []
num_agencias = []
tipo_contas = []
saldos = []
titulares = []


def criar_conta() :   

    tipo_conta = int(input("Informe o tipo de conta (1 - Individual, 2 - Conjunta): "))
    if tipo_conta == 2:
        qtd_titulares = int(input("Informe a quantidade de titulares da conta: "))
    else:
        qtd_titulares = 1
    tentativas = 0 

    while tentativas < qtd_titulares: #Loop de cadastro dos titulares, tolerante à erros de digitação.
        cpf = input("Informe o CPF do titular da conta: ")
        for cpf_cliente in cpf_clientes: #Checagem da existência do cliente no banco de dados.
            if cpf_cliente == cpf:
                titulares.append(cpf)
                tentativas += 1
            else:
                print("Cliente não encontrado. Por favor, tente novamente.")

    num_agencia = input("Informe o número da agência: ")
    regulador_agencia_conta = [agencia for agencia in agencias if num_agencias == num_agencia] #Necessário para garantir a sequência numeral das contas.
    if len(regulador_agencia_conta) > 0: #Checagem da existência da agência no banco de dados.
        num_conta = len(regulador_agencia_conta) + 1 #Adição do número da conta considerando a sequência de números de conta já existentes na agência digitada.
    else:
        num_conta = 1

            
    opcao_valor_inicial = int(input("Deseja informar um valor inicial para a conta? (1 - Sim, 2 - Não): "))
    if opcao_valor_inicial == 1:
        saldo = 0
        while saldo <= 0:
            saldo = float(input("Informe o valor inicial da conta: "))
    else:
        saldo = 0
    num_contas.append(num_conta)
    tipo_contas.append(tipo_conta)
    saldos.append(saldo)
    num_agencias.append(num_agencia) 

    return 



# def deposito() : #Aumenta o saldo da conta com o valor do depósito.
#     valor_deposito = float(input("Insira o valor a ser depositado: "))
#     num_conta = input("Digite o número da conta: ")
#     conta_da_movimentacao = []
#     for conta in contas: #Checagem da existência da conta no banco de dados.
#         if conta[1] == num_conta:
#             conta_da_movimentacao = conta
#         else:
#             print("Conta não encontrada. Por favor, tente novamente.")
#         return

#     num_agencia = input("Digite o número da agência: ")
#     if conta_da_movimentacao[1] != num_agencia: #Checagem da correspondência entre a agência e a conta digitadas.
#         print("Agência não correspondente à conta informada. Por favor, tente novamente.")
#         return

#     cpf = input("Para fins de verificação, por favor, informe o CPF do titular: ")
#     for titulares in conta_da_movimentacao: #Checagem da existência do cliente no banco de dados.
#         if conta_da_movimentacao[4][0] != cpf:
#             print("Movimento não autorizado.")
#             return
#         else:            
#             if valor_deposito > 0:
                
#             else:
#                 print("Valor inválido. Por favor, tente novamente.")    
#                 return
#         return 

def saque(saldo, valor_saque) : #Diminui o saldo da conta com o valor do saque.
     if saldo >= valor_saque:
      saldo = saldo - valor_saque
      return saldo
     else:
       return False

#Adicionado a função: Consultar Saldo

def consultar_saldo(saldo):
   print("Saldo atual: R$", saldo)



