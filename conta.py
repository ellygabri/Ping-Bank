from main import clientes #lista de clientes encontrados em main.py
from main import agencias

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


def criar_conta(tipo_conta, titulares,num_agencia, saldo): #Criação da conta e adição dos dados relacionados.   

    confirmacao_existencia = 0
    regulador_agencia_conta = []

    for conta in contas: #Necessário para garantir a sequência numeral correta das contas.
        if conta[1] == num_agencia:  
            regulador_agencia_conta.append(conta)
    for agencia in agencias: #Checagem da existência da agência no banco de dados.
        if agencia[0] == num_agencia:
            confirmacao_existencia = 1
            if len(regulador_agencia_conta) > 0: 
                num_conta = len(regulador_agencia_conta) + 1 #Adição do número da conta considerando a sequência de números de conta já existentes na agência digitada.
            else:
                num_conta = 1 #Adição da primeira conta da nova agência. 
    if confirmacao_existencia != 1: 
        print("Agência não localizada. Por favor, tente novamente.")
        return            

    #Finalização. Todas as informações são adicionadas na última posição das listas.
    contas.append((num_conta, num_agencia, tipo_conta, saldo, titulares))
    return contas


def deposito(num_conta, num_agencia, cpf_validacao, valor_deposito): #Aumenta o saldo da conta com o valor do depósito.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Transação não autorizada.")
        return
    
    contas[indice] = contas[indice][:3] + (contas[indice][3] + valor_deposito,) + contas[indice][4:] #Finalização. O valor de depósito é adicionado ao valor preexistente.
    print("Depósito realizado com sucesso. Saldo atual: R$", contas[indice][3])
    return 

def saque(num_conta, num_agencia, cpf_validacao, valor_saque): #Diminui o saldo da conta com o valor do saque.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Transação não autorizada.")
        return
    
    contas[indice] = contas[indice][:3] + (contas[indice][3] - valor_saque,) + contas[indice][4:] #Finalização. O valor de saque é subtraído do valor preexistente.
    print("Saque realizado com sucesso. Saldo atual: R$", contas[indice][3])
    return

def consultar_saldo(num_conta, num_agencia, cpf_validacao): #Consulta o saldo da conta.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
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
    return

def alterar_tipo_conta(num_conta, num_agencia, cpf_validacao, novo_tipo_conta, titulares): #Altera o tipo de conta (individual ou conjunta).

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return
    if novo_tipo_conta == 1 and len(titulares) != 1:
        print("Apenas um titular é permitido para uma conta individual. Por favor, tente novamente.")
        return
    elif novo_tipo_conta == 2 and len(titulares) < 2:
        print("Para uma conta conjunta, é necessário ter pelo menos dois titulares. Por favor, tente novamente.")
        return
    
    # Finalização. A lista original é fatiada nos valores aos quais interessa a modificação. 
    # Entre as partes fatiadas, os novos valores são inseridos.
    contas[indice] = contas[indice][:2] + (novo_tipo_conta,) + contas[indice][3] + (contas[indice][:4] + (titulares,)) 
    print("Tipo de conta alterado com sucesso: ", contas[indice][2], ", CPF´s: ", ", ".join(contas[indice][4]))
    return 
    
