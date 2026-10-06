from clientes import buscar_cliente, normalizar_cpf
from agencias import buscar_agencia

def verificador_existencia(contas, num_conta, num_agencia): #Verifica a existência da conta e da agência no banco de dados.
    indice = 0
    for conta in contas:
        if conta["num_conta"] == num_conta and conta["num_agencia"] == num_agencia: #É de extrema importância alinhar os índices para garantir exatidão na checagem.
            return indice
        
        indice += 1
    return -1

def verificacao_seguranca(contas, indice, cpf): #Checagem de segurança (uma espécie de senha).
    cpf = normalizar_cpf(cpf)
 
    if cpf in contas[indice]["titulares"]:
        return 1
    return 0

def gerar_numero_conta(contas, num_agencia):

    agencia = filter(lambda conta: conta["num_agencia"] == num_agencia, contas)
    maior_numero = max(map(lambda conta: int(conta["num_conta"]), agencia), default = 0)

    return maior_numero + 1


def criar_conta(contas, clientes, agencias, num_agencia, tipo_titulares, saldo, titulares, tipo_conta): #Criação da conta e adição dos dados relacionados. 

    indice_agencia = buscar_agencia(agencias, num_agencia)

    if indice_agencia == -1:
        return -1
    if tipo_titulares != 1 and tipo_titulares != 2:
        return -2
    if saldo < 0:
        return -3
    if tipo_titulares == 1 and len(titulares) != 1:
        return -4
    elif tipo_titulares == 2 and len(titulares) < 2:
        return -4
    if tipo_conta != 1 and tipo_conta != 2 and tipo_conta != 3:
        return -6

    titulares_normalizados = []

    for cpf in titulares:

        cpf = normalizar_cpf(cpf)

        if buscar_cliente(clientes, cpf) == -1:
            return -5
        if cpf in titulares_normalizados:
            return -7

        titulares_normalizados.append(cpf)


    num_conta = gerar_numero_conta(contas, num_agencia)

    conta = {"num_conta": num_conta,"num_agencia": num_agencia,"tipo_titulares": tipo_titulares,"saldo": saldo,"titulares": titulares_normalizados,"tipo_conta": tipo_conta}

    return conta 
                            

def procurar_conta(contas, num_conta, num_agencia, cpf):

    indice = verificador_existencia(contas, num_conta, num_agencia)

    if indice == -1:
        return False
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2
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
    if contas[indice]["tipo_conta"] == 3:
        return -4

    contas[indice]["saldo"] += valor_deposito
    
    return 1

def saque(contas, num_conta, num_agencia, cpf, valor_saque): #Diminui o saldo da conta com o valor do saque.

    indice = verificador_existencia(contas, num_conta, num_agencia)

    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2
    if valor_saque <= 0:
        return 0
    if valor_saque > contas[indice]["saldo"]:
        return -3

    contas[indice]["saldo"] -= valor_saque

    return 1

def consultar_saldo(contas, num_conta, num_agencia, cpf): #Consulta o saldo da conta.

    indice = verificador_existencia(contas, num_conta, num_agencia)

    if indice == -1:
        return -1
    if verificacao_seguranca(contas, indice, cpf) != 1:
        return -2

    return contas[indice]["saldo"]

def transferencia(contas, conta_origem, agencia_origem, cpf, conta_destino, agencia_destino, valor): #Função para realizar a operação de transferência entre contas

    indice_origem = verificador_existencia(contas, conta_origem, agencia_origem)

    if indice_origem == -1:
        return -1
    if verificacao_seguranca(contas, indice_origem, cpf) != 1:
        return -2

    indice_destino = verificador_existencia( contas, conta_destino, agencia_destino )

    if indice_destino == -1:
        return -3
    if conta_origem == conta_destino and agencia_origem == agencia_destino:
        return -4
    if valor <= 0:
        return 0
    if contas[indice_origem]["tipo_conta"] == 3:
        return -6
    if valor > contas[indice_origem]["saldo"]:
        return -5

    contas[indice_origem]["saldo"] -= valor
    contas[indice_destino]["saldo"] += valor

    return 1

def listar_contas_clientes(contas, cpf): #Listar todas as contas associadas ao cliente

    cpf = normalizar_cpf(cpf)

    contas_cliente = list(filter(lambda conta: cpf in conta["titulares"], contas))

    if len(contas_cliente) == 0:
        return False

    return contas_cliente

def listar_titulares(contas, num_conta, num_agencia): #Listar todos os clientes associados a conta

    indice = verificador_existencia(contas, num_conta, num_agencia )

    if indice == -1:
        return False

    return contas[indice]["titulares"]

def adicionar_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, novo_titular): #Função para adicionar um cliente a uma conta

    indice = verificador_existencia( contas,num_conta,num_agencia)

    if indice == -1:
        return -1

    if verificacao_seguranca(contas,indice, cpf_validacao) != 1:
        return -2

    novo_titular = normalizar_cpf(novo_titular)

    if buscar_cliente(clientes, novo_titular) == -1:
        return -3

    if novo_titular in contas[indice]["titulares"]:
        return 0

    contas[indice]["titulares"].append(novo_titular)

    if len(contas[indice]["titulares"]) > 1:
        contas[indice]["tipo_titulares"] = 2

    return 1

def remover_titular(contas, num_conta, num_agencia, cpf_validacao, titular_removido):

    indice = verificador_existencia(contas,num_conta, num_agencia)

    if indice == -1:
        return -1

    if verificacao_seguranca(contas,indice, cpf_validacao) != 1:
        return -2

    titular_removido = normalizar_cpf(titular_removido)
    titulares = contas[indice]["titulares"]

    if titular_removido not in titulares:
        return 0

    if len(titulares) == 1:
        return -3

    for i in range(len(titulares)):
        if titulares[i] == titular_removido:
            del titulares[i]
            if len(titulares) == 1:
                contas[indice]["tipo_titulares"] = 1
            return 1

def substituir_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, titular_antigo, novo_titular): #Utilizado Para substituir um titular na conta

    indice = verificador_existencia(contas, num_conta,num_agencia)

    if indice == -1:
        return -1
    if verificacao_seguranca(contas,indice,cpf_validacao) != 1:
        return -2

    titular_antigo = normalizar_cpf(titular_antigo)
    novo_titular = normalizar_cpf(novo_titular)

    if buscar_cliente(clientes, novo_titular) == -1:
        return -3

    if novo_titular in contas[indice]["titulares"]:
        return -4

    titulares = contas[indice]["titulares"]
    for i in range(len(titulares)):
        if titulares[i] == titular_antigo:
            titulares[i] = novo_titular
            return 1

    return 0


def excluir_conta(contas,num_conta,num_agencia,cpf): #Função utilizada para excluir uma conta cadastrada

    indice = verificador_existencia(contas,num_conta,num_agencia)

    if indice == -1:
        return -1

    if verificacao_seguranca(contas,indice,cpf) != 1:
        return -2

    if contas[indice]["saldo"] != 0:
        return 0

    del contas[indice]

    return 1

def calculo_poupanca(num_conta, num_agencia, contas, meses_decorridos): #Função para calcular o rendimento da poupança

    indice = verificador_existencia(contas,num_conta,num_agencia)

    if indice == -1:
        return -1

    if contas[indice]["tipo_conta"] != 2:
        return -2

    if meses_decorridos <= 0:
        return -3

    rendimento = contas[indice]["saldo"] * 0.005 * meses_decorridos
    novo_saldo = contas[indice]["saldo"] + rendimento
    contas[indice]["saldo"] = novo_saldo

    return novo_saldo
