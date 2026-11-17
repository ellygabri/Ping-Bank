from flask import Flask, render_template, request, redirect, url_for
from dados import carregar_dados, salvar_dados
from relatorio import resumo_bancario, montante_agencia, quantidade_contas_agencia
from clientes import Cliente
from agencias import cadastrar_agencia, procurar_agencia, listar_agencias
from contas import ContaCorrente, ContaPoupanca

app = Flask(__name__)

#Página inicial
@app.route("/")

def inicio():

    return render_template("inicio.html")

# Página do Dashboard
@app.route("/dashboard")
def dashboard():

    clientes = agencia.listar_clientes()
    contas = agencia.listar_contas()

    quantidade_clientes = len(clientes)
    quantidade_contas = agencia.quantidade_contas()
    montante_total = agencia.montante()

    quantidade_corrente = 0
    quantidade_poupanca = 0

    montante_corrente = 0.0
    montante_poupanca = 0.0

    maior_saldo = 0.0
    menor_saldo = 0.0
    saldo_medio = 0.0

    for conta in contas:

        if isinstance(conta, ContaCorrente):
            quantidade_corrente += 1
            montante_corrente += conta.saldo

        elif isinstance(conta, ContaPoupanca):
            quantidade_poupanca += 1
            montante_poupanca += conta.saldo

    if len(contas) > 0:

        maior_saldo = contas[0].saldo
        menor_saldo = contas[0].saldo

        for conta in contas:

            if conta.saldo > maior_saldo:
                maior_saldo = conta.saldo

            if conta.saldo < menor_saldo:
                menor_saldo = conta.saldo

        saldo_medio = montante_total / len(contas)

    return render_template("dashboard.html",
        quantidade_clientes = quantidade_clientes,
        quantidade_contas = quantidade_contas,
        montante_total = montante_total,
        maior_saldo = maior_saldo,
        menor_saldo = menor_saldo,
        saldo_medio = saldo_medio,
        quantidade_corrente = quantidade_corrente,
        quantidade_poupanca = quantidade_poupanca,
        montante_corrente = montante_corrente,
        montante_poupanca = montante_poupanca
    )
# Página para listar clientes
@app.route("/clientes")
def pagina_clientes():

    lista_clientes = agencia.listar_clientes()

    lista_clientes = sorted(lista_clientes, key=lambda cliente: cliente.nome.lower())

    mensagem = request.args.get("mensagem", "")

    return render_template("clientes.html", clientes=lista_clientes, mensagem=mensagem)

# Página para cadastrar cliente
@app.route("/clientes/cadastrar", methods=["GET", "POST"])
def cadastrar_cliente_w():

    mensagem = ""

    if request.method == "POST":

        nome = request.form["nome"]
        cpf = request.form["cpf"]
        contato = request.form["contato"]
        endereco = request.form["endereco"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]

        try:
            cliente = Cliente(nome,cpf, contato, endereco, data_nascimento,email)

            resultado = agencia.adicionar_cliente(cliente)

            if resultado == False:
                mensagem = "Já existe um cliente com esse CPF."

            else:
                return redirect(url_for("pagina_clientes", mensagem="Cliente cadastrado com sucesso."))

        except ValueError as erro:
            mensagem = str(erro)

    return render_template("cadastrar_cliente.html", mensagem=mensagem)

# Página para procurar cliente
@app.route("/clientes/procurar", methods=["GET", "POST"])
def procurar_cliente_w():

    cliente = None
    mensagem = ""

    if request.method == "POST":

        cpf = request.form["cpf"]

        cliente = agencia.buscar_cliente(cpf)

        if cliente is None:
            mensagem = "Cliente não encontrado."

    return render_template("procurar_cliente.html", cliente=cliente, mensagem=mensagem)

# Página para editar cliente
@app.route("/clientes/editar/<cpf>", methods=["GET", "POST"])
def editar_cliente_w(cpf):

    cliente = agencia.buscar_cliente(cpf)

    if cliente is None:
        return redirect(url_for("pagina_clientes", mensagem="Cliente não encontrado."))

    mensagem = ""

    if request.method == "POST":

        nome = request.form["nome"]
        contato = request.form["contato"]
        endereco = request.form["endereco"]
        data_nascimento = request.form["data_nascimento"]
        email = request.form["email"]

        if (nome.strip() == "" or contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == ""):
            mensagem = "As informações não podem ser vazias."

        else:
            cliente.editar_dado("nome", nome)
            cliente.editar_dado("contato", contato)
            cliente.editar_dado("endereco", endereco)
            cliente.editar_dado("data_nascimento", data_nascimento)
            cliente.editar_dado("email", email)

            return redirect(url_for("pagina_clientes", mensagem="Cliente alterado com sucesso."))

    return render_template("editar_cliente.html", cliente=cliente, mensagem=mensagem)

