#Função de apoio para retirar pontos e traço do CPF
def normalizar_cpf(cpf):
    cpf_normalizado = ""

    for caractere in cpf:
        if caractere != "." and caractere != "-":
            cpf_normalizado = cpf_normalizado + caractere

    return cpf_normalizado

#Classe responsável por representar um cliente do banco
class Cliente:
    def __init__(self, nome, cpf, contato, endereco, data_nascimento, email):
        self.nome = nome
        self.cpf = normalizar_cpf(cpf)
        self.contato = contato
        self.endereco = endereco
        self.data_nascimento = data_nascimento
        self.email = email

        #Não permite criar um cliente com CPF inválido
        if not self.validar_cpf():
            raise ValueError("CPF inválido.")
        
        #Garantindo que todos os dados obrigatórios tenham sido preenchidos
        if (not self.nome.strip() or not self.contato.strip() or not self.endereco.strip() or not self.data_nascimento.strip() or not self.email.strip()):
            raise ValueError("Todos os campos do cliente são obrigatórios.")

    #Método responsável por validar o CPF do cliente
    def validar_cpf(self):
        cpf = self.cpf

        #Verificando se o CPF possui 11 digitos, como é o padrão
        if len(cpf) != 11:
            return False

        #Verificando se todos os caracteres são números
        numeros = "0123456789"

        for caractere in cpf:
            if caractere not in numeros:
                return False

        #Verificando se todos os números do CPF são iguais
        todos_iguais = True

        for i in range(1, len(cpf)):
            if cpf[i] != cpf[0]:
                todos_iguais = False

        if todos_iguais == True:
             return False
        
        # Cálculo do primeiro dígito verificador
        soma = 0
        peso = 10

        for i in range(9):
             soma += int(cpf[i]) * peso
             peso -= 1

        resto = soma % 11

        if resto < 2:
            primeiro_digito = 0

        else:
            primeiro_digito = 11 - resto 

        if primeiro_digito != int(cpf[9]):
           return False
        
        # Cálculo do segundo dígito verificador
        soma = 0
        peso = 11

        for i in range(10):
            soma += int(cpf[i]) * peso
            peso -= 1

        resto = soma % 11

        if resto < 2:
            segundo_digito = 0

        else:
            segundo_digito = 11 - resto

        if segundo_digito != int(cpf[10]):
            return False

        return True
        
    #Método responsável por editar os dados do cliente
    #OBS: O CPF não pode ser alterado
    def editar_dado(self, campo, nova_info):
        if campo not in("nome", "contato", "endereco", "data_nascimento", "email"):
            return -2
        if not isinstance(nova_info, str) or nova_info.strip() == "":
            return 0
        
        nova_info = nova_info.strip()

        if campo == "nome":
            self.nome = nova_info
        elif campo == "contato":
            self.contato = nova_info
        elif campo == "endereco":
            self.endereco = nova_info
        elif campo == "data_nascimento":
            self.data_nascimento = nova_info
        elif campo == "email":
            self.email = nova_info
        
        return 1