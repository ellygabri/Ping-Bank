# Função de apoio, não precisa aparecer como opção no menu. Está sendo utilizada para evitar repetir a lógica de busca em todas as partes em que seriam necessárias.

def buscar_agencia(agencias, num_agencia):
    for i in range(len(agencias)):
        if agencias[i][0] == num_agencia:
            return i
    return -1
    
#Cadastrar Agência:  
  
def cadastrar_agencia(agencias, num_agencia, nome_agencia):
    if num_agencia.strip() == "" or nome_agencia.strip() == "":
        return False
    indice = buscar_agencia(agencias, num_agencia)
    if indice != -1:
        print("Agência já cadastrada!")
        return False
    agencia = (num_agencia, nome_agencia)
    return agencia
    
#Função para procurar apenas uma agência:    
    
def procurar_agencia (agencias, num_agencia):
    indice = buscar_agencia(agencias, num_agencia)
    if indice == -1:
        print("Agência não localizada!")
        return False
    agencia = agencias[indice]
    print("Número: ", agencia[0], "Nome: ", agencia[1])
    return True

#Listar todas as agências

def listar_agencias(agencias):
    if len(agencias) == 0:
        print("Nenhuma agência cadastrada!")
        return
    
    print("========== AGÊNCIAS ==========")

    for agencia in agencias:
        print("Número: ", agencia[0], "Nome: ", agencia[1])
    print("============================")
