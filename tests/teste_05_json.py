# Teste 05 - Salvar e carregar dados no JSON (dados.py)
# IMPORTANTE: o teste trabalha em uma pasta temporária,
# então o ping_bank_dados.json de verdade NÃO é alterado.
import os
import sys
import shutil
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from verificacao import verificar
from dados import carregar_dados, salvar_dados


def rodar():
    casos = []

    pasta_original = os.getcwd()
    pasta_temporaria = tempfile.mkdtemp()
    os.chdir(pasta_temporaria)

    clientes = [{"nome": "João Araújo", "cpf": "10433218100", "contato": "(79) 99100-0001",
                 "endereco": "Rua das Palmeiras, 120", "data_nascimento": "14/03/1992",
                 "email": "joao@example.com"}]
    agencias = [{"num_agencia": "0001", "nome_agencia": "Agência Centro"}]
    contas = [{"num_conta": 1, "num_agencia": "0001", "tipo_titulares": 1,
               "saldo": 1234.56, "titulares": ["10433218100"], "tipo_conta": 1}]

    # Salva e carrega de volta
    salvar_dados(clientes, agencias, contas)
    casos.append({"descricao": "salvar_dados cria o arquivo JSON",
                  "resultado": os.path.exists("ping_bank_dados.json"), "esperado": True})

    c, a, ct = carregar_dados()
    casos.append({"descricao": "Clientes carregados são iguais aos salvos",
                  "resultado": c, "esperado": list(clientes)})
    casos.append({"descricao": "Agências carregadas são iguais às salvas",
                  "resultado": a, "esperado": list(agencias)})
    casos.append({"descricao": "Contas carregadas são iguais às salvas",
                  "resultado": ct, "esperado": list(contas)})
    casos.append({"descricao": "Acentos são preservados (ensure_ascii = False)",
                  "resultado": c[0]["nome"], "esperado": "João Araújo"})
    casos.append({"descricao": "Saldo decimal é preservado",
                  "resultado": ct[0]["saldo"], "esperado": 1234.56})

    # O arquivo guarda os acentos de verdade, e não códigos \u00e3
    arquivo = open("ping_bank_dados.json", "r", encoding="utf-8")
    texto = arquivo.read()
    arquivo.close()
    casos.append({"descricao": "Arquivo contém o texto 'João' legível",
                  "resultado": "João" in texto, "esperado": True})

    # Salvar de novo sobrescreve
    clientes.append({"nome": "Maria", "cpf": "96001338914", "contato": "2", "endereco": "B",
                     "data_nascimento": "01/01/1990", "email": "m@example.com"})
    salvar_dados(clientes, agencias, contas)
    c2, a2, ct2 = carregar_dados()
    casos.append({"descricao": "Salvar de novo atualiza os clientes (2)",
                  "resultado": len(c2), "esperado": 2})

    # Banco vazio
    salvar_dados([], [], [])
    c3, a3, ct3 = carregar_dados()
    casos.append({"descricao": "Banco vazio é salvo e carregado como listas vazias",
                  "resultado": [c3, a3, ct3], "esperado": [[], [], []]})

    # Volta para a pasta original e apaga a temporária
    os.chdir(pasta_original)
    shutil.rmtree(pasta_temporaria)

    print("=== Teste 05: JSON ===")
    return verificar(casos)


if __name__ == "__main__":
    rodar()
