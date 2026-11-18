import json

from agencias import Agencia
from clientes import Cliente
from contas import ContaCorrente, ContaPoupanca

ARQUIVO_DADOS = "ping_bank_dados.json"


def carregar_dados():
    
    # Abre e carrega o conteúdo do arquivo JSON para um dicionário Python
    arquivo = open(ARQUIVO_DADOS, "r", encoding="utf-8")
    dados = json.load(arquivo)
    arquivo.close()

    numero_agencia = "001"
    nome_agencia = "Agência PING BANK"

    if "agencia" in dados:
        numero_agencia = dados["agencia"].get("numero", numero_agencia)
        nome_agencia = dados["agencia"].get("nome", nome_agencia)

    agencia = Agencia(numero_agencia, nome_agencia)

    # Reconstrói os objetos Cliente a partir da lista no JSON e os adiciona à agência
    for dados_cliente in dados.get("clientes", []):
        cliente = Cliente(
            dados_cliente["nome"],
            dados_cliente["cpf"],
            dados_cliente["contato"],
            dados_cliente["endereco"],
            dados_cliente["data_nascimento"],
            dados_cliente["email"]
        )
        agencia.adicionar_cliente(cliente)

    # Reconstrói as contas e as vincula ao cliente titular
    for dados_conta in dados.get("contas", []):
        cpf_cliente = dados_conta.get("cpf_cliente")
        cliente = agencia.buscar_cliente(cpf_cliente)

        # toda conta deve pertencer a um cliente já cadastrado
        if cliente is None:
            raise ValueError("Existe uma conta no JSON vinculada a um cliente inexistente.")

        tipo_conta = dados_conta.get("tipo_conta")
        saldo = dados_conta.get("saldo", 0.0)
        num_conta = dados_conta.get("num_conta")

        # Instancia a subclasse correspondente ao tipo de conta salvo
        if tipo_conta == "Corrente" or tipo_conta == "corrente" or tipo_conta == 1:
            limite = dados_conta.get("limite_cheque_especial", 200.0)
            conta = ContaCorrente(saldo, num_conta, cliente, limite)
            agencia.adicionar_conta(conta)

        elif tipo_conta == "Poupança" or tipo_conta == "poupanca" or tipo_conta == 2:
            taxa = dados_conta.get("taxa_rendimento", ContaPoupanca.TAXA_RENDIMENTO_PADRAO)
            conta = ContaPoupanca(saldo, num_conta, cliente, taxa)
            agencia.adicionar_conta(conta)

    return agencia


def salvar_dados(agencia):
    
    clientes = []

    # Converte cada objeto Cliente da agência em um dicionário
    for cliente in agencia.listar_clientes():
        clientes.append({
            "nome": cliente.nome,
            "cpf": cliente.cpf,
            "contato": cliente.contato,
            "endereco": cliente.endereco,
            "data_nascimento": cliente.data_nascimento,
            "email": cliente.email
        })

    contas = []

    # Converte cada objeto Conta em um dicionário
    for conta in agencia.listar_contas():
        dados_conta = {
            "num_conta": conta.num_conta,
            "tipo_conta": conta.tipo_conta(),
            "saldo": conta.saldo,
            "cpf_cliente": conta.cliente.cpf
        }

        # Adiciona atributos específicos conforme a subclasse da conta
        if isinstance(conta, ContaCorrente):
            dados_conta["limite_cheque_especial"] = conta.limite_cheque_especial
        elif isinstance(conta, ContaPoupanca):
            dados_conta["taxa_rendimento"] = conta.taxa_rendimento

        contas.append(dados_conta)

    # Estrutura o dicionário raiz que será exportado para o arquivo
    dados = {
        "agencia": {
            "numero": agencia.numero,
            "nome": agencia.nome
        },
        "clientes": clientes,
        "contas": contas
    }

    # Grava os dados formatados no arquivo JSON preservando acentuação
    arquivo = open(ARQUIVO_DADOS, "w", encoding="utf-8")
    json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    arquivo.close()