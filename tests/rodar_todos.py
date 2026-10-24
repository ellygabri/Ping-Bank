# Executa todos os testes de uma vez.
# Uso (na pasta raiz do projeto): python tests/rodar_todos.py
import os
import sys

PASTA_TESTES = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PASTA_TESTES)

import teste_01_cpf
import teste_02_cadastros
import teste_03_tipos_conta
import teste_04_buscas
import teste_05_json

total_falhas = 0
total_falhas += teste_01_cpf.rodar()
print()
total_falhas += teste_02_cadastros.rodar()
print()
total_falhas += teste_03_tipos_conta.rodar()
print()
total_falhas += teste_04_buscas.rodar()
print()
total_falhas += teste_05_json.rodar()

print()
if total_falhas == 0:
    print("TODOS OS TESTES PASSARAM.")
else:
    print("TOTAL DE FALHAS:", total_falhas)
