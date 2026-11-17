from clientes import normalizar_cpf


class Agencia:
    def __init__(self, numero, nome=""):
        self.numero = str(numero)
        self.nome = nome.strip()
        self.clientes = []
        self.contas = []

    def __str__(self):
        return f"Agência {self.numero} - {self.nome}"

    def adicionar_cliente(self, cliente):
        if self.buscar_cliente(cliente.cpf) is not None:
            return False

        self.clientes.append(cliente)
        return True

    def remover_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)

        if cliente is None:
            return -1

        for conta in self.contas:
            if conta.cliente == cliente:
                return 0

        self.clientes.remove(cliente)
        return 1

    def adicionar_conta(self, conta):
        if self.buscar_conta(conta.num_conta) is not None:
            return False

        self.contas.append(conta)
        return True

    def remover_conta(self, numero_conta):
        conta = self.buscar_conta(numero_conta)

        if conta is None:
            return False

        self.contas.remove(conta)
        return True

    def buscar_cliente(self, cpf):
        cpf = normalizar_cpf(cpf)

        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente

        return None

    def buscar_conta(self, numero_conta):
        for conta in self.contas:
            if str(conta.num_conta) == str(numero_conta).strip():
                return conta

        return None

    def listar_clientes(self):
        return self.clientes

    def listar_contas(self):
        return self.contas

    def listar_contas_cliente(self, cpf):
        cliente = self.buscar_cliente(cpf)
        contas_cliente = []

        if cliente is None:
            return contas_cliente

        for conta in self.contas:
            if conta.cliente == cliente:
                contas_cliente.append(conta)

        return contas_cliente

    def listar_contas_positivas(self):
        contas_positivas = []

        for conta in self.contas:
            if conta.saldo > 0:
                contas_positivas.append(conta)

        return contas_positivas

    def proximo_numero_conta(self):
        maior_numero = 0

        for conta in self.contas:
            if conta.num_conta > maior_numero:
                maior_numero = conta.num_conta

        return maior_numero + 1

    def quantidade_contas(self):
        return len(self.contas)

    def montante(self):
        total = 0.0

        for conta in self.contas:
            total += conta.saldo

        return total