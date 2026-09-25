import json

import agencia
import cliente
import conta

CAMINHO_DADOS = "ping_bank_dados.json"


def ler_inteiro(mensagem, minimo=None):
    valor = input(mensagem).strip()
    while not valor.isdigit() or (minimo is not None and int(valor) < minimo):
        print("Digite um número válido.")
        valor = input(mensagem).strip()
    return int(valor)


def ler_float(mensagem, minimo=None):
    valor = input(mensagem).strip().replace(",", ".")
    valido = False
    numero = 0.0
    while not valido:
        try:
            numero = float(valor)
            valido = minimo is None or numero >= minimo
        except ValueError:
            valido = False
        if not valido:
            print("Digite um valor válido.")
            valor = input(mensagem).strip().replace(",", ".")
    return numero


def cadastrar_cliente_fluxo(lista_clientes):
    print("\n--- Cadastro de Cliente ---")
    cpf = input("CPF: ").strip()
    if cliente.buscar_cliente(lista_clientes, cpf) != -1:
        print("Já existe um cliente com esse CPF.")
        return
    dados = [
        input("Nome completo: ").strip(), cpf,
        input("Telefone/contato: ").strip(), input("Endereço: ").strip(),
        input("Data de nascimento (dd/mm/aaaa): ").strip(), input("E-mail: ").strip(),
    ]
    novo_cliente = cliente.cadastrar_cliente(*dados)
    if novo_cliente is False:
        print("Erro: todos os campos são obrigatórios.")
        return
    lista_clientes.append(novo_cliente)
    print("Cliente cadastrado com sucesso.")


def editar_cliente_fluxo(lista_clientes):
    cpf = input("CPF do cliente: ").strip()
    indice = cliente.buscar_cliente(lista_clientes, cpf)
    if indice == -1:
        print("Cliente não encontrado.")
        return
    atual = lista_clientes[indice]
    dados = [
        input(f"Nome completo [{atual[0]}]: ").strip() or atual[0], cpf,
        input(f"Telefone/contato [{atual[2]}]: ").strip() or atual[2],
        input(f"Endereço [{atual[3]}]: ").strip() or atual[3],
        input(f"Data de nascimento [{atual[4]}]: ").strip() or atual[4],
        input(f"E-mail [{atual[5]}]: ").strip() or atual[5],
    ]
    cliente.editar_cliente(lista_clientes, *dados)


def excluir_cliente_fluxo(lista_clientes, lista_contas):
    cpf = input("CPF do cliente: ").strip()
    resultado = cliente.excluir_cliente(lista_clientes, lista_contas, cpf)
    mensagens = {
        -1: "Cliente não encontrado.",
        0: "O cliente ainda é titular de uma conta.",
        1: "Cliente excluído com sucesso.",
    }
    print(mensagens[resultado])


