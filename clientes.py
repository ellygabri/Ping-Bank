# Função de apoio para retirar pontos e traço do CPF
def normalizar_cpf(cpf):
    cpf_normalizado = ""
    for caractere in cpf:
        if caractere != "." and caractere != "-":
            cpf_normalizado = cpf_normalizado + caractere
    return cpf_normalizado

# Função de apoio para validar o CPF
def validar_cpf(cpf):
    cpf = normalizar_cpf(cpf)
    # Verificando se o CPF possui 11 digitos, como é o padrão
    if len(cpf) != 11:
        return False

    # Verificando se todos os caracteres são números
    numeros = "0123456789"
    for caractere in cpf:
        if caractere not in numeros:
            return False

    # Verificando se todos os números do CPF são iguais
    todos_iguais = True
    for i in range(1, len(cpf)):
        if cpf[i] != cpf[0]:
            todos_iguais = False
    if todos_iguais == True:
        return False

    # Cálculo do primeiro dígito verificador
    soma = 0
    peso = 10

    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11

    if resto < 2:
        primeiro_digito = 0
    else:
        primeiro_digito = 11 - resto

    if primeiro_digito != int(cpf[9]):
        return False

    # Cálculo do segundo dígito verificador
    soma = 0
    peso = 11

    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1

    resto = soma % 11

    if resto < 2:
        segundo_digito = 0
    else:
        segundo_digito = 11 - resto

    if segundo_digito != int(cpf[10]):
        return False

    return True

# Função de apoio para buscar um cliente utilizando o CPF
def buscar_cliente(clientes, cpf):
    cpf = normalizar_cpf(cpf)

    for i in range(len(clientes)):
        if clientes[i]["cpf"] == cpf:
            return i
    return -1

# Função para cadastrar um cliente no sistema do banco
def cadastrar_cliente(clientes, nome, cpf, contato, endereco, data_nascimento, email):
    # Verifica a existência de campos vazios
    if nome.strip() == "" or cpf.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
        return -1

    cpf = normalizar_cpf(cpf)

    if validar_cpf(cpf) == False:
        return -2
        
    # Verifica se o cliente já está cadastrado
    indice = buscar_cliente(clientes, cpf)

    if indice != -1:
        return 0

    # Cria o dicionário referente ao cliente
    cliente = {"nome": nome,"cpf": cpf,"contato": contato,"endereco": endereco,"data_nascimento": data_nascimento,"email": email}

    # Adiciona o dicionário criado à lista de clientes
    clientes.append(cliente)
    return 1

# Função para procurar apenas um cliente considerando o CPF
def procurar_cliente(clientes, cpf):
    indice = buscar_cliente(clientes, cpf)

    if indice == -1:
        return False
    return clientes[indice]

# Função utilizada para listar todos os clientes cadastrados
def listar_clientes(clientes):
    if len(clientes) == 0:
        return False
    return clientes

# Função para fazer alteração nos dados dos clientes,com exceção do CPF
def editar_cliente(clientes, cpf, campo, nova_info):
    indice = buscar_cliente(clientes, cpf)
    # Verifica se o cliente existe no sistema
    if indice == -1:
        return -1
    # Garante que o novo dado não seja vazio
    if nova_info.strip() == "":
        return 0

    # Verifica se o campo selecionado pode ser alterado
    if campo != "nome" and campo != "contato" and campo != "endereco" and campo != "data_nascimento" and campo != "email":
        return -2

    # Altera somente o campo escolhido
    clientes[indice][campo] = nova_info
    return 1
 
# Função para excluir um cliente, verificando antes se ele ainda possui uma conta no banco
def excluir_cliente(clientes, contas, cpf):
    cpf = normalizar_cpf(cpf)
    indice = buscar_cliente(clientes, cpf)

    if indice == -1:
        return -1

    # Verifica se o CPF ainda é titular de alguma conta
    for conta in contas:
        if cpf in conta["titulares"]:
            return 0
    # Exclui o cliente da lista
    del clientes[indice]
    return 1