def adicionar_titulares(num_conta, num_agencia, cpf_validacao, titulares): #Altera os titulares da conta.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return

    procurar_titular = clientes[indice]
    atuais_titulares = contas[indice][4] 
    for titular in titulares:
        atuais_titulares = contas[indice][4]
        if titular in procurar_titular[4]:
            if titular not in atuais_titulares:
                #Alteramos a tupla que resgatamos, de modo a adicionar o novo titular.
                titular_adicionado = atuais_titulares + (titular,)
                contas[indice] = contas[indice][:4] + (titular_adicionado,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                print("Titular adicionado com sucesso: ", ", ".join(contas[indice][4]))
            else: 
                print("O CPF cadastrado já possui a titularidade da conta. Por favor, tente novamente.")
        else:
            print("Um dos titulares não tem o cpf cadastrado. Por favor, tente novamente.")
            print("Titulares atuais: ", ", ".join(contas[indice][4]))
            return

def remover_titulares(num_conta, num_agencia, cpf_validacao, titulares): #Altera os titulares da conta.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return
    
    procurar_titular = clientes[indice] 
    for titular in titulares:
        atuais_titulares = contas[indice][4]
        if titular in procurar_titular[4]:
            if titular in atuais_titulares:
                    titular_subtraido = atuais_titulares #Resgate da tupla de titulares.
                    indice_a_subtrair = 0 #Índice de interesse.
                    for cpf_subtraido in titular_subtraido: #Buscamos o CPF em questão na tupla e adicionamos um valor ao índice caso não o encontremos,
                        if cpf_subtraido != titular: # representando que o índice de interesse não é o que foi checado no momento.
                            indice_a_subtrair += 1
                        else:
                            break
                    #Alteramos a tupla que resgatamos, de modo a remover o titular. (Note que não consideramos o índice encontrado no momento de unir a tupla, indicando uma exclusão)
                    titular_subtraido = titular_subtraido[:indice_a_subtrair] + titular_subtraido[indice_a_subtrair + 1:]
                    contas[indice] = contas[indice][:4] + (titular_subtraido,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                    print("Titular removido com sucesso")
            else: 
                print("O CPF digitado NÃO possui a titularidade da conta. Por favor, tente novamente.")
        else:
            print("Um dos titulares não tem o cpf cadastrado. Por favor, tente novamente.")
            print("Titulares atuais: ", ", ".join(contas[indice][4]))
    return


def alterar_titulares(num_conta, num_agencia, cpf_validacao, titular_antigo, titular_novo): #Altera os titulares da conta.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return
    
    procurar_titular = clientes[indice] 
    if titular_antigo in procurar_titular[4]:
        if titular_antigo in contas[indice][4]:
                titular_alterado = contas[indice][4] #Resgate da tupla de titulares.
                indice_a_subtrair = 0 #Índice de interesse.
                for cpf_alterado in titular_alterado: #Buscamos o CPF em questão na tupla e adicionamos um valor ao índice caso não o encontremos,
                    if cpf_alterado != titular_antigo: # representando que o índice de interesse não é o que foi checado no momento.
                        indice_a_subtrair += 1
                    else:
                        break

                titular_alterado = titular_alterado[:indice_a_subtrair] + (titular_novo,) + titular_alterado[indice_a_subtrair + 1:]
                contas[indice] = contas[indice][:4] + (titular_alterado,) #Finalização. A tupla de titulares alterada é adicionada às informações do cliente na lista.
                print("Titular alterado com sucesso: ", ", ".join(contas[indice][4]))
                return
        else: 
            print("O CPF digitado NÃO possui a titularidade da conta. Por favor, tente novamente.")
    else:
        print("Um dos titulares não tem o cpf cadastrado. Por favor, tente novamente.")
        print("Titulares atuais: ", ", ".join(contas[indice][4]))
    return

def excluir_conta(num_conta,num_agencia, cpf_validacao): #Exclusão da conta.

    verificar_existencia, indice = verificador_existencia(num_conta, num_agencia) #Verifica a existência da conta e da agência no banco de dados.
    if verificar_existencia != 1:
        print("Os dados não correspondem. Por favor, tente novamente.")
        return
    
    if (verificacao_seguranca(cpf_validacao)) != 1:
        print("Ação não autorizada.")
        return
    
    if len(contas[indice][4]) > 2 or contas[indice][3] > 0: #Verificação de saldo e quantidade de titulares, a fim de evitar exclusão indevida.
        print("Não é possível excluir a conta. A conta possui saldo e/ou mais de um titular. Por favor, revise os dados e tente novamente.")
        return
    else:
        contas.pop(indice) #Finalização. A tupla da conta é excluída.
        print("Conta excluída com sucesso.")
        return
