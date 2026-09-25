# Função de apoio, não precisa aparecer como opção no menu. Está sendo utilizada para evitar repetir a lógica de busca em todas as partes em que seriam necessárias.

def buscar_agencia(agencias, num_agencia):
    for i in range(len(agencias)):
        if agencias[i][0] == num_agencia:
            return i
    return -1
    
#Cadastrar uma agência  
  
def cadastrar_agencia(agencias, num_agencia, nome_agencia):
    if num_agencia.strip() == "" or nome_agencia.strip() == "":
        return 0
    indice = buscar_agencia(agencias, num_agencia)
    if indice != -1:
        return 1
    agencia = (num_agencia, nome_agencia)
    return agencia
    
#Função para procurar apenas uma agência cadastrada 
    
def procurar_agencia (agencias, num_agencia):
    indice = buscar_agencia(agencias, num_agencia)
    if indice == -1:
        return False
    agencia = agencias[indice]
    return agencia

#Listar todas as agências do banco

def listar_agencias(agencias):
    if len(agencias) == 0:
        return False
    return agencias
