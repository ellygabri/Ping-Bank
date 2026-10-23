from flask import Flask, render_template, request, redirect, url_for
from dados import carregar_dados, salvar_dados
from relatorio import resumo_bancario
from clientes import cadastrar_cliente, procurar_cliente, listar_clientes, editar_cliente, excluir_cliente
from agencias import cadastrar_agencia, procurar_agencia, listar_agencias
from contas import criar_conta, procurar_conta, listar_contas, listar_contas_saldo_positivo, listar_contas_clientes, listar_titulares, adicionar_titular, remover_titular, substituir_titular, excluir_conta, consultar_saldo, deposito, saque, transferencia, calculo_poupanca 

app = Flask(__name__)

#Página inicial do Dashboard
@app.route("/")

def dashboard():
    clientes, agencias, contas = carregar_dados()

    resumo = resumo_bancario(clientes, agencias, contas)

    return render_template("dashboard.html", resumo = resumo)

#Página para listar clientes
@app.route("/clientes")

def pagina_clientes():
    clientes, agencias, contas = carregar_dados()
    lista_clientes = listar_clientes(clientes)

    if lista_clientes == False:
        lista_clientes = []
    mensagem = request.args.get("mensagem", "")
    return render_template("clientes.html", clientes = lista_clientes, mensagem = mensagem)

#Página para cadastrar cliente
@app.route("/clientes/cadastrar", methods = ["GET", "POST"])

def cadastrar_cliente_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        nome = request.form["nome"]
        cpf = request.form["cpf"]
        contato = request.form["contato"]
        endereco = request.form["endereco"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]

        resultado = cadastrar_cliente(clientes, nome, cpf, contato, endereco, data_nascimento, email)
        if resultado == -2:
            mensagem = "CPF inválido."
        elif resultado == -1:
            mensagem = "Existem campos vazios."
        elif resultado == 0:
            mensagem = "Já existe um cliente com esse CPF."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            return redirect(url_for("pagina_clientes", mensagem = "Cliente cadastrado com sucesso."))
    return render_template("cadastrar_cliente.html", mensagem = mensagem)

#Página para procurar cliente
@app.route("/clientes/procurar", methods =["GET", "POST"])

def procurar_cliente_w():
    cliente = None
    mensagem = "" 

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        cpf = request.form["cpf"]
        resultado = procurar_cliente(clientes, cpf)

        if resultado == False:
            mensagem = "Cliente não encontrado."
        else:
            cliente = resultado
    return render_template("procurar_cliente.html", cliente = cliente, mensagem = mensagem)

#Página para editar um cliente
@app.route("/clientes/editar/<cpf>", methods=["GET", "POST"])

def editar_cliente_w(cpf):
    clientes, agencias, contas = carregar_dados()
    cliente = procurar_cliente(clientes, cpf)

    if cliente == False:
        return redirect(url_for("pagina_clientes", mensagem = "Cliente não encontrado."))
    mensagem = ""

    if request.method == "POST":
        nome = request.form["nome"]
        contato = request.form["contato"]
        endereco = request.form["endereco"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]

        if nome.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
                mensagem = "As informações não podem ser vazias."
        else:
            editar_cliente(clientes, cpf, "nome", nome)
            editar_cliente(clientes, cpf, "contato", contato)
            editar_cliente(clientes, cpf, "endereco", endereco)
            editar_cliente(clientes, cpf, "data_nascimento", data_nascimento)
            editar_cliente(clientes, cpf, "email", email)
            salvar_dados(clientes, agencias, contas)

            return redirect(url_for("pagina_clientes", mensagem = "Cliente alterado com sucesso."))
    return render_template("editar_cliente.html", cliente = cliente, mensagem = mensagem)

#Função para excluir um cliente
@app.route("/clientes/excluir/<cpf>", methods = ["POST"])

def excluir_cliente_w(cpf):
    clientes, agencias, contas = carregar_dados()

    resultado = excluir_cliente(clientes, contas, cpf)

    if resultado == -1:
        mensagem = "Cliente não encontrado."
    elif resultado == 0:
        mensagem = "O cliente ainda é titular de uma conta."
    else:
        salvar_dados(clientes, agencias, contas)

        mensagem = "Cliente excluído com sucesso."

    return redirect(url_for("pagina_clientes", mensagem = mensagem))

#Página para listar agências
@app.route("/agencias")

def pagina_agencias():
    clientes, agencias, contas = carregar_dados()

    lista_agencias = listar_agencias(agencias)

    if lista_agencias == False:
        lista_agencias = []
    mensagem = request.args.get("mensagem", "")

    return render_template("agencias.html", agencias = lista_agencias, mensagem = mensagem)

#Página para cadastrar agência
@app.route("/agencias/cadastrar", methods = ["GET", "POST"])

