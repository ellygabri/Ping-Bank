# Teste 01 - Validação de CPF (clientes.py)
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from verificacao import verificar
from clientes import validar_cpf, normalizar_cpf

CPFS_VALIDOS = [
    "104.332.181-00", "960.013.389-14", "083.863.794-99", "026.542.351-14",
    "161.559.407-89", "816.184.959-50", "310.341.316-56", "475.255.341-44",
    "928.327.648-51", "350.305.641-60",
]

CPFS_INVALIDOS = [
    ["111.111.111-11", "todos os dígitos iguais"],
    ["000.000.000-00", "somente zeros"],
    ["104.332.181-01", "último dígito errado"],
    ["104.332.181-10", "penúltimo dígito errado"],
    ["123.456.789-00", "dígitos verificadores inválidos"],
    ["1043321810", "faltando um dígito"],
    ["104332181000", "um dígito a mais"],
    ["", "vazio"],
    ["abc.def.ghi-jk", "letras"],
    ["104.332.18a-00", "uma letra no meio"],
    ["104 332 181 00", "espaços no lugar da máscara"],
]


def rodar():
    casos = []

    # CPFs válidos, com máscara e sem máscara
    for cpf in CPFS_VALIDOS:
        casos.append({"descricao": "CPF válido com máscara: " + cpf,
                      "resultado": validar_cpf(cpf), "esperado": True})
        casos.append({"descricao": "CPF válido sem máscara: " + cpf,
                      "resultado": validar_cpf(normalizar_cpf(cpf)), "esperado": True})

    # CPF que já está no ping_bank_dados.json
    casos.append({"descricao": "CPF do cliente que já vem no JSON",
                  "resultado": validar_cpf("04190910503"), "esperado": True})

    # CPFs inválidos
    for item in CPFS_INVALIDOS:
        casos.append({"descricao": "CPF inválido (" + item[1] + "): " + item[0],
                      "resultado": validar_cpf(item[0]), "esperado": False})

    # Todos os dígitos repetidos de 0 a 9
    for numero in range(10):
        repetido = str(numero) * 11
        casos.append({"descricao": "CPF repetido: " + repetido,
                      "resultado": validar_cpf(repetido), "esperado": False})

    # normalizar_cpf
    casos.append({"descricao": "normalizar_cpf remove pontos e traço",
                  "resultado": normalizar_cpf("104.332.181-00"), "esperado": "10433218100"})
    casos.append({"descricao": "normalizar_cpf mantém CPF já limpo",
                  "resultado": normalizar_cpf("10433218100"), "esperado": "10433218100"})
    casos.append({"descricao": "normalizar_cpf com texto vazio",
                  "resultado": normalizar_cpf(""), "esperado": ""})

    print("=== Teste 01: CPF ===")
    return verificar(casos)


if __name__ == "__main__":
    rodar()
