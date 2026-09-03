"""
Etapa 1:
Criação da função para cadastro do cliente
"""

def cadastrar_cliente (nome, cpf, num_contato, endereco, data_nascimento, email):
    if nome.strip() == "" or cpf.strip() == "" or num_contato.strip() == "" or endereco.strip() == "" or data_nascimento.strip() == "" or email.strip() == "":
        return False
    else:
        dados_cliente = (nome, cpf, num_contato, endereco, data_nascimento, email)
        return dados_cliente
