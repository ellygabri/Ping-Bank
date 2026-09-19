from cliente import cpf_clientes
num_contas = []
num_agencias = []
tipo_contas = []
saldos = []
titulares = []


def verificador_existencia(num_conta, num_agencia): #Verifica a existência da conta e da agência no banco de dados.

    verificar_existencia = 0
    for indice_igual in range(len(num_contas)): #Navega por toda a lista a fim de constatar a existência dos dados.
        if num_contas[indice_igual] == num_conta and num_agencias[indice_igual] == num_agencia: #É de extrema importância alinhar os índices para garantir exatidão na checagem.
            return 1, indice_igual 
    return 0, None

def verificacao_seguranca(cpf_validacao): #Checagem de segurança (espécie de senha). Sujeito à alterações, pois a titulação feita na criação de conta possui falhas graves.

    for titular in titulares: 
        if titular == cpf_validacao:
            return 1
    return 0

def criar_conta(): #Criação da conta e adição dos dados relacionados.   

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
    regulador_agencia_conta = []
    for agencia in num_agencias: #Necessário para garantir a sequência numeral correta das contas.
        if agencia == num_agencia:  
            regulador_agencia_conta.append(agencia)
     
    if len(regulador_agencia_conta) > 0: #Checagem da existência da agência no banco de dados.
        num_conta = len(regulador_agencia_conta) + 1 #Adição do número da conta considerando a sequência de números de conta já existentes na agência digitada.
    else:
        num_conta = 1 #Adição da primeira conta da nova agência. 

            
    opcao_valor_inicial = int(input("Deseja informar um valor inicial para a conta? (1 - Sim, 2 - Não): ")) #Possibilidade de começar com um saldo inicial.
    if opcao_valor_inicial == 1:
        saldo = 0
        while saldo <= 0:
            saldo = float(input("Informe o valor inicial da conta: "))
    else:
        saldo = 0

    #Finalização. Todas as informações são adicionadas na última posição das listas. Necessário para o alinhamento dos índices.
    num_contas.append(num_conta)
    num_agencias.append(num_agencia)
    tipo_contas.append(tipo_conta)
    saldos.append(saldo)
 

    return 



def deposito(): #Aumenta o saldo da conta com o valor do depósito.

    num_conta = input("Digite o número da conta: ")
    num_agencia = input("Digite o número da agência: ")
    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    cpf_validacao = input("Por favor, digite o CPF do titular da conta: ") #Checagem de segurança (espécie de senha).
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Transação não autorizada.")
        return

    valor = float(input("Digite o valor a ser depositado: "))
    while valor <= 0: #Evitando valores inválidos.
        print("Valor inválido. Por favor, tente novamente.")
        valor = float(input("Digite o valor a ser depositado: "))

    saldos[indice] += valor #Finalização.
    print("Depósito realizado com sucesso.")
    return 

def saque(): #Diminui o saldo da conta com o valor do saque.

    num_conta = input("Digite o número da conta: ")
    num_agencia = input("Digite o número da agência: ")
    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    cpf_validacao = input("Por favor, digite o CPF do titular da conta: ") #Checagem de segurança (espécie de senha).
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Transação não autorizada.")
        return

    valor_saque = float(input("Digite o valor a ser sacado: "))
    while valor_saque < 0 or valor_saque > saldos[indice]: #Evitando valores inválidos.
        print("Valor inválido. Por favor, tente novamente.")
        valor_saque = float(input("Digite o valor a ser sacado: "))

    saldos[indice] -= valor_saque #Finalização.
    print("Saque realizado com sucesso.")
    return

def consultar_saldo(): #Consulta o saldo da conta.

    num_conta = input("Digite o número da conta: ")
    num_agencia = input("Digite o número da agência: ")
    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    cpf_validacao = input("Por favor, digite o CPF do titular da conta: ") #Checagem de segurança (espécie de senha).
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Transação não autorizada.")
        return
    
    print("Saldo atual: R$", saldos[indice]) #Finalização.
    return 



