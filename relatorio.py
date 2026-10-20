# Função para calcular o montante total de uma agência
from functools import reduce

def montante_agencia(contas, num_agencia):

    total = reduce(lambda acumulador, conta: acumulador + conta["saldo"],
                    (filter(lambda conta: conta["num_agencia"] == num_agencia, contas)), 0.0)
    return total

# Função para calcular o montante total do banco
def montante_banco(contas):
    total = reduce(lambda acumulador, conta: acumulador + conta["saldo"], contas, 0.0)
    return total

# Função para contar quantas contas existem em uma agência
def quantidade_contas_agencia(contas, num_agencia):
    
    quantidade = reduce(lambda acumulador, _: acumulador + 1,
                    (filter(lambda conta: conta["num_agencia"] == num_agencia, contas)), 0)

    return quantidade

# Função para calcular o montante de cada tipo de conta
def montante_tipo_conta(contas, tipo_conta):

    total = reduce(lambda acumulador, conta: acumulador + conta["saldo"],
                    (filter(lambda conta: conta["tipo_conta"] == tipo_conta, contas)), 0.0)

    return total

# Função para contar quantas contas existem de determinado tipo
def quantidade_tipo_conta(contas, tipo_conta):

    quantidade = reduce(lambda acumulador, _: acumulador + 1,
                    (filter(lambda conta: conta["tipo_conta"] == tipo_conta, contas)), 0)
    return quantidade

# Função para contar contas individuais e conjuntas
def quantidade_tipo_titulares(contas, tipo_titulares):

    quantidade = reduce(lambda acumulador, _: acumulador + 1,
                    (filter(lambda conta: conta["tipo_titulares"] == tipo_titulares, contas)), 0)

    return quantidade

# Função para gerar um resumo geral do banco
def resumo_bancario(clientes, agencias, contas):
    resumo = {
        "quantidade_clientes": len(clientes),
        "quantidade_agencias": len(agencias),
        "quantidade_contas": len(contas),

        "montante_total": montante_banco(contas),

        "quantidade_corrente": quantidade_tipo_conta(contas, 1),
        "quantidade_poupanca": quantidade_tipo_conta(contas, 2),
        "quantidade_salario": quantidade_tipo_conta(contas, 3),

        "montante_corrente": montante_tipo_conta(contas, 1),
        "montante_poupanca": montante_tipo_conta(contas, 2),
        "montante_salario": montante_tipo_conta(contas, 3),

        "quantidade_individuais": quantidade_tipo_titulares(contas, 1),
        "quantidade_conjuntas": quantidade_tipo_titulares(contas, 2)
    }
    return resumo

#Função para encontrar o menor saldo do banco.
def menor_saldo(contas): 

    if len(contas) == 0:
        return False
    menor_saldo = contas[0]["saldo"]
    for conta in contas:
        if conta["saldo"] < menor_saldo:
            conta_menor_saldo = conta

    return conta_menor_saldo

#Função para encontrar o maior saldo do banco.
def maior_saldo(contas): 

    if len(contas) == 0:
        return False
    maior_saldo = contas[0]["saldo"]
    for conta in contas:
        if conta["saldo"] > maior_saldo:
            conta_maior_saldo = conta

    return conta_maior_saldo