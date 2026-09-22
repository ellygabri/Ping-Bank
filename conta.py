from cliente import cpf_clientes


contas = []


def verificador_existencia(num_conta, num_agencia): #Verifica a existência da conta e da agência no banco de dados.

    for conta in range(len(contas)): #Navega por toda a lista a fim de constatar a existência dos dados.
        if contas[conta][0] == num_conta and contas[conta][1] == num_agencia: #É de extrema importância alinhar os índices para garantir exatidão na checagem.
            return 1, conta 
    return 0, None

def verificacao_seguranca(cpf_validacao): #Checagem de segurança (uma espécie de senha).

    for titular in contas: 
        if cpf_validacao in titular[4]: 
            return 1
    return 0

def criar_conta(): #Criação da conta e adição dos dados relacionados.   

    tipo_conta = int(input("Informe o tipo de conta (1 - Individual, 2 - Conjunta): "))
    if tipo_conta == 2:
        qtd_titulares = int(input("Informe a quantidade de titulares da conta: "))
    else:
        qtd_titulares = 1
    tentativas = 0 
    titulares = ()

    while tentativas < qtd_titulares: #Loop de cadastro dos titulares, tolerante à erros de digitação.
        cpf = input("Informe o CPF do titular da conta: ")
        #Checagem da existência do cliente no banco de dados.
        if cpf in cpf_clientes:
            titulares = titulares + (cpf,)
            tentativas += 1
        else:
            print("Cliente não encontrado. Por favor, tente novamente.")

    num_agencia = input("Informe o número da agência: ")
    regulador_agencia_conta = []
    for agencia in contas: #Necessário para garantir a sequência numeral correta das contas.
        if agencia[1] == num_agencia:  
            regulador_agencia_conta.append(agencia)
     
    if len(regulador_agencia_conta) > 0: #Checagem da existência da agência no banco de dados.
        num_conta = len(regulador_agencia_conta) + 1 #Adição do número da conta considerando a sequência de números de conta já existentes na agência digitada.
    else:
        num_conta = 1 #Adição da primeira conta da nova agência. 

            
    opcao_valor_inicial = int(input("Deseja informar um valor inicial para a conta? (1 - Sim, 2 - Não): ")) #Possibilidade de começar com um saldo inicial.
    if opcao_valor_inicial == 1:
        saldo = 0
        while saldo < 0:
            saldo = float(input("Informe o valor inicial da conta: "))
    else:
        saldo = 0

    #Finalização. Todas as informações são adicionadas na última posição das listas.
    contas.append((num_conta, num_agencia, tipo_conta, saldo, titulares))
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

    valor_deposito = float(input("Digite o valor a ser depositado: "))
    while valor_deposito <= 0: #Evitando valores inválidos.
        print("Valor inválido. Por favor, tente novamente.")
        valor_deposito = float(input("Digite o valor a ser depositado: "))

    contas[indice] = contas[indice][:4] + (valor_deposito,) + contas[indice][5:]#Finalização.
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
    while valor_saque < 0 or valor_saque > contas[indice][4]: #Evitando valores inválidos.
        print("Valor inválido. Por favor, tente novamente.")
        valor_saque = float(input("Digite o valor a ser sacado: "))

    contas[indice] = contas[indice][:4] + (contas[indice][4] - valor_saque,) + contas[indice][5:] #Finalização.
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
    
    print("Saldo atual: R$", contas[indice][4]) #Finalização.
    return 

def listar_contas(): #Lista todas as contas cadastradas no banco de dados.
    
    if len(contas) == 0:
        print("Não há contas cadastradas!")
        return
    
    print("==== CONTAS CADASTRADAS ====")

    for conta_apresentada in contas:
        print("Número da conta: ", conta_apresentada[0])
        print("Número da agência: ", conta_apresentada[1])
        print("Tipo de conta: ", "Individual" if conta_apresentada[2] == 1 else "Conjunta")
        print("Saldo: R$", conta_apresentada[3])
        print("Titulares: ", ", ".join(conta_apresentada[4]))
        print("==============================")

