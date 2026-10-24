# Resultados dos testes - Ping Bank

Testes automatizados das funções do sistema, escritos só com listas, dicionários,
`for` e `if`, usando `verificacao.py`.

## Como executar

Na pasta raiz do projeto, com o `.venv` ativado:

```bash
python tests/rodar_todos.py
```

Para rodar um teste só:

```bash
python tests/teste_01_cpf.py
```

Os testes não alteram o `ping_bank_dados.json` (o teste 05 usa uma pasta temporária).

## Resumo

| Arquivo | O que testa | Casos | Resultado |
|---------|-------------|:-----:|-----------|
| `teste_01_cpf.py` | Validação e normalização de CPF | 45 | 45 passaram |
| `teste_02_cadastros.py` | Cadastro, edição e exclusão de clientes; cadastro de agências | 32 | 32 passaram |
| `teste_03_tipos_conta.py` | Contas corrente, poupança e salário; depósito, saque, transferência, titulares | 61 | 61 passaram |
| `teste_04_buscas.py` | Buscas, listagens e relatórios | 50 | 50 passaram |
| `teste_05_json.py` | Salvar e carregar dados no JSON | 9 | 9 passaram |
| **Total** | | **197** | **197 passaram, 0 falharam** |

## Dados de teste

Os 10 clientes usados são fictícios, com CPFs válidos (dígitos verificadores corretos).
E-mails usam o domínio `example.com`.

## Códigos de retorno testados

- `cadastrar_cliente`: 1 cadastrado, 0 CPF repetido, -1 campo vazio, -2 CPF inválido
- `criar_conta`: -1 agência, -2 tipo de titulares, -3 saldo negativo, -4 quantidade de titulares, -5 titular não cadastrado, -6 tipo de conta, -7 titular repetido
- `deposito`: 1 ok, 0 valor inválido, -1 conta, -2 CPF não titular, -4 conta salário
- `saque`: 1 ok, 0 valor inválido, -1 conta, -2 CPF não titular, -3 saldo insuficiente
- `transferencia`: 1 ok, 0 valor inválido, -1 origem, -2 CPF, -3 destino, -4 mesma conta, -5 saldo insuficiente, -6 origem é conta salário
