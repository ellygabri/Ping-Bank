from contas import ContaCorrente, ContaPoupanca


class ResumoBancario:
    def __init__(self, agencia):
        clientes = agencia.listar_clientes()
        contas = agencia.listar_contas()

        self.quantidade_clientes = len(clientes)
        self.quantidade_contas = len(contas)
        self.montante_total = agencia.montante()

        self.quantidade_corrente = 0
        self.quantidade_poupanca = 0
        self.montante_corrente = 0.0
        self.montante_poupanca = 0.0

        self.menor_saldo = 0.0
        self.maior_saldo = 0.0
        self.saldo_medio = 0.0

        for conta in contas:
            if isinstance(conta, ContaCorrente):
                self.quantidade_corrente += 1
                self.montante_corrente += conta.saldo
            elif isinstance(conta, ContaPoupanca):
                self.quantidade_poupanca += 1
                self.montante_poupanca += conta.saldo

        if len(contas) > 0:
            self.menor_saldo = contas[0].saldo
            self.maior_saldo = contas[0].saldo

            for conta in contas:
                if conta.saldo < self.menor_saldo:
                    self.menor_saldo = conta.saldo

                if conta.saldo > self.maior_saldo:
                    self.maior_saldo = conta.saldo

            self.saldo_medio = self.montante_total / len(contas)