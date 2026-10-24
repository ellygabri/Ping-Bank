# Teste 03 - Tipos de conta e operações (contas.py)
# Tipos de conta: 1 = corrente, 2 = poupança, 3 = salário
# Tipos de titulares: 1 = individual, 2 = conjunta
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from verificacao import verificar
from clientes import cadastrar_cliente
from agencias import cadastrar_agencia
from contas import (criar_conta, deposito, saque, transferencia, calculo_poupanca,
                    adicionar_titular, remover_titular, substituir_titular,
                    excluir_conta, consultar_saldo)

ANA = "104.332.181-00"
CARLOS = "960.013.389-14"
MARIANA = "083.863.794-99"
JOAO = "026.542.351-14"
FORA = "529.982.247-25"  # CPF válido, mas não cadastrado


def montar_banco():
    # Cria um banco novo na memória: 4 clientes e 1 agência
    clientes = []
    agencias = []
    contas = []
    cadastrar_cliente(clientes, "Ana", ANA, "1", "Rua A", "01/01/1990", "a@example.com")
    cadastrar_cliente(clientes, "Carlos", CARLOS, "2", "Rua B", "01/01/1991", "b@example.com")
    cadastrar_cliente(clientes, "Mariana", MARIANA, "3", "Rua C", "01/01/1992", "c@example.com")
    cadastrar_cliente(clientes, "Joao", JOAO, "4", "Rua D", "01/01/1993", "d@example.com")
    cadastrar_agencia(agencias, "0001", "Centro")
    return clientes, agencias, contas


def abrir(contas, clientes, agencias, tipo_titulares, saldo, titulares, tipo_conta):
    # Cria e guarda a conta; devolve o resultado de criar_conta
    conta = criar_conta(contas, clientes, agencias, "0001", tipo_titulares, saldo, titulares, tipo_conta)
    if type(conta) == dict:
        contas.append(conta)
    return conta


