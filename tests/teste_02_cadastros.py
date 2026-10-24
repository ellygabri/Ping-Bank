# Teste 02 - Cadastros de clientes e agências (clientes.py e agencias.py)
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

from verificacao import verificar
from clientes import cadastrar_cliente, editar_cliente, excluir_cliente, listar_clientes, procurar_cliente
from agencias import cadastrar_agencia, listar_agencias

PESSOAS = [
    ["Ana Beatriz Souza", "104.332.181-00", "(79) 99100-0001", "Rua das Palmeiras, 120, Centro, Aracaju/SE", "14/03/1992", "ana.souza@example.com"],
    ["Carlos Eduardo Lima", "960.013.389-14", "(79) 99100-0002", "Av. Beira Mar, 455, Atalaia, Aracaju/SE", "22/07/1988", "carlos.lima@example.com"],
    ["Mariana Alves Costa", "083.863.794-99", "(79) 99100-0003", "Rua do Sol, 78, Jardins, Aracaju/SE", "05/11/1995", "mariana.costa@example.com"],
    ["João Pedro Santos", "026.542.351-14", "(79) 99100-0004", "Rua Bahia, 310, São José, Aracaju/SE", "30/01/1985", "joao.santos@example.com"],
    ["Fernanda Oliveira Rocha", "161.559.407-89", "(79) 99100-0005", "Av. Hermes Fontes, 900, Salgado Filho, Aracaju/SE", "18/09/1990", "fernanda.rocha@example.com"],
    ["Rafael Menezes Barros", "816.184.959-50", "(79) 99100-0006", "Rua Sergipe, 66, Siqueira Campos, Aracaju/SE", "09/06/1983", "rafael.barros@example.com"],
    ["Juliana Ferreira Dias", "310.341.316-56", "(79) 99100-0007", "Rua Pernambuco, 215, Getúlio Vargas, Aracaju/SE", "27/12/1998", "juliana.dias@example.com"],
    ["Lucas Gabriel Martins", "475.255.341-44", "(79) 99100-0008", "Av. Rio Branco, 1500, Centro, Aracaju/SE", "12/04/2000", "lucas.martins@example.com"],
    ["Camila Ribeiro Nunes", "928.327.648-51", "(79) 99100-0009", "Rua Lagarto, 42, Santo Antônio, Aracaju/SE", "03/08/1993", "camila.nunes@example.com"],
    ["Pedro Henrique Araújo", "350.305.641-60", "(79) 99100-0010", "Rua Itabaiana, 188, Centro, Aracaju/SE", "25/02/1979", "pedro.araujo@example.com"],
]


def cadastrar_todos(clientes):
    # Cadastra as 10 pessoas e devolve a lista com os resultados
    resultados = []
    for p in PESSOAS:
        resultados.append(cadastrar_cliente(clientes, p[0], p[1], p[2], p[3], p[4], p[5]))
    return resultados


