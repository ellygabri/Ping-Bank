# Função de apoio para buscar uma agência utilizando o número da agência
def buscar_agencia(agencias, num_agencia):
    for i in range(len(agencias)):
        if agencias[i]["num_agencia"] == num_agencia:
            return i
    return -1

# Função para cadastrar uma agência no sistema
def cadastrar_agencia(agencias, num_agencia, nome_agencia):
    # Verifica a existência de campos vazios
    if num_agencia.strip() == "" or nome_agencia.strip() == "":
        return -1
    # Verifica se a agência já existe
    indice = buscar_agencia(agencias, num_agencia)
    if indice != -1:
        return 0

    # Cria o dicionário referente à agência
    agencia = {"num_agencia": num_agencia,"nome_agencia": nome_agencia }

    # Adiciona o dicionário criado à lista de agências
    agencias.append(agencia)
    return 1

# Função para procurar apenas uma agência cadastrada no sistema
def procurar_agencia(agencias, num_agencia):
    indice = buscar_agencia(agencias, num_agencia)
    if indice == -1:
        return False
    return agencias[indice]

# Função para listar todas as agências cadastradas no sistema
def listar_agencias(agencias):
    if len(agencias) == 0:
        return False
    return agencias