def cadastrar_agencia_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_agencia = request.form["num_agencia"]
        nome_agencia = request.form["nome_agencia"]

        resultado = cadastrar_agencia(agencias, num_agencia, nome_agencia)

        if resultado == -1:
            mensagem = "Existem campos vazios."
        elif resultado == 0:
            mensagem = "Agência já cadastrada."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)
            return redirect(url_for("pagina_agencias", mensagem = "Agência cadastrada com sucesso."))
    return render_template("cadastrar_agencia.html", mensagem = mensagem)

#Página para procurar agência
@app.route("/agencias/procurar", methods = ["GET", "POST"])

def procurar_agencia_w():
    agencia = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_agencia = request.form["num_agencia"]

        resultado = procurar_agencia(agencias, num_agencia)

        if resultado == False:
            mensagem = "Agência não encontrada."

        else:
            agencia = resultado

    return render_template("procurar_agencia.html", agencia = agencia, mensagem = mensagem)

#Página para listar contas
@app.route("/contas")

def pagina_contas():
    clientes, agencias, contas = carregar_dados()

    lista_contas = listar_contas(contas)

    if lista_contas == False:
        lista_contas = []
    mensagem = request.args.get("mensagem", "")

    return render_template("contas.html", contas = lista_contas, mensagem = mensagem)

#Página para cadastrar conta
@app.route("/contas/cadastrar", methods = ["GET", "POST"])

def cadastrar_conta_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_agencia = request.form["num_agencia"]
        tipo_titulares = int(request.form["tipo_titulares"])
        saldo = float(request.form["saldo"])
        tipo_conta = int(request.form["tipo_conta"])

        titulares_texto = request.form["titulares"]

        titulares = [cpf.strip() for cpf in titulares_texto.split(",") if cpf.strip() != ""]

        resultado = criar_conta(contas,clientes,num_agencia,tipo_titulares, saldo, titulares, tipo_conta)

        if resultado == -1:
            mensagem = "Agência não encontrada."
        elif resultado == -2:
            mensagem = "Tipo de titularidade inválido."
        elif resultado == -3:
            mensagem = "Saldo inicial inválido."
        elif resultado == -4:
            mensagem = "Quantidade de titulares inválida."
        elif resultado == -5:
            mensagem = "Um dos titulares não está cadastrado."
        elif resultado == -6:
            mensegem = "Tipo de conta inválido."
        elif resultado == -7:
            mensagem = "Existem titulares repetidos."
        else:
            contas.append(resultado)
            salvar_dados(clientes, agencias, contas)

            return redirect(url_for("pagina_contas", mensagem = "Conta cadastrada com sucesso."))
    return render_template("cadastrar_conta.html", mensagem = mensagem)

#Página para procurar conta
@app.route("/contas/procurar", methods = ["GET", "POST"])

def procurar_conta_w():
    conta = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf = request.form["cpf"]

        resultado = procurar_conta( contas, num_conta, num_agencia, cpf)

        if resultado == False:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        else:
            conta = resultado
    return render_template("procurar_conta.html", conta = conta, mensagem = mensagem)

#Página para listar contas de um cliente
@app.route("/contas/cliente", methods = ["GET", "POST"])

def contas_cliente_w():
    contas_cliente = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()
        cpf = request.form["cpf"]

        resultado = listar_contas_clientes(contas, cpf )

        if resultado == False:
            mensagem = "O cliente não possui contas."
        else:
            contas_cliente = resultado
    return render_template("contas_cliente.html", contas = contas_cliente, mensagem = mensagem)

#Página para listar contas com saldo positivo
@app.route("/contas/positivas")

def contas_positivas_w():
    clientes, agencias, contas = carregar_dados()

    lista_contas = listar_contas_saldo_positivo(contas)

    if lista_contas == False:
        lista_contas = []
    return render_template("contas_positivas.html", contas = lista_contas)

#Página para listar titulares de uma conta
@app.route("/contas/titulares", methods = ["GET", "POST"])

def titulares_conta_w():
    titulares = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]

        resultado = listar_titulares(contas, num_conta, num_agencia)
        if resultado == False:
            mensagem = "Conta não encontrada."
        else:
            titulares = resultado
    return render_template("titulares_conta.html", titulares = titulares, mensagem = mensagem)

#Página para adicionar titular
@app.route("/contas/titulares/adicionar", methods = ["GET", "POST"])

def adicionar_titular_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf_validacao = request.form["cpf_validacao"]
        novo_titular = request.form["novo_titular"]

        resultado = adicionar_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, novo_titular)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -3:
            mensagem = "Novo titular não cadastrado."
        elif resultado == 0:
            mensagem = "Esse cliente já é titular da conta."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Titular adicionado com sucesso."
    return render_template("adicionar_titular.html", mensagem = mensagem)

#Página para remover titular
@app.route("/contas/titulares/remover", methods = ["GET", "POST"])

def remover_titular_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf_validacao = request.form["cpf_validacao"]
        titular_removido = request.form["titular_removido"]

        resultado = remover_titular(contas, num_conta, num_agencia, cpf_validacao, titular_removido)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -3:
            mensagem = "A conta não pode ficar sem titular."
        elif resultado == 0:
            mensagem = "O CPF informado não é titular da conta."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Titular removido com sucesso."
    return render_template("remover_titular.html", mensagem = mensagem)

