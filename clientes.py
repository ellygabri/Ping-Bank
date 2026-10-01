# A função de apoio, buscar_clientes, foi eliminada já que não será mais necessária.
 
#Cadastrar um cliente no sistema do banco
def cadastrar_cliente(clientes,nome, cpf, contato, endereco, data_nascimento, email):
    #Verifica a existência de espaços vazios
    if nome.strip() == "" or cpf.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
        return -1
    #Verifica se o cliente já está cadastrado
    if cpf in clientes:
        return 0
    #Armazenando os dados como um dicinário dentro do dicionário principal
    clientes[cpf] = { "nome": nome, "contato": contato, "endereco": endereco, "data_nascimento": data_nascimento, "email": email}
    return 1


#Procurar um cliente cadastrado no sistema (verificando a existência do cliente, utilizando o cpf, em clientes)
def procurar_cliente(clientes, cpf):
   if cpf not in clientes:
       return False
   #Retorna o dicionário referente ao cliente encontrado
   return clientes[cpf]

#Listar todos os clientes cadastrados no sistema
def listar_clientes(clientes):
    if len(clientes) == 0:
        return False
    return clientes
    
#Editar informações de um cliente
def editar_cliente(clientes, nome, cpf, contato, endereco, data_nascimento, email):

    if cpf not in clientes:
        return -1
    #Verifica a existência de espaços vazios
    if nome.strip() == "" or cpf.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
        return 0
    #Armazenando os dados como um dicinário dentro do dicionário principal
    clientes[cpf] = { "nome": nome, "contato": contato, "endereco": endereco, "data_nascimento": data_nascimento, "email": email}
    return 1
    

#Excluir clientes | Um cliente não deve ser excluido se ainda for titular de uma conta
def excluir_cliente(clientes, contas, cpf):

    if cpf not in clientes:
        return -1
    #Alteração para verificar se o cpf é titular de uma conta
    for numero_conta, dados_conta in contas.items():
        if cpf in dados_conta["titulares"]:
            return 0
    del clientes[cpf]
    return 1

""" 
Ainda não recebi os dados respectivos sobre contas. Assim que sejam fornecidos, edito o que for necessário.
"""
