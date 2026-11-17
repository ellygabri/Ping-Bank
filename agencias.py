from clientes import normalizar_cpf, Cliente


class Agencia:
    """Núcleo de agregação do banco: guarda os clientes e as contas da agência
    e centraliza as buscas e os cadastros."""

    def __init__(self, numero, nome=""):
        self.numero = str(numero)
        self.nome = nome
        self.clientes = []
        self.contas = []

    # Apelidos usados pelos templates HTML 
    @property
    def num_agencia(self):
        return self.numero

    @property
    def nome_agencia(self):
        return self.nome

    def __str__(self):
        return f"Agência {self.numero} - {self.nome}"

    #  Cadastros 
    def adicionar_cliente(self, cliente):
        # Evita o mesmo CPF duas vezes 
        if self.buscar_cliente(cliente.cpf) is not None:
            return False
        self.clientes.append(cliente)
        return True

    def adicionar_conta(self, conta):
        # Evita o mesmo número de conta duas vezes dentro da agência
        if self.buscar_conta(conta.num_conta) is not None:
            return False
        self.contas.append(conta)
        return True

    #  Buscas 
    def buscar_cliente(self, cpf):
        cpf = normalizar_cpf(str(cpf))
        for cliente in self.clientes:
            if normalizar_cpf(str(cliente.cpf)) == cpf:
                return cliente
        return None

    def buscar_conta(self, numero_conta):
        # O número vem como int do json e como str dos formulários web
        for conta in self.contas:
            if str(conta.num_conta) == str(numero_conta).strip():
                return conta
        return None

    #  Listagens e totais 
    def listar_contas(self):
        return self.contas

    def listar_clientes(self):
        return self.clientes

    def quantidade_contas(self):
        return len(self.contas)

    def montante(self):
        total = 0.0
        for conta in self.contas:
            total += conta.saldo
        return total
