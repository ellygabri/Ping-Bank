import json

import cliente
import agencia
import conta 


# SUBMENU: CLIENTES

def cadastrar_cliente_fluxo(lista_clientes):
    print("\n--- Cadastro de Cliente ---")
    cpf = input("CPF (somente números): ").strip()

    if cliente.buscar_cliente(lista_clientes, cpf) != -1:
        print(f"Erro: já existe um cliente cadastrado com o CPF {cpf}.")
        return

    nome = input("Nome completo: ").strip()
    contato = input("Telefone/contato: ").strip()
    endereco = input("Endereço: ").strip()
    data_nascimento = input("Data de nascimento (dd/mm/aaaa): ").strip()
    email = input("E-mail: ").strip()

    novo_cliente = cliente.cadastrar_cliente(
        nome, cpf, contato, endereco, data_nascimento, email
    )
    if novo_cliente is False:
        print("Erro: todos os campos são obrigatórios.")
        return

    lista_clientes.append(novo_cliente)
    cliente.cpf_clientes.append(cpf)
    print(f"Cliente '{nome}' cadastrado com sucesso!")


def menu_clientes(lista_clientes):
    while True:
        print("\n===== CLIENTES =====")
        print("1 - Cadastrar cliente")
        print("2 - Listar clientes")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_cliente_fluxo(lista_clientes)
        elif opcao == "2":
            cliente.listar_clientes(lista_clientes)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")



# SUBMENU: AGÊNCIAS

def cadastrar_agencia_fluxo(lista_agencias):
    print("\n--- Cadastro de Agência ---")
    num_agencia = input("Número da agência: ").strip()
    nome_agencia = input("Nome/Localização da agência: ").strip()

    if num_agencia == "" or nome_agencia == "":
        print("Erro: todos os campos são obrigatórios.")
        return

    nova_agencia = agencia.cadastrar_agencia(lista_agencias, num_agencia, nome_agencia)
    if nova_agencia is False:
        # cadastrar_agencia já imprime "Agência já cadastrada!" quando é o caso.
        return

    lista_agencias.append(nova_agencia)
    print(f"Agência {num_agencia} - '{nome_agencia}' cadastrada com sucesso!")


def menu_agencias(lista_agencias):
    while True:
        print("\n===== AGÊNCIAS =====")
        print("1 - Cadastrar agência")
        print("2 - Listar agências")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_agencia_fluxo(lista_agencias)
        elif opcao == "2":
            agencia.listar_agencias(lista_agencias)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")



# SUBMENU: CONTAS

def menu_contas():
    while True:
        print("\n===== CONTAS =====")
        print("1 - Cadastrar conta")
        print("2 - Listar contas")
        print("3 - Consultar saldo")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            conta.criar_conta()
        elif opcao == "2":
            conta.listar_contas()
        elif opcao == "3":
            conta.consultar_saldo()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")



# SUBMENU: OPERAÇÕES

def transferir():
   
    print("\n--- Transferência ---")
    num_conta_origem = input("Número da conta de origem: ").strip()
    num_agencia_origem = input("Número da agência de origem: ").strip()
    existe_origem, indice_origem = conta.verificador_existencia(
        num_conta_origem, num_agencia_origem
    )
    if existe_origem != 1:
        print("Conta de origem não encontrada.")
        return

    cpf_validacao = input("CPF do titular da conta de origem: ").strip()
    if conta.verificacao_seguranca(cpf_validacao) != 1:
        print("Transação não autorizada.")
        return

    num_conta_destino = input("Número da conta de destino: ").strip()
    num_agencia_destino = input("Número da agência de destino: ").strip()
    existe_destino, indice_destino = conta.verificador_existencia(
        num_conta_destino, num_agencia_destino
    )
    if existe_destino != 1:
        print("Conta de destino não encontrada.")
        return

    if indice_origem == indice_destino:
        print("Não é possível transferir para a mesma conta.")
        return

    saldo_origem = conta.contas[indice_origem][3]
    valor = float(input("Valor a ser transferido: "))
    while valor <= 0 or valor > saldo_origem:
        print("Valor inválido. Por favor, tente novamente.")
        valor = float(input("Valor a ser transferido: "))

    origem = conta.contas[indice_origem]
    destino = conta.contas[indice_destino]
    conta.contas[indice_origem] = origem[:3] + (origem[3] - valor,) + origem[4:]
    conta.contas[indice_destino] = destino[:3] + (destino[3] + valor,) + destino[4:]
    print("Transferência realizada com sucesso.")


def menu_operacoes():
    while True:
        print("\n===== OPERAÇÕES =====")
        print("1 - Depositar")
        print("2 - Sacar")
        print("3 - Transferir")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            conta.deposito()
        elif opcao == "2":
            conta.saque()
        elif opcao == "3":
            transferir()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")



# SUBMENU: RELATÓRIOS

def relatorio_montante_agencia(lista_agencias):
    print("\n--- Montante Total de uma Agência ---")
    num_agencia = input("Número da agência: ").strip()

    if agencia.buscar_agencia(lista_agencias, num_agencia) == -1:
        print(f"Erro: a agência {num_agencia} não existe.")
        return

    total = 0
    qtd_contas = 0
    for conta_atual in conta.contas:
        if conta_atual[1] == num_agencia:
            total += conta_atual[3]
            qtd_contas += 1

    print(f"Agência {num_agencia} possui {qtd_contas} conta(s).")
    print(f"Montante total: R$ {total:.2f}")


def relatorio_montante_banco():
    print("\n--- Montante Total do Banco ---")
    total = sum(conta_atual[3] for conta_atual in conta.contas)
    print(f"Total de contas no banco: {len(conta.contas)}")
    print(f"Montante total do Ping-Bank: R$ {total:.2f}")


def menu_relatorios(lista_agencias):
    while True:
        print("\n===== RELATÓRIOS =====")
        print("1 - Montante total de uma agência")
        print("2 - Montante total do banco")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            relatorio_montante_agencia(lista_agencias)
        elif opcao == "2":
            relatorio_montante_banco()
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")



# SALVAR DADOS

def salvar_dados(lista_clientes, lista_agencias, caminho="ping_bank_dados.json"):
   
    dados = [lista_clientes, lista_agencias, conta.contas]

    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em '{caminho}'.")
    except OSError as erro:
        print(f"Erro ao salvar os dados: {erro}")



# MENU PRINCIPAL

def iniciar():
    """Função chamada pelo main.py para dar início ao sistema."""
    # As listas principais que este módulo é responsável por manter.
    lista_clientes = []
    lista_agencias = []


    while True:
        print("\n========== MENU PRINCIPAL ==========")
        print("1 - Clientes")
        print("2 - Agências")
        print("3 - Contas")
        print("4 - Operações")
        print("5 - Relatórios")
        print("6 - Salvar Dados")
        print("0 - Sair")
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            menu_clientes(lista_clientes)
        elif opcao == "2":
            menu_agencias(lista_agencias)
        elif opcao == "3":
            menu_contas()
        elif opcao == "4":
            menu_operacoes()
        elif opcao == "5":
            menu_relatorios(lista_agencias)
        elif opcao == "6":
            salvar_dados(lista_clientes, lista_agencias)
        elif opcao == "0":
            print("Obrigado por usar o Ping-Bank. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")
