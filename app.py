from flask import Flask, render_template
from dados import carregar_dados
from relatorio import resumo_bancario

app = Flask(__name__)

@app.route("/")

def dashboard():
    clientes, agencias, contas = carregar_dados()

    resumo = resumo_bancario(clientes, agencias, contas)

    return render_template("dashboard.html", resumo = resumo)