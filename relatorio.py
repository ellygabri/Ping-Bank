# Função para calcular o montante total de uma agência
def montante_agencia(contas, num_agencia):
    total = 0.0
    
    for conta in contas:
        if conta["num_agencia"] == num_agencia:
            total += conta["saldo"]
    return total

# Função para calcular o montante total do banco
def montante_banco(contas):
    total = 0.0

    for conta in contas:
        total += conta["saldo"]
    return total

# Função para contar quantas contas existem em uma agência
def quantidade_contas_agencia(contas, num_agencia):
    quantidade = 0

    for conta in contas:
        if conta["num_agencia"] == num_agencia:
            quantidade += 1

    return quantidade

# Função para calcular o montante de cada tipo de conta
def montante_tipo_conta(contas, tipo_conta):
    total = 0.0

    for conta in contas:
        if conta["tipo_conta"] == tipo_conta:
            total += conta["saldo"]
    return total

# Função para contar quantas contas existem de determinado tipo
def quantidade_tipo_conta(contas, tipo_conta):
    quantidade = 0

    for conta in contas:
        if conta["tipo_conta"] == tipo_conta:
            quantidade += 1
    return quantidade

# Função para contar contas individuais e conjuntas
def quantidade_tipo_titulares(contas, tipo_titulares):
    quantidade = 0

    for conta in contas:
        if conta["tipo_titulares"] == tipo_titulares:
            quantidade += 1
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
