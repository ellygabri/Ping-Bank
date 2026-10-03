# Compara os resultados usando somente listas, dicionarios, for e if.
def verificar(casos):
    passaram = 0
    falharam = 0

    for caso in casos:
        if caso["resultado"] == caso["esperado"]:
            print("PASSOU:", caso["descricao"])
            passaram += 1
        else:
            print("FALHOU:", caso["descricao"])
            print("Esperado:", caso["esperado"])
            print("Obtido:", caso["resultado"])
            falharam += 1

    print("Resultado:", passaram, "passaram;", falharam, "falharam.")
    return falharam