# Página para excluir cliente
@app.route("/clientes/excluir/<cpf>", methods=["POST"])
def excluir_cliente_w(cpf):

    cliente = agencia.buscar_cliente(cpf)

    if cliente is None:
        mensagem = "Cliente não encontrado."

    else:
        possui_conta = False

        for conta in agencia.contas:

            if conta.cliente == cliente:
                possui_conta = True

        if possui_conta == True:

            mensagem = "O cliente ainda possui uma conta."

        else:
            agencia.clientes.remove(cliente)

            mensagem = "Cliente excluído com sucesso."

    return redirect(url_for("pagina_clientes", mensagem=mensagem))

#  Agência única

@app.route("/agencia")
def pagina_agencia():
    return render_template(
        "agencia.html",
        agencia=agencia,
        quantidade_clientes=len(agencia.listar_clientes()),
        quantidade_contas=agencia.quantidade_contas(),
        montante=agencia.montante()
    )



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

    if request.method == "POST":

        maior_num_conta = len(agencia.contas)
        saldo = float(request.form["saldo"])
        tipo_conta = int(request.form["tipo_conta"])
        
        if tipo_conta == 1:
            agencia.contas.append(ContaCorrente(saldo, (maior_num_conta+1)))
        elif tipo_conta == 2:
            agencia.contas.append(ContaPoupanca(saldo, (maior_num_conta+1)))        

            return redirect(url_for("pagina_contas", mensagem = "Conta cadastrada com sucesso."))
    return render_template("cadastrar_conta.html", mensagem = "...")

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

        num_conta = int(request.form["num_conta"])
        valor = float(request.form["valor"])
        try:
            num_conta.depositar(valor)
        except AttributeError:
            return "Erro: conta não encontrada."

        mensagem = "Saque realizado com sucesso."
    return render_template("deposito.html", mensagem = mensagem)

#Página para realizar saque
@app.route("/operacoes/saque", methods = ["GET", "POST"])

def saque_w():
    mensagem = ""

    if request.method == "POST":

        num_conta = int(request.form["num_conta"])
        valor = float(request.form["valor"])
        try:
            num_conta.sacar(valor)
        except AttributeError:
            return "Erro: conta não encontrada."

        mensagem = "Saque realizado com sucesso."
    return render_template("saque.html", mensagem = mensagem)

#Página para realizar transferência
@app.route("/operacoes/transferencia", methods = ["GET", "POST"])

def transferencia_w():
    mensagem = ""

    if request.method == "POST":

        conta_origem = int(request.form["conta_origem"])
        conta_destino = int(request.form["conta_destino"])
        valor = float(request.form["valor"])
        try:
            conta_origem.transferencia(valor, conta_destino)
        except AttributeError:
            return "Erro: conta(s) não encontrada(s)."
            
        mensagem = "Transferência realizada com sucesso."
    return render_template("transferencia.html", mensagem = mensagem)

#Página para aplicar rendimento da poupança
@app.route("/operacoes/poupanca", methods=["GET", "POST"])
def poupanca_w():
    mensagem = ""
    novo_saldo = None

    if request.method == "POST":
        num_conta = request.form["num_conta"]
        cpf = request.form["cpf"]
        conta = agencia.buscar_conta(num_conta)

        if conta is None:
            mensagem = "Conta não encontrada."
        elif cliente_autorizado(conta, cpf) == False:
            mensagem = "CPF não autorizado."
        elif isinstance(conta, ContaPoupanca) == False:
            mensagem = "A conta informada não é poupança."
        else:
            try:
                meses_decorridos = int(request.form["meses_decorridos"])
                conta.aplicar_rendimento(meses_decorridos)
                novo_saldo = conta.saldo
                mensagem = "Rendimento aplicado com sucesso."
            except ValueError as erro:
                mensagem = str(erro)

    return render_template("poupanca.html", mensagem=mensagem, novo_saldo=novo_saldo)

#Página principal dos relatórios
@app.route("/relatorios")

def pagina_relatorios():
    return render_template("relatorios.html")

#Página para exibir o relatório geral do banco
@app.route("/relatorios/banco")

def relatorio_banco_w():
    clientes, agencias, contas = carregar_dados()

    resumo = resumo_bancario(clientes, agencias, contas)

    return render_template("relatorio_banco.html", resumo = resumo)

#Página para exibir relatório de uma agência
@app.route("/relatorios/agencia", methods = ["GET", "POST"])

def relatorio_agencia_w():
    agencia = None
    quantidade_contas = None
    montante = None
    mensagem = ""

    if request.method == "POST":
        clientes, agencias, contas = carregar_dados()

        num_agencia = request.form["num_agencia"]

        agencia_encontrada = procurar_agencia(agencias, num_agencia)

        if agencia_encontrada == False:
            mensagem = "Agência não encontrada."

        else:
            agencia = agencia_encontrada

            quantidade_contas = quantidade_contas_agencia(contas, num_agencia)

            montante = montante_agencia(contas, num_agencia)
    return render_template("relatorio_agencia.html", agencia = agencia, quantidade_contas = quantidade_contas, montante = montante, mensagem = mensagem)