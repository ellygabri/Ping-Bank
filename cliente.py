
def buscar_cliente(clientes, cpf):
    for cliente in clientes:
        if cliente[1] == cpf:
            return cliente
        return None

def cadastrar_cliente(clientes):
    nome = input("Informe o nome: ")
    cpf = input("Informe o CPF: ")

    if buscar_cliente(clientes, cpf) != None:
        print("Cliente já cadastrado")
        return
    contato = input("Informe seu número para contato: ")
    endereco = input("Informe seu endereço: ")
    data_nascimento = input("Informe sua data de nascimento: ")
    email = input("Informe um e-mail válido: ")

    cliente = [nome, cpf, contato, endereco, data_nascimento, email]
    clientes.append(cliente)

    print("Cliente cadastrado com sucesso!")

def listar_clientes(clientes):
    if len(clientes) == 0:
        print("Não há clientes cadastrados!")
        return
    print("==== CLIENTES CADASTRADOS ====")

    for cliente in clientes:
        print("Nome: ", cliente[0])
        print("CPF: ", cliente[1])
        print("==============================")
