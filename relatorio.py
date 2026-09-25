def montante_agencia(contas, num_agencia):
    total = 0.0

    for conta in contas:
        if conta[1] == num_agencia:
            total = total + conta[3]
    return total

def montante_banco(contas):
    total = 0.0
    for conta in contas:
        total = total + conta[3]
    return total

def resumo_bancario(clientes, agencias, contas):
    quantidade_clientes = len(clientes)
    quantidade_agencias = len(agencias)
    quantidade_contas = len(contas)

    total_banco = montante_banco(contas)

    return(quantidade_clientes, quantidade_agencias, quantidade_contas, total_banco)
