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

    contas[indice] = contas[indice][:3] + (contas[indice][3] + valor_deposito,) + contas[indice][4:] #Finalização. O valor de depósito é adicionado ao valor preexistente.
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
    while valor_saque < 0 or valor_saque > contas[indice][3]: #Evitando valores inválidos.
        print("Valor inválido. Por favor, tente novamente.")
        valor_saque = float(input("Digite o valor a ser sacado: "))

    contas[indice] = contas[indice][:3] + (contas[indice][3] - valor_saque,) + contas[indice][4:] #Finalização. O valor de saque é subtraído do valor preexistente.
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
    
    print("Saldo atual: R$", contas[indice][3]) #Finalização.
    return 

def listar_contas(): #Lista todas as contas cadastradas no banco de dados.
    
    if len(contas) == 0: #Tratamento de lista vazia.
        print("Não há contas cadastradas!")
        return
    
    print("==== CONTAS CADASTRADAS ====")

    for conta_apresentada in contas: #Contas apresentadas conforme a lista é percorrida.
        print("Número da conta: ", conta_apresentada[0])
        print("Número da agência: ", conta_apresentada[1])
        print("Tipo de conta: ", "Individual" if conta_apresentada[2] == 1 else "Conjunta")
        print("Saldo: R$", conta_apresentada[3])
        print("Titulares: ", ", ".join(conta_apresentada[4]))
        print("==============================")

