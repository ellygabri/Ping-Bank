def buscar_agencia(agencias, num_agencia):
    for agencia in agencias:
        if agencia[0] == num_agencia:
            return agencia
    return None

def cadastrar_agencia(agencias):
    num_agencia = input("informe o numero da agência: ")

    if buscar_agencia(agencias, num_agencia) != None:
        print("Agência já cadastrada!")
        return
    
    nome_agencia = input("Informe o nome da agência: ")

    agencia = [num_agencia, nome_agencia]
    agencias.append(agencia)

    print("Agência cadastrada com sucesso!")

def listar_agencias(agencias):
    if len(agencias) == 0:
        print("Nenhuma agência cadastrada!")
        return
    
    print("==== AGÊNCIAS ====")

    for agencia in agencias:
        print("Número: ", agencia[0])
        print("Nome: ", agencia[1])
        print("============================")