def menu_clientes(lista_clientes, lista_contas):
    opcao = ""
    while opcao != "0":
        print("\n===== CLIENTES =====")
        print("1 - Cadastrar cliente\n2 - Listar clientes\n3 - Procurar cliente")
        print("4 - Editar cliente\n5 - Excluir cliente\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_cliente_fluxo(lista_clientes)
        elif opcao == "2":
            cliente.listar_clientes(lista_clientes)
        elif opcao == "3":
            cliente.procurar_cliente(lista_clientes, input("CPF: ").strip())
        elif opcao == "4":
            editar_cliente_fluxo(lista_clientes)
        elif opcao == "5":
            excluir_cliente_fluxo(lista_clientes, lista_contas)
        elif opcao != "0":
            print("Opção inválida.")


def cadastrar_agencia_fluxo(lista_agencias):
    print("\n--- Cadastro de Agência ---")
    numero = input("Número da agência: ").strip()
    nome = input("Nome/localização: ").strip()
    nova_agencia = agencia.cadastrar_agencia(lista_agencias, numero, nome)
    if nova_agencia is False:
        print("Não foi possível cadastrar a agência.")
        return
    lista_agencias.append(nova_agencia)
    print("Agência cadastrada com sucesso.")


def menu_agencias(lista_agencias):
    opcao = ""
    while opcao != "0":
        print("\n===== AGÊNCIAS =====")
        print("1 - Cadastrar agência\n2 - Listar agências\n3 - Procurar agência\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_agencia_fluxo(lista_agencias)
        elif opcao == "2":
            agencia.listar_agencias(lista_agencias)
        elif opcao == "3":
            agencia.procurar_agencia(lista_agencias, input("Número: ").strip())
        elif opcao != "0":
            print("Opção inválida.")


def cadastrar_conta_fluxo(lista_contas, lista_clientes, lista_agencias):
    numero_agencia = input("Número da agência: ").strip()
    tipo = ler_inteiro("Tipo (1 - individual, 2 - conjunta): ", 1)
    while tipo not in (1, 2):
        print("Escolha o tipo 1 ou 2.")
        tipo = ler_inteiro("Tipo (1 - individual, 2 - conjunta): ", 1)
    texto = input("CPF(s) do(s) titular(es), separados por vírgula: ")
    saldo = ler_float("Saldo inicial: ", 0)
    titulares = tuple(cpf.strip() for cpf in texto.split(",") if cpf.strip())
    nova_conta = conta.criar_conta(lista_contas, lista_clientes, lista_agencias, numero_agencia, tipo, saldo, titulares)
    mensagens = {-1: "Agência não encontrada.", -2: "Tipo de conta inválido.", -3: "O saldo não pode ser negativo.", -4: "Conta individual deve ter um titular.", -5: "Um dos titulares não está cadastrado.", -6: "Não repita titulares."}
    if nova_conta in mensagens:
        print(mensagens[nova_conta])
        return
    lista_contas.append(nova_conta)
    print(f"Conta {nova_conta[0]} criada com sucesso.")


def listar_contas_fluxo(lista_contas):
    contas = conta.listar_contas(lista_contas)
    if contas is False:
        print("Nenhuma conta cadastrada.")
        return
    print("\n========== CONTAS ==========")
    for conta_atual in contas:
        titulares = ", ".join(conta_atual[4])
        print(f"Número: {conta_atual[0]} | Agência: {conta_atual[1]} | Tipo: {conta_atual[2]} | Saldo: R$ {conta_atual[3]:.2f} | Titulares: {titulares}")


def consultar_saldo_fluxo(lista_contas):
    numero = ler_inteiro("Número da conta: ")
    numero_agencia = input("Número da agência: ").strip()
    cpf = input("CPF do titular: ").strip()
    saldo = conta.consultar_saldo(lista_contas, numero, numero_agencia, cpf)
    if saldo == -1:
        print("Conta não encontrada.")
    elif saldo == -2:
        print("CPF não autorizado.")
    else:
        print(f"Saldo: R$ {saldo:.2f}")


def menu_contas(lista_contas, lista_clientes, lista_agencias):
    opcao = ""
    while opcao != "0":
        print("\n===== CONTAS =====")
        print("1 - Cadastrar conta\n2 - Listar contas\n3 - Consultar saldo\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_conta_fluxo(lista_contas, lista_clientes, lista_agencias)
        elif opcao == "2":
            listar_contas_fluxo(lista_contas)
        elif opcao == "3":
            consultar_saldo_fluxo(lista_contas)
        elif opcao != "0":
            print("Opção inválida.")


def deposito_fluxo(lista_contas):
    numero = ler_inteiro("Número da conta: ")
    numero_agencia = input("Número da agência: ").strip()
    cpf = input("CPF do titular: ").strip()
    valor = ler_float("Valor do depósito: ", 0)
    resultado = conta.deposito(lista_contas, numero, numero_agencia, cpf, valor)
    mensagens = {-1: "Conta não encontrada.", -2: "CPF não autorizado.", 0: "Valor inválido.", 1: "Depósito realizado."}
    print(mensagens[resultado])


def saque_fluxo(lista_contas):
    numero = ler_inteiro("Número da conta: ")
    numero_agencia = input("Número da agência: ").strip()
    cpf = input("CPF do titular: ").strip()
    valor = ler_float("Valor do saque: ", 0)
    resultado = conta.saque(lista_contas, numero, numero_agencia, cpf, valor)
    mensagens = {-1: "Conta não encontrada.", -2: "CPF não autorizado.", 0: "Valor inválido.", -3: "Saldo insuficiente.", 1: "Saque realizado."}
    print(mensagens[resultado])


def transferencia_fluxo(lista_contas):
    conta_origem = ler_inteiro("Conta de origem: ")
    agencia_origem = input("Agência de origem: ").strip()
    cpf = input("CPF do titular da origem: ").strip()
    conta_destino = ler_inteiro("Conta de destino: ")
    agencia_destino = input("Agência de destino: ").strip()
    valor = ler_float("Valor da transferência: ", 0)
    resultado = conta.tranferencia(lista_contas, conta_origem, agencia_origem, cpf, conta_destino, agencia_destino, valor)
    mensagens = {-1: "Conta de origem não encontrada.", -2: "CPF não autorizado.", -3: "Conta de destino não encontrada.", -4: "A origem e o destino são iguais.", 0: "Valor inválido.", -5: "Saldo insuficiente.", 1: "Transferência realizada."}
    print(mensagens[resultado])


def menu_operacoes(lista_contas):
    opcao = ""
    while opcao != "0":
        print("\n===== OPERAÇÕES =====")
        print("1 - Depositar\n2 - Sacar\n3 - Transferir\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            deposito_fluxo(lista_contas)
        elif opcao == "2":
            saque_fluxo(lista_contas)
        elif opcao == "3":
            transferencia_fluxo(lista_contas)
        elif opcao != "0":
            print("Opção inválida.")


def menu_relatorios(lista_contas, lista_agencias):
    opcao = ""
    while opcao != "0":
        print("\n===== RELATÓRIOS =====")
        print("1 - Montante de uma agência\n2 - Montante total do banco\n0 - Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            numero = input("Número da agência: ").strip()
            if agencia.buscar_agencia(lista_agencias, numero) == -1:
                print("Agência não encontrada.")
            else:
                contas_agencia = [item for item in lista_contas if item[1] == numero]
                total = sum(item[3] for item in contas_agencia)
                print(f"Quantidade de contas: {len(contas_agencia)}")
                print(f"Montante: R$ {total:.2f}")
        elif opcao == "2":
            total = sum(item[3] for item in lista_contas)
            print(f"Total de contas: {len(lista_contas)}")
            print(f"Montante total: R$ {total:.2f}")
        elif opcao != "0":
            print("Opção inválida.")


def salvar_dados(lista_clientes, lista_agencias, lista_contas, caminho=CAMINHO_DADOS):
    dados = {
        "clientes": [
            {
                "nome": cliente_atual[0],
                "cpf": cliente_atual[1],
                "contato": cliente_atual[2],
                "endereco": cliente_atual[3],
                "data_nascimento": cliente_atual[4],
                "email": cliente_atual[5],
            }
            for cliente_atual in lista_clientes
        ],
        "agencias": [
            {"numero": agencia_atual[0], "nome": agencia_atual[1]}
            for agencia_atual in lista_agencias
        ],
        "contas": [
            {
                "numero": conta_atual[0],
                "agencia": conta_atual[1],
                "tipo": conta_atual[2],
                "saldo": conta_atual[3],
                "titulares": list(conta_atual[4]),
            }
            for conta_atual in lista_contas
        ],
    }
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
        print(f"Dados salvos com sucesso em '{caminho}'.")
    except OSError as erro:
        print(f"Erro ao salvar os dados: {erro}")


def carregar_dados(caminho=CAMINHO_DADOS):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        return [], [], []
    except (OSError, json.JSONDecodeError):
        print(f"Não foi possível ler os dados de '{caminho}'.")
        return [], [], []

    if not isinstance(dados, dict):
        print("Formato de dados inválido.")
        return [], [], []

    clientes = [
        (
            item["nome"], item["cpf"], item["contato"], item["endereco"],
            item["data_nascimento"], item["email"],
        )
        for item in dados.get("clientes", [])
    ]
    agencias = [
        (item["numero"], item["nome"])
        for item in dados.get("agencias", [])
    ]
    contas = [
        (
            item["numero"], item["agencia"], item["tipo"], item["saldo"],
            tuple(item["titulares"]),
        )
        for item in dados.get("contas", [])
    ]
    return clientes, agencias, contas


def iniciar():
    lista_clientes, lista_agencias, lista_contas = carregar_dados()
    opcao = ""
    print("=" * 40)
    print("       BEM-VINDO AO PING-BANK")
    print("=" * 40)
    while opcao != "0":
        print("\n========== MENU PRINCIPAL ==========")
        print("1 - Clientes\n2 - Agências\n3 - Contas\n4 - Operações")
        print("5 - Relatórios\n6 - Salvar dados\n0 - Sair")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            menu_clientes(lista_clientes, lista_contas)
        elif opcao == "2":
            menu_agencias(lista_agencias)
        elif opcao == "3":
            menu_contas(lista_contas, lista_clientes, lista_agencias)
        elif opcao == "4":
            menu_operacoes(lista_contas)
        elif opcao == "5":
            menu_relatorios(lista_contas, lista_agencias)
        elif opcao == "6":
            salvar_dados(lista_clientes, lista_agencias, lista_contas)
        elif opcao != "0":
            print("Opção inválida.")
    print("Obrigado por usar o Ping-Bank. Até logo!")
