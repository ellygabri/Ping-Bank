import json

from clientes import cadastrar_cliente, procurar_cliente, listar_clientes, editar_cliente, excluir_cliente

from agencias import buscar_agencia, cadastrar_agencia, procurar_agencia, listar_agencias

from contas import criar_conta, procurar_conta, listar_contas, deposito, saque, consultar_saldo, transferencia, listar_contas_clientes, listar_titulares, adicionar_titular, remover_titular, substituir_titular, excluir_conta, calculo_poupanca

from relatorio import montante_agencia, quantidade_contas_agencia, resumo_bancario

# Função para carregar os dados armazenados no JSON
def carregar_dados():

    arquivo = open(
        "ping_bank_dados.json",
        "r",
        encoding="utf-8"
    )

    dados = json.load(arquivo)

    arquivo.close()

    clientes = dados["clientes"]
    agencias = dados["agencias"]
    contas = dados["contas"]

    return clientes, agencias, contas

# Função para salvar os dados no JSON
def salvar_dados(clientes, agencias, contas):

    dados = {
        "clientes": clientes,
        "agencias": agencias,
        "contas": contas
    }

    arquivo = open(
        "ping_bank_dados.json",
        "w",
        encoding="utf-8"
    )

    json.dump(
        dados,
        arquivo,
        ensure_ascii=False,
        indent=4
    )

    arquivo.close()

# Confere os caracteres antes de converter a entrada para inteiro.
def ler_inteiro(mensagem):
    valido = False

    while valido == False:
        entrada = input(mensagem).strip()
        valido = True
        quantidade_digitos = 0

        for i in range(len(entrada)):
            if entrada[i] in "0123456789":
                quantidade_digitos += 1
            elif i == 0 and (entrada[i] == "-" or entrada[i] == "+"):
                valido = True
            else:
                valido = False

        if quantidade_digitos == 0:
            valido = False

        if valido == False:
            print("Entrada inválida. Digite um número inteiro.")

    return int(entrada)

# Aceita um separador decimal, ponto ou virgula, e exige algum digito.
def ler_valor(mensagem):
    valido = False

    while valido == False:
        entrada = input(mensagem).strip()
        numero = ""
        quantidade_digitos = 0
        quantidade_separadores = 0
        valido = True

        for i in range(len(entrada)):
            if entrada[i] in "0123456789":
                numero = numero + entrada[i]
                quantidade_digitos += 1
            elif entrada[i] == "." or entrada[i] == ",":
                numero = numero + "."
                quantidade_separadores += 1
            elif i == 0 and (entrada[i] == "-" or entrada[i] == "+"):
                numero = numero + entrada[i]
            else:
                valido = False

        if quantidade_digitos == 0 or quantidade_separadores > 1:
            valido = False

        if valido == False:
            print("Entrada inválida. Digite um valor numérico.")

    return float(numero)

# Função utilizada apenas para mostrar os dados de um cliente
def exibir_cliente(cliente):

    print("Nome:", cliente["nome"])
    print("CPF:", cliente["cpf"])
    print("Contato:", cliente["contato"])
    print("Endereço:", cliente["endereco"])
    print("Data de nascimento:", cliente["data_nascimento"])
    print("E-mail:", cliente["email"])

# Função utilizada apenas para mostrar os dados de uma agência
def exibir_agencia(agencia):

    print("Número da agência:", agencia["num_agencia"])
    print("Nome da agência:", agencia["nome_agencia"])

# Função para identificar o tipo da conta
def nome_tipo_conta(tipo_conta):

    if tipo_conta == 1:
        return "Corrente"

    elif tipo_conta == 2:
        return "Poupança"

    elif tipo_conta == 3:
        return "Salário"

    return "Tipo inválido"

# Função para identificar se a conta é individual ou conjunta
def nome_tipo_titulares(tipo_titulares):

    if tipo_titulares == 1:
        return "Individual"

    elif tipo_titulares == 2:
        return "Conjunta"

    return "Tipo inválido"

