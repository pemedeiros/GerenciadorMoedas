from datetime import datetime

from lib.interface import cabecalho


def arqexiste(nome):
    try:
        a = open(nome, 'rt')
        a.close()
    except FileNotFoundError:
        return False
    else:
        return True


def criararquivo(nome):
    try:
        a = open(nome, 'wt+')
        a.close()
    except:
        print('Houve um erro ao criar o arquivo')
    else:
        print(f'Arquivo {nome} criado com sucesso')


def lerarquivo(nome):
    try:
        a = open(nome, 'rt')
    except:
        print('Erro ao ler o arquivo')
    else:
        cabecalho('RELATÓRIO CÂMBIOS')
        for linha in a:
            dado = linha.split(';')
            dado[1] = dado[1].replace('\n', '')
            print(f'Cliente: {dado[0]}, Lucro: R${dado[1]:>3}, Valor Final:{dado[2]:>3}\n'
                  f'Moeda de origem:{dado[3]:>3}, Moeda de destino:{dado[4]:>3}\n'
                  f'Valor Original:{dado[5]:>3}\n'
                  f'Valor convertido:{dado[6]:>3}, Dia da operação: {dado[7]:>3}\n'
                  f'------------------------------------------------------')
    finally:
        a.close()


def valor_total(arq):
    try:
        a = open(arq, 'rt')
    except:
        print('Erro ao ler o arquivo')
    else:
        cabecalho('VALOR TOTAL DAS OPERAÇÕES')
        fim = 0.0
        for linha in a:
            dado = linha.split(';')
            fim = float(dado[8])+fim
        print(f' Valor Final em R$:{fim}')
    finally:
        a.close()

def taxas(arq):
    try:
        a = open(arq, 'rt')
    except:
        print('Erro ao ler o arquivo')
    else:
        cabecalho('LUCRO')
        fim = 0.0
        for linha in a:
            dado = linha.split(';')
            fim = float(dado[1])+fim
        print(f' Lucro total em R$:{fim}')
    finally:
        a.close()

def cadastrar(arq, nome='desconhecido', lucro=0, final = 0, origem='', destino='',original='',convertido='',dia='',vFinalRs = ''):
    try:
        a = open(arq, 'at')
    except:
        print('Houve um erro ao abrir o arquivo ')
    else:
        try:
            a.write(f'{nome};{lucro};{final};{origem};{destino};{original};{convertido};{dia};{vFinalRs}\n')
        except:
            print('Houve um erro ao escrever no arquivo')
        else:
            print(f'Novo registro de {nome} adicionado')
            a.close()


def filtro_data(arq,ini,fim):
    try:
        a = open(arq, 'rt')
    except:
        print('Erro ao ler o arquivo')
    else:
        cabecalho('FILTRO POR DATA')
        for linha in a:
            dado = linha.split(';')
            dado[1] = dado[1].replace('\n', '')
            data = datetime.strptime(dado[7], "%d/%m/%Y")
            if ini <= data <= fim:
                print(f'Cliente: {dado[0]}, Lucro: R${dado[1]:>3}, Valor Final:{dado[2]:>3}\n'
                      f'Moeda de origem:{dado[3]:>3}, Moeda de destino:{dado[4]:>3}\n'
                      f'Valor Original:{dado[5]:>3}\n'
                      f'Valor convertido:{dado[6]:>3}, Dia da operação: {dado[7]:>3}\n'
                      f'------------------------------------------------------')
    finally:
        a.close()


def filtro_nome(arq,nome):
    try:
        a = open(arq, 'rt')
    except:
        print('Erro ao ler o arquivo')
    else:
        cabecalho('FILTRO POR DATA')
        for linha in a:
            dado = linha.split(';')
            dado[1] = dado[1].replace('\n', '')
            if nome == dado[0]:
                print(f'Cliente: {dado[0]}, Lucro: R${dado[1]:>3}, Valor Final:{dado[2]:>3}\n'
                      f'Moeda de origem:{dado[3]:>3}, Moeda de destino:{dado[4]:>3}\n'
                      f'Valor Original:{dado[5]:>3}\n'
                      f'Valor convertido:{dado[6]:>3}, Dia da operação: {dado[7]:>3}\n'
                      f'------------------------------------------------------')
    finally:
        a.close()