def rodar():
    casos = []
    clientes = []

    # --- Cadastro de clientes ---
    resultados = cadastrar_todos(clientes)
    esperado = []
    for i in range(10):
        esperado.append(1)
    casos.append({"descricao": "Cadastro das 10 pessoas retorna 1 em todas",
                  "resultado": resultados, "esperado": esperado})
    casos.append({"descricao": "Lista fica com 10 clientes",
                  "resultado": len(clientes), "esperado": 10})
    casos.append({"descricao": "CPF é guardado sem máscara",
                  "resultado": clientes[0]["cpf"], "esperado": "10433218100"})

    p = PESSOAS[0]
    casos.append({"descricao": "CPF repetido (com máscara) retorna 0",
                  "resultado": cadastrar_cliente(clientes, p[0], p[1], p[2], p[3], p[4], p[5]), "esperado": 0})
    casos.append({"descricao": "CPF repetido (sem máscara) retorna 0",
                  "resultado": cadastrar_cliente(clientes, p[0], "10433218100", p[2], p[3], p[4], p[5]), "esperado": 0})
    casos.append({"descricao": "CPF repetido não aumenta a lista",
                  "resultado": len(clientes), "esperado": 10})
    casos.append({"descricao": "CPF inválido retorna -2",
                  "resultado": cadastrar_cliente(clientes, "Teste", "111.111.111-11", "1", "Rua", "01/01/2000", "t@example.com"), "esperado": -2})

    # Cada campo vazio deve retornar -1
    campos = ["nome", "cpf", "contato", "endereco", "data_nascimento", "email"]
    for posicao in range(6):
        dados = ["Teste", "529.982.247-25", "(79) 99999-0000", "Rua Teste, 1", "01/01/2000", "teste@example.com"]
        dados[posicao] = ""
        resultado = cadastrar_cliente([], dados[0], dados[1], dados[2], dados[3], dados[4], dados[5])
        casos.append({"descricao": "Campo vazio (" + campos[posicao] + ") retorna -1",
                      "resultado": resultado, "esperado": -1})

    casos.append({"descricao": "Campo só com espaços retorna -1",
                  "resultado": cadastrar_cliente([], "   ", "529.982.247-25", "1", "Rua", "01/01/2000", "t@example.com"), "esperado": -1})

    # --- Listagem ordenada por nome ---
    ordenados = listar_clientes(clientes)
    nomes = []
    for c in ordenados:
        nomes.append(c["nome"])
    casos.append({"descricao": "listar_clientes ordena por nome (A-Z)",
                  "resultado": nomes[0] + " | " + nomes[9],
                  "esperado": "Ana Beatriz Souza | Rafael Menezes Barros"})
    casos.append({"descricao": "listar_clientes vazio retorna False",
                  "resultado": listar_clientes([]), "esperado": False})

    # --- Edição ---
    casos.append({"descricao": "editar_cliente altera o contato (retorna 1)",
                  "resultado": editar_cliente(clientes, "104.332.181-00", "contato", "(79) 98888-7777"), "esperado": 1})
    casos.append({"descricao": "contato foi realmente alterado",
                  "resultado": procurar_cliente(clientes, "10433218100")["contato"], "esperado": "(79) 98888-7777"})
    casos.append({"descricao": "editar_cliente com CPF inexistente retorna -1",
                  "resultado": editar_cliente(clientes, "529.982.247-25", "nome", "X"), "esperado": -1})
    casos.append({"descricao": "editar_cliente com valor vazio retorna 0",
                  "resultado": editar_cliente(clientes, "104.332.181-00", "nome", "  "), "esperado": 0})
    casos.append({"descricao": "editar_cliente não permite alterar o CPF (retorna -2)",
                  "resultado": editar_cliente(clientes, "104.332.181-00", "cpf", "52998224725"), "esperado": -2})

    # --- Exclusão ---
    contas = [{"titulares": ["10433218100"]}]
    casos.append({"descricao": "excluir_cliente que é titular de conta retorna 0",
                  "resultado": excluir_cliente(clientes, contas, "104.332.181-00"), "esperado": 0})
    casos.append({"descricao": "excluir_cliente sem conta retorna 1",
                  "resultado": excluir_cliente(clientes, contas, "960.013.389-14"), "esperado": 1})
    casos.append({"descricao": "excluir_cliente inexistente retorna -1",
                  "resultado": excluir_cliente(clientes, contas, "960.013.389-14"), "esperado": -1})
    casos.append({"descricao": "Lista fica com 9 clientes após a exclusão",
                  "resultado": len(clientes), "esperado": 9})

    # --- Agências ---
    agencias = []
    casos.append({"descricao": "cadastrar_agencia nova retorna 1",
                  "resultado": cadastrar_agencia(agencias, "0001", "Agência Centro"), "esperado": 1})
    casos.append({"descricao": "cadastrar_agencia segunda retorna 1",
                  "resultado": cadastrar_agencia(agencias, "0002", "Agência Atalaia"), "esperado": 1})
    casos.append({"descricao": "cadastrar_agencia repetida retorna 0",
                  "resultado": cadastrar_agencia(agencias, "0001", "Outra"), "esperado": 0})
    casos.append({"descricao": "cadastrar_agencia com número vazio retorna -1",
                  "resultado": cadastrar_agencia(agencias, "", "Sem número"), "esperado": -1})
    casos.append({"descricao": "cadastrar_agencia com nome vazio retorna -1",
                  "resultado": cadastrar_agencia(agencias, "0003", " "), "esperado": -1})
    casos.append({"descricao": "listar_agencias ordena por nome",
                  "resultado": listar_agencias(agencias)[0]["nome_agencia"], "esperado": "Agência Atalaia"})
    casos.append({"descricao": "listar_agencias vazio retorna False",
                  "resultado": listar_agencias([]), "esperado": False})

    print("=== Teste 02: Cadastros ===")
    return verificar(casos)


if __name__ == "__main__":
    rodar()
