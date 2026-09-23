# Função de apoio, não precisa aparecer como opção no menu. Está sendo utilizada para evitar repetir a lógica de busca em todas as partes em que seriam necessárias.

def buscar_cliente(clientes, cpf):
    for i in range(len(clientes)):
        if clientes[i][1] == cpf:
            return i
    return -1

#Cadastrar um cliente

def cadastrar_cliente(nome, cpf, contato, endereco, data_nascimento, email):
    if nome.strip() == "" or cpf.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
        return False
    return (nome, cpf, contato, endereco, data_nascimento, email)

#Procurar um cliente

def procurar_cliente(clientes, cpf):
    indice = buscar_cliente(clientes, cpf)

    if indice == -1:
        print("Cliente não encontrado!")
        return False
    cliente = clientes[indice]
    print("Nome: ", cliente[0], "CPF: ", cliente[1], "Contato: ", cliente[2], "Endereço: ", cliente[3], "Data de nascimento: ", cliente[4], "E-mail: ", cliente[5])
    return True

#Listar todos os clientes cadastrados

def listar_clientes(clientes):
    if len(clientes) == 0:
        print("Nenhum cliente cadastrado!")
        return
    print("========== CLIENTES ==========")
    for cliente in clientes:
        print("Nome: ", cliente[0], "CPF: ", cliente[1], "Contato: ", cliente[2], "Endereço: ", cliente[3], "Data de nascimento: ", cliente[4], "E-mail: ", cliente[5])
    print("========== FIM! ==========")

#Editar informações de um cliente

def editar_cliente(clientes, nome, cpf, contato, endereco, data_nascimento, email):
    
    indice = buscar_cliente(clientes, cpf)

    if indice == -1:
        print("Cliente não encontrado!")
        return False
    cliente_editado = cadastrar_cliente(nome, cpf, contato, endereco, data_nascimento, email)
    if cliente_editado == False:
        print("Dados Inválidos!")
        return False
    clientes[indice] = cliente_editado
    print("Cliente editado com sucesso!")
    return True

#Falta a função Excluir_conta.
