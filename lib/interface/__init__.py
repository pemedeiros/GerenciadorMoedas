def leiaint(msg):
    while True:
        try:
            v = int(input(msg))
        except(ValueError, TypeError):
            print('\033[0;31mERRO! Digite um valor válido.\033[m')
            continue
        else:
            return v


def linha(tam = 42):
    return '-' * tam


def cabecalho(txt):
    print(linha())
    print(txt.center(42))
    print(linha())


def menu(lista):
    cabecalho('MENU PRINCIPAL')
    c = 1
    for item in lista:
        print(f'\033[33m{c}\033[m - \033[34m{item}\033[m')
        c += 1
    print(linha())
    opc = leiaint('Sua opção: ')
    return opc