def rodar():
    casos = []
    clientes, agencias, contas = montar_banco()

    # --- Criação ---
    corrente = abrir(contas, clientes, agencias, 1, 1000.0, [ANA], 1)
    casos.append({"descricao": "Conta corrente é criada com número 1",
                  "resultado": corrente["num_conta"], "esperado": 1})
    poupanca = abrir(contas, clientes, agencias, 1, 1000.0, [CARLOS], 2)
    casos.append({"descricao": "Conta poupança é criada com número 2",
                  "resultado": poupanca["num_conta"], "esperado": 2})
    salario = abrir(contas, clientes, agencias, 1, 500.0, [MARIANA], 3)
    casos.append({"descricao": "Conta salário é criada com número 3",
                  "resultado": salario["num_conta"], "esperado": 3})
    conjunta = abrir(contas, clientes, agencias, 2, 0.0, [ANA, JOAO], 1)
    casos.append({"descricao": "Conta conjunta guarda os 2 titulares",
                  "resultado": len(conjunta["titulares"]), "esperado": 2})
    casos.append({"descricao": "Titulares são guardados sem máscara",
                  "resultado": conjunta["titulares"][0], "esperado": "10433218100"})

    # Códigos de erro da criação
    casos.append({"descricao": "criar_conta com agência inexistente retorna -1",
                  "resultado": criar_conta(contas, clientes, agencias, "9999", 1, 0.0, [ANA], 1), "esperado": -1})
    casos.append({"descricao": "criar_conta com tipo_titulares inválido retorna -2",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 3, 0.0, [ANA], 1), "esperado": -2})
    casos.append({"descricao": "criar_conta com saldo negativo retorna -3",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 1, -1.0, [ANA], 1), "esperado": -3})
    casos.append({"descricao": "individual com 2 titulares retorna -4",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 1, 0.0, [ANA, JOAO], 1), "esperado": -4})
    casos.append({"descricao": "conjunta com 1 titular retorna -4",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 2, 0.0, [ANA], 1), "esperado": -4})
    casos.append({"descricao": "titular não cadastrado retorna -5",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 1, 0.0, [FORA], 1), "esperado": -5})
    casos.append({"descricao": "tipo de conta inválido retorna -6",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 1, 0.0, [ANA], 4), "esperado": -6})
    casos.append({"descricao": "titular repetido na conta retorna -7",
                  "resultado": criar_conta(contas, clientes, agencias, "0001", 2, 0.0, [ANA, ANA], 1), "esperado": -7})

    # --- Depósito ---
    casos.append({"descricao": "Depósito na corrente retorna 1",
                  "resultado": deposito(contas, 1, "0001", ANA, 200.0), "esperado": 1})
    casos.append({"descricao": "Saldo da corrente passa a 1200",
                  "resultado": consultar_saldo(contas, 1, "0001", ANA), "esperado": 1200.0})
    casos.append({"descricao": "Depósito na poupança retorna 1",
                  "resultado": deposito(contas, 2, "0001", CARLOS, 100.0), "esperado": 1})
    casos.append({"descricao": "Depósito na conta salário é bloqueado (-4)",
                  "resultado": deposito(contas, 3, "0001", MARIANA, 100.0), "esperado": -4})
    casos.append({"descricao": "Depósito com valor zero retorna 0",
                  "resultado": deposito(contas, 1, "0001", ANA, 0), "esperado": 0})
    casos.append({"descricao": "Depósito com valor negativo retorna 0",
                  "resultado": deposito(contas, 1, "0001", ANA, -50.0), "esperado": 0})
    casos.append({"descricao": "Depósito em conta inexistente retorna -1",
                  "resultado": deposito(contas, 99, "0001", ANA, 10.0), "esperado": -1})
    casos.append({"descricao": "Depósito com CPF que não é titular retorna -2",
                  "resultado": deposito(contas, 1, "0001", CARLOS, 10.0), "esperado": -2})

    # --- Saque ---
    casos.append({"descricao": "Saque na corrente retorna 1",
                  "resultado": saque(contas, 1, "0001", ANA, 200.0), "esperado": 1})
    casos.append({"descricao": "Saldo da corrente volta a 1000",
                  "resultado": consultar_saldo(contas, 1, "0001", ANA), "esperado": 1000.0})
    casos.append({"descricao": "Saque maior que o saldo retorna -3",
                  "resultado": saque(contas, 1, "0001", ANA, 5000.0), "esperado": -3})
    casos.append({"descricao": "Saque de todo o saldo é permitido",
                  "resultado": saque(contas, 3, "0001", MARIANA, 500.0), "esperado": 1})
    casos.append({"descricao": "Saldo da conta salário fica zerado",
                  "resultado": consultar_saldo(contas, 3, "0001", MARIANA), "esperado": 0.0})
    casos.append({"descricao": "Saque com valor zero retorna 0",
                  "resultado": saque(contas, 1, "0001", ANA, 0), "esperado": 0})
    casos.append({"descricao": "Saque com CPF errado retorna -2",
                  "resultado": saque(contas, 1, "0001", CARLOS, 10.0), "esperado": -2})
    casos.append({"descricao": "Saque em conta inexistente retorna -1",
                  "resultado": saque(contas, 99, "0001", ANA, 10.0), "esperado": -1})

    # --- Transferência (corrente 1 -> poupança 2) ---
    casos.append({"descricao": "Transferência corrente -> poupança retorna 1",
                  "resultado": transferencia(contas, 1, "0001", ANA, 2, "0001", 300.0), "esperado": 1})
    casos.append({"descricao": "Origem perdeu 300 (700)",
                  "resultado": consultar_saldo(contas, 1, "0001", ANA), "esperado": 700.0})
    casos.append({"descricao": "Destino ganhou 300 (1400)",
                  "resultado": consultar_saldo(contas, 2, "0001", CARLOS), "esperado": 1400.0})
    casos.append({"descricao": "Transferência com origem inexistente retorna -1",
                  "resultado": transferencia(contas, 99, "0001", ANA, 2, "0001", 10.0), "esperado": -1})
    casos.append({"descricao": "Transferência com CPF errado retorna -2",
                  "resultado": transferencia(contas, 1, "0001", CARLOS, 2, "0001", 10.0), "esperado": -2})
    casos.append({"descricao": "Transferência com destino inexistente retorna -3",
                  "resultado": transferencia(contas, 1, "0001", ANA, 99, "0001", 10.0), "esperado": -3})
    casos.append({"descricao": "Transferência para a própria conta retorna -4",
                  "resultado": transferencia(contas, 1, "0001", ANA, 1, "0001", 10.0), "esperado": -4})
    casos.append({"descricao": "Transferência acima do saldo retorna -5",
                  "resultado": transferencia(contas, 1, "0001", ANA, 2, "0001", 99999.0), "esperado": -5})
    casos.append({"descricao": "Transferência com valor zero retorna 0",
                  "resultado": transferencia(contas, 1, "0001", ANA, 2, "0001", 0), "esperado": 0})
    casos.append({"descricao": "Transferir a partir da conta salário é bloqueado (-6)",
                  "resultado": transferencia(contas, 3, "0001", MARIANA, 1, "0001", 10.0), "esperado": -6})

    # --- Poupança ---
    nova = abrir(contas, clientes, agencias, 1, 1000.0, [JOAO], 2)
    casos.append({"descricao": "Poupança de 1000 rende 0,5% ao mês (2 meses = 1010)",
                  "resultado": round(calculo_poupanca(nova["num_conta"], "0001", contas, 2), 2), "esperado": 1010.0})
    casos.append({"descricao": "Rendimento da poupança fica salvo na conta",
                  "resultado": round(nova["saldo"], 2), "esperado": 1010.0})
    casos.append({"descricao": "calculo_poupanca em conta inexistente retorna -1",
                  "resultado": calculo_poupanca(99, "0001", contas, 2), "esperado": -1})
    casos.append({"descricao": "calculo_poupanca em conta corrente retorna -2",
                  "resultado": calculo_poupanca(1, "0001", contas, 2), "esperado": -2})
    casos.append({"descricao": "calculo_poupanca com 0 meses retorna -3",
                  "resultado": calculo_poupanca(nova["num_conta"], "0001", contas, 0), "esperado": -3})

    # --- Titulares (conta corrente 1 é individual da Ana) ---
    casos.append({"descricao": "adicionar_titular retorna 1",
                  "resultado": adicionar_titular(contas, clientes, 1, "0001", ANA, JOAO), "esperado": 1})
    casos.append({"descricao": "Conta passa a ser conjunta (tipo_titulares = 2)",
                  "resultado": contas[0]["tipo_titulares"], "esperado": 2})
    casos.append({"descricao": "adicionar_titular repetido retorna 0",
                  "resultado": adicionar_titular(contas, clientes, 1, "0001", ANA, JOAO), "esperado": 0})
    casos.append({"descricao": "adicionar_titular não cadastrado retorna -3",
                  "resultado": adicionar_titular(contas, clientes, 1, "0001", ANA, FORA), "esperado": -3})
    casos.append({"descricao": "adicionar_titular com CPF de validação errado retorna -2",
                  "resultado": adicionar_titular(contas, clientes, 1, "0001", MARIANA, CARLOS), "esperado": -2})
    casos.append({"descricao": "substituir_titular retorna 1",
                  "resultado": substituir_titular(contas, clientes, 1, "0001", ANA, JOAO, CARLOS), "esperado": 1})
    casos.append({"descricao": "substituir por quem já é titular retorna -4",
                  "resultado": substituir_titular(contas, clientes, 1, "0001", ANA, CARLOS, ANA), "esperado": -4})
    casos.append({"descricao": "substituir titular que não está na conta retorna 0",
                  "resultado": substituir_titular(contas, clientes, 1, "0001", ANA, MARIANA, JOAO), "esperado": 0})
    casos.append({"descricao": "remover_titular retorna 1",
                  "resultado": remover_titular(contas, 1, "0001", ANA, CARLOS), "esperado": 1})
    casos.append({"descricao": "Conta volta a ser individual (tipo_titulares = 1)",
                  "resultado": contas[0]["tipo_titulares"], "esperado": 1})
    casos.append({"descricao": "Não pode remover o único titular (-3)",
                  "resultado": remover_titular(contas, 1, "0001", ANA, ANA), "esperado": -3})
    casos.append({"descricao": "remover quem não é titular retorna 0",
                  "resultado": remover_titular(contas, 1, "0001", ANA, MARIANA), "esperado": 0})

    # --- Exclusão de conta ---
    casos.append({"descricao": "excluir_conta com saldo diferente de zero retorna 0",
                  "resultado": excluir_conta(contas, 1, "0001", ANA), "esperado": 0})
    casos.append({"descricao": "excluir_conta com CPF errado retorna -2",
                  "resultado": excluir_conta(contas, 3, "0001", CARLOS), "esperado": -2})
    quantidade_antes = len(contas)
    casos.append({"descricao": "excluir_conta com saldo zero retorna 1",
                  "resultado": excluir_conta(contas, 3, "0001", MARIANA), "esperado": 1})
    casos.append({"descricao": "Conta excluída sai da lista",
                  "resultado": len(contas), "esperado": quantidade_antes - 1})
    casos.append({"descricao": "excluir_conta inexistente retorna -1",
                  "resultado": excluir_conta(contas, 3, "0001", MARIANA), "esperado": -1})

    print("=== Teste 03: Tipos de conta e operações ===")
    return verificar(casos)


if __name__ == "__main__":
    rodar()
