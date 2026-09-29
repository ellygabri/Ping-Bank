from cliente import buscar_cliente
from agencia import buscar_agencia

def verificador_existencia(contas, num_conta, num_agencia): #Verifica a existência da conta e da agência no banco de dados.

    for i in range(len(contas)): #Navega por toda a lista a fim de constatar a existência dos dados.
        if contas[i][0] == num_conta and contas[i][1] == num_agencia: #É de extrema importância alinhar os índices para garantir exatidão na checagem.
            return i
    return -1

def verificacao_seguranca(contas, indice, cpf): #Checagem de segurança (uma espécie de senha).
    titulares = contas[indice][4]

    for titular in titulares: 
        if titular == cpf:
            return 1
    return 0

def gerar_numero_conta(contas, num_agencia):

    maior_numero = 0

    for conta in contas:

        if conta[1] == num_agencia:

            if conta[0] > maior_numero:

                maior_numero = conta[0]

    return maior_numero + 1

def criar_conta(contas, clientes, agencias, num_agencia, tipo_conta, saldo, titulares): #Criação da conta e adição dos dados relacionados.   
    indice_agencia = buscar_agencia(agencias, num_agencia)
    if indice_agencia == -1:
        return -1
    if tipo_conta != 1 and tipo_conta != 2:
        return -2
    if saldo < 0:
        return -3
    if tipo_conta == 1 and len(titulares) != 1:
        return -4
    for i in range(len(titulares)):
        cpf = titulares[i]
        if buscar_cliente(clientes, cpf) == -1:
            return -5
        for j in range(i+1, len(titulares)):
            if titulares[i] == titulares[j]:
                return -6
    num_conta = gerar_numero_conta(contas, num_agencia)
    conta = (num_conta, num_agencia, tipo_conta, saldo, titulares)

    return conta

def procurar_conta(contas, num_conta, num_agencia):
    indice = verificador_existencia(contas, num_conta, num_agencia)
    if indice == -1:
        return False
    return contas[indice]

def listar_contas(contas):
    if len(contas) == 0:
        return False
    return contas

def deposito(contas, num_conta, num_agencia, cpf, valor_deposito): #Aumenta o saldo da conta com o valor do depósito.
    indice = verificador_existencia(contas, num_conta, num_agencia)
    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2
    if valor_deposito <= 0:
        return 0
    conta = contas[indice]
    novo_saldo = (conta[3] + valor_deposito)

    contas[indice] = (conta[0], conta[1], conta[2], novo_saldo, conta[4])
    return 1

def saque(contas, num_conta, num_agencia, cpf, valor_saque): #Diminui o saldo da conta com o valor do saque.
    indice = verificador_existencia(contas, num_conta, num_agencia)

    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2
    if valor_saque <= 0:
        return 0
    conta = contas[indice]

    if valor_saque > conta[3]:
        return -3
    novo_saldo = (conta[3] - valor_saque)

    contas[indice] = (conta[0], conta[1], conta[2], novo_saldo, conta[4])
    return 1

def consultar_saldo(contas, num_conta, num_agencia, cpf): #Consulta o saldo da conta.

    indice = verificador_existencia(contas, num_conta, num_agencia)
    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2
    return contas[indice][3]

def tranferencia(contas, conta_origem, agencia_origem, cpf, conta_destino, agencia_destino, valor): #Função para realizar a operação de transferência entre contas
    indice_origem = verificador_existencia(contas, conta_origem, agencia_origem)
    if indice_origem == -1:
        return -1
    if verificacao_seguranca(contas, indice_origem, cpf) != 1:
        return -2
    indice_destino = verificador_existencia(contas, conta_destino, agencia_destino)
    if indice_destino == -1:
        return -3
    if conta_origem == conta_destino and agencia_origem == agencia_destino:
        return -4
    if valor <= 0:
        return 0
    origem = contas[indice_origem]
    destino = contas[indice_destino]

    if valor > origem[3]:
        return -5
    contas[indice_origem] = (origem[0], origem[1], origem[2], origem[3] - valor, origem[4])
    contas[indice_destino] = (destino[0], destino[1], destino[2], destino[3]+valor, destino[4])
    return 1

def listar_contas_clientes(contas, cpf): #Listar todas as contas associadas ao cliente
    contas_cliente = []

    for conta in contas:
        titulares = conta[4]
        for titular in titulares:
            if titular == cpf:
                contas_cliente.append(conta)
    if len(contas_cliente) == 0:
        return False
    return contas_cliente

def listar_titulares(contas, num_conta, num_agencia): #Listar todos os clientes associados a conta
    indice = verificador_existencia(contas, num_conta, num_agencia)
    if indice == -1:
        return False
    return contas[indice][4]
def adicionar_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, novo_titular): #Função para adicionar um cliente a uma conta
    indice = verificador_existencia(contas, num_conta, num_agencia)
    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf_validacao) != 1:
        return -2
    if buscar_cliente(clientes, novo_titular) == -1:
        return -3
    conta = contas[indice]
    titulares = conta[4]

    for titular in titulares:
        if titular == novo_titular:
            return 0
    novos_titulares = titulares + (novo_titular,)

    contas[indice] = (conta[0], conta[1], 2, conta[3], novos_titulares)
    return 1

def substituir_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, titular_antigo, novo_titular): #Utilizado Para substituir um titular na conta

    indice = verificador_existencia(contas,num_conta,num_agencia)

    if indice == -1:
        return -1

    if verificacao_seguranca(contas,indice,cpf_validacao) != 1:
        return -2

    if buscar_cliente(clientes,novo_titular) == -1:
        return -3

    conta = contas[indice]
    titulares = conta[4]

    for titular in titulares:
        if titular == novo_titular:
            return -4
    encontrado = False
    novos_titulares = ()

    for titular in titulares:
        if titular == titular_antigo:
            novos_titulares = (novos_titulares + (novo_titular,))
            encontrado = True

        else:
            novos_titulares = (novos_titulares + (titular,))

    if encontrado == False:
        return 0

    contas[indice] = (conta[0],conta[1],conta[2],conta[3],novos_titulares)
    return 1

def excluir_conta(contas,num_conta,num_agencia,cpf): #Função utilizada para excluir uma conta cadastrada
    indice = verificador_existencia(contas,num_conta,num_agencia)

    if indice == -1:
        return -1

    if verificacao_seguranca(contas,indice,cpf) != 1:
        return -2

    conta = contas[indice]

    if conta[3] != 0:
        return 0

    del contas[indice]
    return 1
