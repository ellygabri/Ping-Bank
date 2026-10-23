import json

#Função responsável por carregar os dados armazenados no JSON
def carregar_dados():
    arquivo = open("ping_bank_dados.json", "r", encoding= "utf-8")

    dados = json.load(arquivo)

    arquivo.close()

    clientes = dados["clientes"]
    agencias = dados["agencias"]
    contas = dados["contas"]

    return clientes, agencias, contas

#Função responsável para salvar os dados no JSON
def salvar_dados(clientes,agencias,contas):
    dados = {"clientes": clientes, "agencias": agencias, "contas": contas}
    arquivo = open("ping_bank_dados.json", "w", encoding = "utf-8")

    json.dump(dados,arquivo, ensure_ascii = False, indent = 4)

    arquivo.close()