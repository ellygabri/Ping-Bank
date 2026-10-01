# A função de apoio, buscar_agencia, foi eliminada já que não será mais necessária.
 
#Cadastrar uma agência no sistema
def cadastrar_agencia(agencias, num_agencia, nome_agencia):
    #Verifica a existência de campos vazios
    if num_agencia.strip() == "" or nome_agencia.strip() == "":
        return -1
    #Verifica se a agência já existe
    if num_agencia in agencias:
        return 0
    agencias[num_agencia] = {"nome_agencia": nome_agencia}
    return 1

#Função para procurar apenas uma agência cadastrada no sistema
def procurar_agencia (agencias, num_agencia):
    if num_agencia not in agencias:
        return False
    #retorna o dicionário da agência encontrada
    return agencias[num_agencia]

#Listar todas as agências cadastradas no sistema
def listar_agencias(agencias):
    #Verifica se o dicionário de agências está vazio
    if not agencias:
        return False
    return agencias