# Função utilizada apenas para mostrar os dados de uma conta
def exibir_conta(conta):

    print("Número da conta:", conta["num_conta"])
    print("Agência:", conta["num_agencia"])
    print("Tipo da conta:", nome_tipo_conta(conta["tipo_conta"]))
    print(
        "Titularidade:",
        nome_tipo_titulares(conta["tipo_titulares"])
    )
    print("Saldo: R$", conta["saldo"])

    print("Titulares:")

    for cpf in conta["titulares"]:
        print("-", cpf)

# Menu referente aos clientes
def menu_clientes(clientes, contas):

    opcao = ""

    while opcao != "0":

        print("========== CLIENTES ==========")
        print("1 - Cadastrar cliente")
        print("2 - Procurar cliente")
        print("3 - Listar clientes")
        print("4 - Editar cliente")
        print("5 - Excluir cliente")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            nome = input("Nome: ")
            cpf = input("CPF: ")
            contato = input("Contato: ")
            endereco = input("Endereço: ")
            data_nascimento = input("Data de nascimento: ")
            email = input("E-mail: ")
            
            resultado = cadastrar_cliente(
                clientes,
                nome,
                cpf,
                contato,
                endereco,
                data_nascimento,
                email
            )

            if resultado == -2:
                print("CPF inválido.")

            elif resultado == -1:
                print("Existem campos vazios.")

            elif resultado == 0:
                print("Já existe um cliente com esse CPF.")

            elif resultado == 1:
                print("Cliente cadastrado com sucesso.")

        elif opcao == "2":

            cpf = input("CPF do cliente: ")

            cliente = procurar_cliente(
                clientes,
                cpf
            )

            if cliente == False:
                print("Cliente não encontrado.")

            else:
                exibir_cliente(cliente)

        elif opcao == "3":

            resultado = listar_clientes(clientes)

            if resultado == False:
                print("Nenhum cliente cadastrado.")

            else:

                for cliente in resultado:

                    print("------------------------------")
                    exibir_cliente(cliente)

        elif opcao == "4":

            cpf = input("CPF do cliente: ")

            print("1 - Nome")
            print("2 - Contato")
            print("3 - Endereço")
            print("4 - Data de nascimento")
            print("5 - E-mail")

            campo_escolhido = input(
                "Qual informação deseja alterar? "
            )

            campo = ""

            if campo_escolhido == "1":
                campo = "nome"

            elif campo_escolhido == "2":
                campo = "contato"

            elif campo_escolhido == "3":
                campo = "endereco"

            elif campo_escolhido == "4":
                campo = "data_nascimento"

            elif campo_escolhido == "5":
                campo = "email"

            if campo == "":
                print("Campo inválido.")

            else:

                nova_info = input(
                    "Digite a nova informação: "
                )

                resultado = editar_cliente(
                    clientes,
                    cpf,
                    campo,
                    nova_info
                )

                if resultado == -2:
                    print("Campo inválido.")

                elif resultado == -1:
                    print("Cliente não encontrado.")

                elif resultado == 0:
                    print("A nova informação não pode ser vazia.")

                elif resultado == 1:
                    print("Cliente alterado com sucesso.")

        elif opcao == "5":

            cpf = input("CPF do cliente: ")

            resultado = excluir_cliente(
                clientes,
                contas,
                cpf
            )

            if resultado == -1:
                print("Cliente não encontrado.")

            elif resultado == 0:
                print(
                    "O cliente ainda é titular de uma conta."
                )

            elif resultado == 1:
                print("Cliente excluído com sucesso.")


        elif opcao != "0":

            print("Opção inválida.")

# Menu referente às agências
def menu_agencias(agencias):

    opcao = ""

    while opcao != "0":

        print("========== AGÊNCIAS ==========")
        print("1 - Cadastrar agência")
        print("2 - Procurar agência")
        print("3 - Listar agências")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            num_agencia = input(
                "Número da agência: "
            )

            nome_agencia = input(
                "Nome da agência: "
            )

            resultado = cadastrar_agencia(
                agencias,
                num_agencia,
                nome_agencia
            )

            if resultado == -1:
                print("Existem campos vazios.")

            elif resultado == 0:
                print("Agência já cadastrada.")

            elif resultado == 1:
                print("Agência cadastrada com sucesso.")


        elif opcao == "2":

            num_agencia = input(
                "Número da agência: "
            )

            agencia = procurar_agencia(
                agencias,
                num_agencia
            )

            if agencia == False:
                print("Agência não encontrada.")

            else:
                exibir_agencia(agencia)


        elif opcao == "3":

            resultado = listar_agencias(agencias)

            if resultado == False:
                print("Nenhuma agência cadastrada.")

            else:

                for agencia in resultado:

                    print("------------------------------")
                    exibir_agencia(agencia)

        elif opcao != "0":

            print("Opção inválida.")

