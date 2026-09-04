from cliente import cadastrar_cliente
from conta import criar_conta_agencia, saque, consultar_saldo, deposito

#Cadastrar cliente
nome = input("Informe o seu nome completo: ")
cpf = input("informe o seu CPF: ")
contato = input("Informe o seu número de contato: ")
endereco = input("Informe o seu endereço atual: ")
data_nascimento = input("Informe a sua data de nascimento: ")
email = input("Informe o seu email: ") 

cliente = cadastrar_cliente(nome, cpf, contato, endereco, data_nascimento, email)

if cliente == False:
    print("Erro! Dados invalidos, tente novamente!")
else:
    print("Cliente cadastrado com sucesso!")
    print("Dados do cliente: ", cliente)

#Criar Conta
conta, agencia, saldo = criar_conta_agencia()
print("Conta criada!")
print("Número da conta: ",conta, "Número da Agência: ", agencia)
consultar_saldo(saldo)

#Deposito
valor_dep = float(input("Insira o valor a ser depositado: "))
novo_saldo = deposito(saldo, valor_dep)

if novo_saldo == False:
    print("Erro! Solicitação inválida")
else:
    saldo = novo_saldo
    print("Operação bem sucedida.")
    consultar_saldo(saldo)

#Saque
valor_saq = float(input("Insira o valor a ser sacado: "))
novo_saldo = saque(saldo, valor_saq)

if novo_saldo == False:
    print("Erro! SOlicitação inválida")
else:
    saldo = novo_saldo
    print("Operação bem sucedida.")
    consultar_saldo(saldo)
