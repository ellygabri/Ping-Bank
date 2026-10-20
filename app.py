from flask import Flask, render_template, request, redirect, url_for
from dados import carregar_dados, salvar_dados
from relatorio import resumo_bancario
from clientes import cadastrar_cliente, procurar_cliente, listar_clientes, editar_cliente, excluir_cliente

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