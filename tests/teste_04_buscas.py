# Teste 04 - Buscas, listagens e relatórios
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from verificacao import verificar
from clientes import buscar_cliente, procurar_cliente
from agencias import buscar_agencia, procurar_agencia
from contas import (verificador_existencia, procurar_conta, listar_contas, listar_contas_saldo_positivo,
                    listar_contas_clientes, listar_titulares, consultar_saldo)
from relatorio import (montante_agencia, montante_banco, quantidade_contas_agencia, montante_tipo_conta,
                       quantidade_tipo_conta, quantidade_tipo_titulares, resumo_bancario,
                       menor_saldo, maior_saldo, saldo_medio)

ANA = "10433218100"
CARLOS = "96001338914"
MARIANA = "08386379499"

CLIENTES = [
    {"nome": "Ana", "cpf": ANA, "contato": "1", "endereco": "A", "data_nascimento": "01/01/1990", "email": "a@example.com"},
    {"nome": "Carlos", "cpf": CARLOS, "contato": "2", "endereco": "B", "data_nascimento": "01/01/1991", "email": "b@example.com"},
]
AGENCIAS = [
    {"num_agencia": "0001", "nome_agencia": "Centro"},
    {"num_agencia": "0002", "nome_agencia": "Atalaia"},
]


def novas_contas():
    # Contas novas a cada chamada, para um teste não afetar o outro
    return [
        {"num_conta": 1, "num_agencia": "0001", "tipo_titulares": 1, "saldo": 1000.0, "titulares": [ANA], "tipo_conta": 1},
        {"num_conta": 2, "num_agencia": "0001", "tipo_titulares": 2, "saldo": 500.0, "titulares": [ANA, CARLOS], "tipo_conta": 2},
        {"num_conta": 1, "num_agencia": "0002", "tipo_titulares": 1, "saldo": 0.0, "titulares": [CARLOS], "tipo_conta": 3},
    ]