def alterar_dados_conta(): #Altera os dados passíveis de alteração da conta.

    num_conta = input("Digite o número da conta: ")
    num_agencia = input("Digite o número da agência: ")
    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    cpf_validacao = input("Por favor, digite o CPF do titular da conta: ") #Checagem de segurança (espécie de senha).
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return

    print("==== ALTERAR DADOS DA CONTA ====") #Menu de opções para alteração.
    print("1 - Alterar tipo de conta")
    print("2 - Alterar titulares da conta")
    print("Digite outros números para retornar ao menu principal.")
    opcao_alteracao = int(input("Escolha a opção desejada: "))
    
    if opcao_alteracao == 1: #Opção para alterar o tipo de conta.
        novo_tipo_conta = int(input("Informe o novo tipo de conta (1 - Individual, 2 - Conjunta): "))

        if novo_tipo_conta == 1: #...Caso individual
            novo_titular_unico = input("Informe o CPF titular unitário da conta: ")
            contas[indice] = contas[indice][:4] + (novo_titular_unico,) #Basta apenas vincular ao final da lista menos o último elemento (os titulares antigos)
            print("Tipo de conta alterado com sucesso: Individual, CPF: ", contas[indice][4])
            return

        elif novo_tipo_conta == 2: #... Caso conjunta
            qtd_novos_titulares = int(input("Informe a quantidade de titulares da conta: "))
            while qtd_novos_titulares < 2: #Verificação para garantir a quantidade referente ao tipo.
                print("Para uma conta conjunta, é necessário ter pelo menos dois titulares. Por favor, tente novamente.")
                qtd_novos_titulares = int(input("Informe a quantidade de titulares da conta: "))

            tentativas = 0 
            titulares = ()
            while tentativas < qtd_novos_titulares: #Loop de cadastro dos titulares, tolerante à erros de digitação.
                cpf = input("Informe o CPF do novo titular da conta: ")
                if cpf in cpf_clientes: #Checagem da existência do cliente no banco de dados.
                    titulares = titulares + (cpf,)
                    tentativas += 1
                else:
                    print("Cliente não encontrado. Por favor, tente novamente.")

            # Finalização. A lista original é fatiada nos valores aos quais interessa a modificação. 
            # Entre as partes fatiadas, os novos valores são inseridos.
            contas[indice] = contas[indice][:2] + (novo_tipo_conta,) + contas[indice][3] + (contas[indice][:4] + (titulares,)) 
            print("Tipo de conta alterado com sucesso: ", contas[indice][2], ", CPF´s: ", ", ".join(contas[indice][4]))
        else:
            print("Opção inválida. Por favor, tente novamente.")
            return
    
    elif opcao_alteracao == 2: #Opção para alterar os titulares da conta.
        print("=== ATUAIS TITULARES === ") #Os atuais titulares são apresentados.
        print("Titulares: ", ", ".join(contas[indice][4]))
        print("==========================") #... E as novas opções de alteração são apresentadas.
        print("1 - Adicionar titular")
        print("2 - Remover titular")
        print("3 - Substituir titular")
        print("4 - Excluir conta")
        print("Digite outros números para retornar ao menu principal.")
        opcao_titular = int(input("Escolha a opção desejada: ")) 

        if opcao_titular == 1: #Adição de titular.
            titulares = () #Lista de apoio.
            while titulares != 0: #Loop de cadastro dos titulares, tolerante à erros de digitação.

                novo_titular = input("Informe o CPF do titular a ser adicionado (0 para finalizar): ")
                for procurar_titular in cpf_clientes: #Checagem da existência do cliente no banco de dados.
                    if novo_titular in cpf_clientes:
                        titular_adicionado = contas[procurar_titular][4] #Resgate da tupla de titulares.
                        indice_a_adicionar = 0 #Índice de interesse.
                        for cpf_adicionado in titular_adicionado: #Buscamos o CPF em questão na tupla e adicionamos um valor ao índice caso não o encontremos,
                            if cpf_adicionado != novo_titular:    # representando que o índice de interese não é o que foi checado no momento.
                                indice_a_adicionar += 1
                            else:
                                break
                        #Alteramos a tupla que resgatamos, de modo a adicionar o novo titular.
                        titular_adicionado = titular_adicionado[:indice_a_adicionar] + (novo_titular,) + titular_adicionado[indice_a_adicionar + 1:]
                        contas[procurar_titular] = contas[procurar_titular][:4] + (titular_adicionado,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                        print("Titular adicionado com sucesso: ", ", ".join(contas[procurar_titular][4]))
                        return
                    else:
                        print("Cliente não encontrado. Por favor, tente novamente.")
            
        elif opcao_titular == 2: #Remoção de titular.

            titular_a_remover = input("Informe o CPF do titular a ser removido: ")
            for procurar_titular in cpf_clientes: #Checagem da existência do cliente no banco de dados.
                if titular_a_remover in contas[procurar_titular][4]:
                    titular_subtraido = contas[procurar_titular][4] #Resgate da tupla de titulares.
                    indice_a_subtrair = 0 #Índice de interesse.
                    for cpf_subtraido in titular_subtraido: #Buscamos o CPF em questão na tupla e adicionamos um valor ao índice caso não o encontremos,
                        if cpf_subtraido != titular_a_remover: # representando que o índice de interesse não é o que foi checado no momento.
                            indice_a_subtrair += 1
                        else:
                            break
                    #Alteramos a tupla que resgatamos, de modo a remover o titular. (Note que não consideramos o índice encontrado no momento de unir a tupla, indicando uma exclusão)
                    titular_subtraido = titular_subtraido[:indice_a_subtrair] + titular_subtraido[indice_a_subtrair + 1:]
                    contas[procurar_titular] = contas[procurar_titular][:4] + (titular_subtraido,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                    print("Titular removido com sucesso: ", contas[procurar_titular][4])
                    return
                else:
                   print("Cliente não encontrado. Por favor, tente novamente.")
        elif opcao_alteracao == 3: 

            titular_a_alterar = input("Informe o CPF do titular a ser alterado: ")


            for procurar_titular in cpf_clientes: #Checagem da existência do cliente no banco de dados.
                if titular_a_alterar in contas[procurar_titular][4]: 
                    titular_alterado = contas[procurar_titular][4] #Resgate da tupla de titulares.
                    indice_a_alterar = 0 #Índice de interesse.
                    for cpf_alterado in titular_alterado: #Buscamos o CPF em questão na tupla e adicionamos um valor ao índice caso não o encontremos,
                        if cpf_alterado != titular_a_alterar: # representando que o índice de interesse não é o que foi checado no momento.
                            indice_a_alterar += 1
                        else:
                            break
                    novo_titular = input("Informe o CPF do novo titular: ") #(!ALERTA!: Necessário adicionar uma checagem de existência. Postergada em razão da possibilidade de alteração na lógica atual da checagem)
                    #Alteramos a tupla que resgatamos, de modo a substituir o titular. O índice encontrado é o ponto do corte, o novo tituar é inserido no meio da tupla, de modo a substituir o valor antigo.
                    titular_alterado = titular_alterado[:indice_a_alterar] + (novo_titular,) + titular_alterado[indice_a_alterar + 1:]
                    contas[procurar_titular] = contas[procurar_titular][:4] + (titular_alterado,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                    print("Titular alterado com sucesso: ", contas[procurar_titular][4])
                    return
        elif opcao_alteracao == 4: #Exclusão da conta.

            conta_a_excluir = input("Informe o número da conta a ser deletada: ")
            agencia_da_conta = input("Informe o número da agência da conta a ser deletada: ")

            verificar_existencia, indice = verificador_existencia(conta_a_excluir, agencia_da_conta) #Verifica a existência da conta e da agência no banco de dados.
            if verificar_existencia != 1:
                print("Os dados não correspondem. Por favor, tente novamente.")
                return
            
            if len(contas[indice][4]) > 2 or contas[indice][3] > 0: #Verificação de saldo e quantidade de titulares, a fim de evitar exclusão indevida.
                print("Não é possível excluir a conta. A conta possui saldo e/ou mais de um titular. Por favor, revise os dados e tente novamente.")
                return
            else:
                print("A conta será excluída. Tem certeza? Digite 'Sim' ou 'Não' para confirmar.")
                while True: #Loop de confirmação, tolerante à erros de digitação.
                    confirmacao = input("Confirmação: ")
                    if confirmacao.strip().lower() == 'não': 
                        print("Exclusão cancelada.")
                        return
                    elif confirmacao.strip().lower() == 'sim': 
                        print("Excluindo a conta...")
                        #Removemos a tupla do índice indicado pela checagem de existência.
                        contas.pop(indice) #Finalização. A tupla da conta é excluída.
                        print("Conta excluída com sucesso.")
                        return
                    else:
                        print("Opção inválida. Por favor, tente novamente.")
        else:
            return