#Página para substituir titular
@app.route("/contas/titulares/substituir", methods = ["GET", "POST"])

def substituir_titular_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf_validacao = request.form["cpf_validacao"]
        titular_antigo = request.form["titular_antigo"]
        novo_titular = request.form["novo_titular"]

        resultado = substituir_titular(contas, clientes, num_conta, num_agencia, cpf_validacao, titular_antigo, novo_titular)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -3:
            mensagem = "Novo titular não cadastrado."
        elif resultado == -4:
            mensagem = "O novo cliente já é titular."
        elif resultado == 0:
            mensagem = "Titular antigo não encontrado."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Titular substituído com sucesso."
    return render_template("substituir_titular.html", mensagem = mensagem)

#Página para excluir conta
@app.route("/contas/excluir", methods = ["GET", "POST"])

def excluir_conta_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf = request.form["cpf"]

        resultado = excluir_conta(contas, num_conta, num_agencia, cpf)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == 0:
            mensagem = "A conta precisa estar com saldo zero."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)
            return redirect(url_for("pagina_contas", mensagem = "Conta excluída com sucesso."))
    return render_template( "excluir_conta.html", mensagem = mensagem)

#Página principal das operações bancárias
@app.route("/operacoes")

def pagina_operacoes():
    return render_template("operacoes.html")

#Página para consultar saldo
@app.route("/operacoes/saldo", methods = ["GET", "POST"])

def consultar_saldo_w():
    saldo = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf = request.form["cpf"]

        resultado = consultar_saldo(contas, num_conta, num_agencia, cpf)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        else:
            saldo = resultado
    return render_template("consultar_saldo.html", saldo = saldo, mensagem = mensagem)

#Página para realizar depósito
@app.route("/operacoes/deposito", methods = ["GET", "POST"])

def deposito_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf = request.form["cpf"]
        valor = float(request.form["valor"])

        resultado = deposito(contas, num_conta, num_agencia, cpf, valor)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -4:
            mensagem = "Conta salário não permite essa operação."
        elif resultado == 0:
            mensagem = "Valor inválido."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Depósito realizado com sucesso."
    return render_template("deposito.html", mensagem = mensagem)

#Página para realizar saque
@app.route("/operacoes/saque", methods = ["GET", "POST"])

def saque_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        cpf = request.form["cpf"]
        valor = float(request.form["valor"])

        resultado = saque(contas, num_conta, num_agencia, cpf, valor)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -3:
            mensagem = "Saldo insuficiente."
        elif resultado == 0:
            mensagem = "Valor inválido."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Saque realizado com sucesso."
    return render_template("saque.html", mensagem = mensagem)

#Página para realizar transferência
@app.route("/operacoes/transferencia", methods = ["GET", "POST"])

def transferencia_w():
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        conta_origem = int(request.form["conta_origem"])
        agencia_origem = request.form["agencia_origem"]
        cpf = request.form["cpf"]

        conta_destino = int(request.form["conta_destino"])
        agencia_destino = request.form["agencia_destino"]

        valor = float(request.form["valor"])

        resultado = transferencia(contas, conta_origem, agencia_origem, cpf, conta_destino, agencia_destino, valor)

        if resultado == -1:
            mensagem = "Conta de origem não encontrada."
        elif resultado == -2:
            mensagem = "CPF não autorizado."
        elif resultado == -3:
            mensagem = "Conta de destino não encontrada."
        elif resultado == -4:
            mensagem = "As contas de origem e destino são iguais."
        elif resultado == -5:
            mensagem = "Saldo insuficiente."
        elif resultado == -6:
            mensagem = "Conta salário não permite essa operação."
        elif resultado == 0:
            mensagem = "Valor inválido."
        elif resultado == 1:
            salvar_dados(clientes, agencias, contas)

            mensagem = "Transferência realizada com sucesso."
    return render_template("transferencia.html", mensagem = mensagem)

#Página para aplicar rendimento da poupança
@app.route("/operacoes/poupanca", methods = ["GET", "POST"])

def poupanca_w():
    mensagem = ""
    novo_saldo = None

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_conta = int(request.form["num_conta"])
        num_agencia = request.form["num_agencia"]
        meses_decorridos = int(request.form["meses_decorridos"])

        resultado = calculo_poupanca(num_conta, num_agencia, contas, meses_decorridos)

        if resultado == -1:
            mensagem = "Conta não encontrada."
        elif resultado == -2:
            mensagem = "A conta informada não é poupança."
        elif resultado == -3:
            mensagem = "Quantidade de meses inválida."
        else:
            salvar_dados(clientes, agencias, contas)

            novo_saldo = resultado
            mensagem = "Rendimento aplicado com sucesso."
    return render_template("poupanca.html", mensagem = mensagem, novo_saldo = novo_saldo)