def rodar():
    casos = []
    contas = novas_contas()

    # --- Clientes ---
    casos.append({"descricao": "buscar_cliente acha o primeiro (índice 0)",
                  "resultado": buscar_cliente(CLIENTES, ANA), "esperado": 0})
    casos.append({"descricao": "buscar_cliente aceita CPF com máscara",
                  "resultado": buscar_cliente(CLIENTES, "960.013.389-14"), "esperado": 1})
    casos.append({"descricao": "buscar_cliente inexistente retorna -1",
                  "resultado": buscar_cliente(CLIENTES, MARIANA), "esperado": -1})
    casos.append({"descricao": "procurar_cliente devolve o cliente",
                  "resultado": procurar_cliente(CLIENTES, ANA)["nome"], "esperado": "Ana"})
    casos.append({"descricao": "procurar_cliente inexistente retorna False",
                  "resultado": procurar_cliente(CLIENTES, MARIANA), "esperado": False})
    casos.append({"descricao": "procurar_cliente em lista vazia retorna False",
                  "resultado": procurar_cliente([], ANA), "esperado": False})

    # --- Agências ---
    casos.append({"descricao": "buscar_agencia acha a segunda (índice 1)",
                  "resultado": buscar_agencia(AGENCIAS, "0002"), "esperado": 1})
    casos.append({"descricao": "buscar_agencia inexistente retorna -1",
                  "resultado": buscar_agencia(AGENCIAS, "9999"), "esperado": -1})
    casos.append({"descricao": "procurar_agencia devolve a agência",
                  "resultado": procurar_agencia(AGENCIAS, "0001")["nome_agencia"], "esperado": "Centro"})
    casos.append({"descricao": "procurar_agencia inexistente retorna False",
                  "resultado": procurar_agencia(AGENCIAS, "9999"), "esperado": False})

    # --- Contas ---
    casos.append({"descricao": "verificador_existencia acha conta 2 da agência 0001",
                  "resultado": verificador_existencia(contas, 2, "0001"), "esperado": 1})
    casos.append({"descricao": "Mesmo número em outra agência é outra conta",
                  "resultado": verificador_existencia(contas, 1, "0002"), "esperado": 2})
    casos.append({"descricao": "verificador_existencia inexistente retorna -1",
                  "resultado": verificador_existencia(contas, 5, "0001"), "esperado": -1})
    casos.append({"descricao": "procurar_conta com titular correto devolve a conta",
                  "resultado": procurar_conta(contas, 1, "0001", ANA)["saldo"], "esperado": 1000.0})
    casos.append({"descricao": "procurar_conta com CPF com máscara funciona",
                  "resultado": procurar_conta(contas, 1, "0001", "104.332.181-00")["saldo"], "esperado": 1000.0})
    casos.append({"descricao": "procurar_conta com CPF de não titular retorna -2",
                  "resultado": procurar_conta(contas, 1, "0001", CARLOS), "esperado": -2})
    casos.append({"descricao": "procurar_conta inexistente retorna False",
                  "resultado": procurar_conta(contas, 9, "0001", ANA), "esperado": False})
    casos.append({"descricao": "consultar_saldo de titular",
                  "resultado": consultar_saldo(contas, 2, "0001", CARLOS), "esperado": 500.0})
    casos.append({"descricao": "listar_contas devolve as 3 contas",
                  "resultado": len(listar_contas(contas)), "esperado": 3})
    casos.append({"descricao": "listar_contas vazio retorna False",
                  "resultado": listar_contas([]), "esperado": False})
    casos.append({"descricao": "listar_contas_saldo_positivo ignora saldo zero",
                  "resultado": len(listar_contas_saldo_positivo(contas)), "esperado": 2})
    casos.append({"descricao": "listar_contas_saldo_positivo sem nenhuma retorna False",
                  "resultado": listar_contas_saldo_positivo([contas[2]]), "esperado": False})
    casos.append({"descricao": "Ana é titular de 2 contas",
                  "resultado": len(listar_contas_clientes(contas, ANA)), "esperado": 2})
    casos.append({"descricao": "Carlos (CPF com máscara) é titular de 2 contas",
                  "resultado": len(listar_contas_clientes(contas, "960.013.389-14")), "esperado": 2})
    casos.append({"descricao": "Cliente sem conta retorna False",
                  "resultado": listar_contas_clientes(contas, MARIANA), "esperado": False})
    casos.append({"descricao": "listar_titulares da conta conjunta",
                  "resultado": listar_titulares(contas, 2, "0001"), "esperado": [ANA, CARLOS]})
    casos.append({"descricao": "listar_titulares de conta inexistente retorna False",
                  "resultado": listar_titulares(contas, 9, "0001"), "esperado": False})

    # --- Relatórios ---
    casos.append({"descricao": "montante_banco soma todos os saldos",
                  "resultado": montante_banco(contas), "esperado": 1500.0})
    casos.append({"descricao": "montante_banco sem contas é 0",
                  "resultado": montante_banco([]), "esperado": 0.0})
    casos.append({"descricao": "montante_agencia 0001",
                  "resultado": montante_agencia(contas, "0001"), "esperado": 1500.0})
    casos.append({"descricao": "montante_agencia 0002",
                  "resultado": montante_agencia(contas, "0002"), "esperado": 0.0})
    casos.append({"descricao": "quantidade_contas_agencia 0001",
                  "resultado": quantidade_contas_agencia(contas, "0001"), "esperado": 2})
    casos.append({"descricao": "quantidade_contas_agencia inexistente",
                  "resultado": quantidade_contas_agencia(contas, "9999"), "esperado": 0})
    casos.append({"descricao": "montante_tipo_conta poupança",
                  "resultado": montante_tipo_conta(contas, 2), "esperado": 500.0})
    casos.append({"descricao": "quantidade_tipo_conta salário",
                  "resultado": quantidade_tipo_conta(contas, 3), "esperado": 1})
    casos.append({"descricao": "quantidade_tipo_titulares individuais",
                  "resultado": quantidade_tipo_titulares(contas, 1), "esperado": 2})
    casos.append({"descricao": "quantidade_tipo_titulares conjuntas",
                  "resultado": quantidade_tipo_titulares(contas, 2), "esperado": 1})
    casos.append({"descricao": "menor_saldo",
                  "resultado": menor_saldo(contas)["saldo"], "esperado": 0.0})
    casos.append({"descricao": "maior_saldo",
                  "resultado": maior_saldo(contas)["saldo"], "esperado": 1000.0})
    casos.append({"descricao": "menor_saldo sem contas retorna False",
                  "resultado": menor_saldo([]), "esperado": False})
    casos.append({"descricao": "maior_saldo sem contas retorna False",
                  "resultado": maior_saldo([]), "esperado": False})
    casos.append({"descricao": "saldo_medio",
                  "resultado": saldo_medio(contas), "esperado": 500.0})
    casos.append({"descricao": "saldo_medio sem contas é 0",
                  "resultado": saldo_medio([]), "esperado": 0.0})

    resumo = resumo_bancario(CLIENTES, AGENCIAS, contas)
    casos.append({"descricao": "resumo_bancario: quantidade de clientes",
                  "resultado": resumo["quantidade_clientes"], "esperado": 2})
    casos.append({"descricao": "resumo_bancario: quantidade de agências",
                  "resultado": resumo["quantidade_agencias"], "esperado": 2})
    casos.append({"descricao": "resumo_bancario: quantidade de contas",
                  "resultado": resumo["quantidade_contas"], "esperado": 3})
    casos.append({"descricao": "resumo_bancario: montante total",
                  "resultado": resumo["montante_total"], "esperado": 1500.0})
    casos.append({"descricao": "resumo_bancario: corrente / poupança / salário",
                  "resultado": [resumo["quantidade_corrente"], resumo["quantidade_poupanca"], resumo["quantidade_salario"]],
                  "esperado": [1, 1, 1]})
    casos.append({"descricao": "resumo_bancario: maior e menor saldo",
                  "resultado": [resumo["maior_saldo"], resumo["menor_saldo"]], "esperado": [1000.0, 0.0]})

    vazio = resumo_bancario([], [], [])
    casos.append({"descricao": "resumo_bancario de banco vazio tudo zerado",
                  "resultado": [vazio["quantidade_contas"], vazio["montante_total"], vazio["maior_saldo"], vazio["menor_saldo"], vazio["saldo_medio"]],
                  "esperado": [0, 0.0, 0.0, 0.0, 0.0]})

    print("=== Teste 04: Buscas, listagens e relatórios ===")
    return verificar(casos)


if __name__ == "__main__":
    rodar()