# Menu referente às contas
def menu_contas(clientes, agencias, contas):

    opcao = ""

    while opcao != "0":

        print("========== CONTAS ==========")
        print("1 - Criar conta")
        print("2 - Procurar conta")
        print("3 - Listar contas")
        print("4 - Listar contas de um cliente")
        print("5 - Listar titulares")
        print("6 - Adicionar titular")
        print("7 - Remover titular")
        print("8 - Substituir titular")
        print("9 - Excluir conta")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            num_agencia = input(
                "Número da agência: "
            )

            print("1 - Conta individual")
            print("2 - Conta conjunta")

            tipo_titulares = ler_inteiro("Tipo de titularidade: ")

            titulares = []

            if tipo_titulares == 1:

                cpf = input(
                    "CPF do titular: "
                )

                titulares.append(cpf)


            elif tipo_titulares == 2:

                quantidade = ler_inteiro("Quantidade de titulares: ")

                i = 0

                while i < quantidade:

                    cpf = input(
                        "CPF do titular: "
                    )

                    titulares.append(cpf)

                    i += 1

            saldo = ler_valor("Saldo inicial: R$ ")

            print("1 - Conta corrente")
            print("2 - Conta poupança")
            print("3 - Conta salário")

            tipo_conta = ler_inteiro("Tipo da conta: ")

            resultado = criar_conta(
                contas,
                clientes,
                agencias,
                num_agencia,
                tipo_titulares,
                saldo,
                titulares,
                tipo_conta
            )

            if resultado == -1:
                print("Agência não encontrada.")

            elif resultado == -2:
                print("Tipo de titularidade inválido.")

            elif resultado == -3:
                print("Saldo inicial inválido.")

            elif resultado == -4:
                print(
                    "Quantidade de titulares inválida."
                )

            elif resultado == -5:
                print(
                    "Um dos titulares não está cadastrado."
                )

            elif resultado == -6:
                print("Tipo de conta inválido.")

            elif resultado == -7:
                print("Existem titulares repetidos.")

            else:

                contas.append(resultado)

                print("Conta criada com sucesso.")
                print(
                    "Número da conta:",
                    resultado["num_conta"]
                )

        elif opcao == "2":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf = input(
                "CPF de um titular: "
            )

            resultado = procurar_conta(
                contas,
                num_conta,
                num_agencia,
                cpf
            )

            if resultado == False:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            else:
                exibir_conta(resultado)

        elif opcao == "3":

            resultado = listar_contas(contas)

            if resultado == False:
                print("Nenhuma conta cadastrada.")

            else:

                for conta in resultado:

                    print("------------------------------")
                    exibir_conta(conta)


        elif opcao == "4":

            cpf = input(
                "CPF do cliente: "
            )

            resultado = listar_contas_clientes(
                contas,
                cpf
            )

            if resultado == False:
                print(
                    "O cliente não possui contas."
                )

            else:

                for conta in resultado:

                    print("------------------------------")
                    exibir_conta(conta)


        elif opcao == "5":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            resultado = listar_titulares(
                contas,
                num_conta,
                num_agencia
            )

            if resultado == False:
                print("Conta não encontrada.")

            else:

                print("Titulares:")

                for cpf in resultado:
                    print("-", cpf)

        elif opcao == "6":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf_validacao = input(
                "CPF de um titular atual: "
            )

            novo_titular = input(
                "CPF do novo titular: "
            )

            resultado = adicionar_titular(
                contas,
                clientes,
                num_conta,
                num_agencia,
                cpf_validacao,
                novo_titular
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -3:
                print("Novo titular não cadastrado.")

            elif resultado == 0:
                print(
                    "Esse cliente já é titular da conta."
                )

            elif resultado == 1:
                print(
                    "Titular adicionado com sucesso."
                )

        elif opcao == "7":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf_validacao = input(
                "CPF de um titular atual: "
            )

            titular_removido = input(
                "CPF do titular que será removido: "
            )

            resultado = remover_titular(
                contas,
                num_conta,
                num_agencia,
                cpf_validacao,
                titular_removido
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -3:
                print(
                    "A conta não pode ficar sem titular."
                )

            elif resultado == 0:
                print(
                    "O CPF informado não é titular da conta."
                )

            elif resultado == 1:
                print(
                    "Titular removido com sucesso."
                )

        elif opcao == "8":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf_validacao = input(
                "CPF de um titular atual: "
            )

            titular_antigo = input(
                "CPF que será substituído: "
            )

            novo_titular = input(
                "CPF do novo titular: "
            )

            resultado = substituir_titular(
                contas,
                clientes,
                num_conta,
                num_agencia,
                cpf_validacao,
                titular_antigo,
                novo_titular
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -3:
                print(
                    "Novo titular não cadastrado."
                )

            elif resultado == -4:
                print(
                    "O novo cliente já é titular."
                )

            elif resultado == 0:
                print(
                    "Titular antigo não encontrado."
                )

            elif resultado == 1:
                print(
                    "Titular substituído com sucesso."
                )

        elif opcao == "9":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf = input(
                "CPF de um titular: "
            )

            resultado = excluir_conta(
                contas,
                num_conta,
                num_agencia,
                cpf
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == 0:
                print(
                    "A conta precisa estar com saldo zero."
                )

            elif resultado == 1:
                print("Conta excluída com sucesso.")

        elif opcao != "0":

            print("Opção inválida.")

# Menu referente às operações bancárias
def menu_operacoes(contas):

    opcao = ""

    while opcao != "0":

        print("========== OPERAÇÕES ==========")
        print("1 - Consultar saldo")
        print("2 - Depositar")
        print("3 - Sacar")
        print("4 - Transferir")
        print("5 - Aplicar rendimento da poupança")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf = input(
                "CPF de um titular: "
            )

            resultado = consultar_saldo(
                contas,
                num_conta,
                num_agencia,
                cpf
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            else:
                print("Saldo atual: R$", resultado)

        elif opcao == "2":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf = input(
                "CPF de um titular: "
            )

            valor = ler_valor("Valor do depósito: R$ ")

            resultado = deposito(
                contas,
                num_conta,
                num_agencia,
                cpf,
                valor
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -4:
                print(
                    "Conta salário não permite essa operação."
                )

            elif resultado == 0:
                print("Valor inválido.")

            elif resultado == 1:
                print("Depósito realizado com sucesso.")

        elif opcao == "3":

            num_conta = ler_inteiro("Número da conta: ")

            num_agencia = input(
                "Número da agência: "
            )

            cpf = input(
                "CPF de um titular: "
            )

            valor = ler_valor("Valor do saque: R$ ")

            resultado = saque(
                contas,
                num_conta,
                num_agencia,
                cpf,
                valor
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -3:
                print("Saldo insuficiente.")

            elif resultado == 0:
                print("Valor inválido.")

            elif resultado == 1:
                print("Saque realizado com sucesso.")

        elif opcao == "4":

            conta_origem = ler_inteiro("Conta de origem: ")

            agencia_origem = input(
                "Agência de origem: "
            )

            cpf = input(
                "CPF de um titular da conta de origem: "
            )

            conta_destino = ler_inteiro("Conta de destino: ")

            agencia_destino = input(
                "Agência de destino: "
            )

            valor = ler_valor("Valor da transferência: R$ ")

            resultado = transferencia(
                contas,
                conta_origem,
                agencia_origem,
                cpf,
                conta_destino,
                agencia_destino,
                valor
            )

            if resultado == -1:
                print(
                    "Conta de origem não encontrada."
                )

            elif resultado == -2:
                print("CPF não autorizado.")

            elif resultado == -3:
                print(
                    "Conta de destino não encontrada."
                )

            elif resultado == -4:
                print(
                    "A conta de origem e destino são iguais."
                )

            elif resultado == -5:
                print("Saldo insuficiente.")

            elif resultado == -6:
                print(
                    "Conta salário não permite essa operação."
                )

            elif resultado == 0:
                print("Valor inválido.")

            elif resultado == 1:
                print(
                    "Transferência realizada com sucesso."
                )

        elif opcao == "5":

            num_conta = ler_inteiro("Número da conta poupança: ")

            num_agencia = input(
                "Número da agência: "
            )

            meses_decorridos = ler_inteiro("Quantidade de meses decorridos: ")

            resultado = calculo_poupanca(
                num_conta,
                num_agencia,
                contas,
                meses_decorridos
            )

            if resultado == -1:
                print("Conta não encontrada.")

            elif resultado == -2:
                print(
                    "A conta informada não é poupança."
                )

            elif resultado == -3:
                print(
                    "Quantidade de meses inválida."
                )

            else:
                print(
                    "Novo saldo da poupança: R$",
                    resultado
                )

        elif opcao != "0":

            print("Opção inválida.")

# Menu referente aos relatórios
def menu_relatorios(clientes, agencias, contas):

    opcao = ""

    while opcao != "0":

        print("========== RELATÓRIOS ==========")
        print("1 - Relatório de uma agência")
        print("2 - Relatório geral do banco")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            num_agencia = input(
                "Número da agência: "
            )

            indice = buscar_agencia(
                agencias,
                num_agencia
            )

            if indice == -1:
                print("Agência não encontrada.")

            else:

                quantidade = quantidade_contas_agencia(
                    contas,
                    num_agencia
                )

                total = montante_agencia(
                    contas,
                    num_agencia
                )

                print(
                    "Agência:",
                    num_agencia
                )

                print(
                    "Quantidade de contas:",
                    quantidade
                )

                print(
                    "Montante da agência: R$",
                    total
                )

        elif opcao == "2":

            resumo = resumo_bancario(
                clientes,
                agencias,
                contas
            )

            print(
                "Clientes cadastrados:",
                resumo["quantidade_clientes"]
            )

            print(
                "Agências cadastradas:",
                resumo["quantidade_agencias"]
            )

            print(
                "Contas cadastradas:",
                resumo["quantidade_contas"]
            )

            print(
                "Montante total do banco: R$",
                resumo["montante_total"]
            )

            print(
                "Contas correntes:",
                resumo["quantidade_corrente"]
            )

            print(
                "Montante em contas correntes: R$",
                resumo["montante_corrente"]
            )

            print(
                "Contas poupança:",
                resumo["quantidade_poupanca"]
            )

            print(
                "Montante em poupança: R$",
                resumo["montante_poupanca"]
            )

            print(
                "Contas salário:",
                resumo["quantidade_salario"]
            )

            print(
                "Montante em contas salário: R$",
                resumo["montante_salario"]
            )

            print(
                "Contas individuais:",
                resumo["quantidade_individuais"]
            )

            print(
                "Contas conjuntas:",
                resumo["quantidade_conjuntas"]
            )

        elif opcao != "0":

            print("Opção inválida.")

# Função principal do menu
def executar_menu():

    clientes, agencias, contas = carregar_dados()

    opcao = ""

    while opcao != "0":

        print("========== BANCO VIRTUAL ==========")
        print("1 - Clientes")
        print("2 - Agências")
        print("3 - Contas")
        print("4 - Operações bancárias")
        print("5 - Relatórios")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            menu_clientes(
                clientes,
                contas
            )

            salvar_dados(
                clientes,
                agencias,
                contas
            )


        elif opcao == "2":

            menu_agencias(
                agencias
            )

            salvar_dados(
                clientes,
                agencias,
                contas
            )


        elif opcao == "3":

            menu_contas(
                clientes,
                agencias,
                contas
            )

            salvar_dados(
                clientes,
                agencias,
                contas
            )

        elif opcao == "4":

            menu_operacoes(
                contas
            )

            salvar_dados(
                clientes,
                agencias,
                contas
            )

        elif opcao == "5":

            menu_relatorios(
                clientes,
                agencias,
                contas
            )

        elif opcao != "0":

            print("Opção inválida.")

    salvar_dados(
        clientes,
        agencias,
        contas
    )

    print("Programa encerrado.")
