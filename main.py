import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date, datetime
from time import sleep
from lib.arquivo import arqexiste, criararquivo, lerarquivo, cadastrar, valor_total, taxas, filtro_data, filtro_nome
from lib.interface import menu, cabecalho, leiaint

moeda = {
    'BRL': 1,
    'USD': 0,
    'CAD': 0,
    'JPY': 0,
    'EUR': 0,
    'GBP': 0,
    'AUD': 0,
    'RUB': 0,
    'HKD': 0,
    'CNY': 0,
    'CHF': 0,
    'SEK': 0
}

valor_total_operacoes = 0.0
valor_total_ganho = 0.0
valor_para_real = 0.0

req = requests.get('http://br.advfn.com/cambio/graficos/brl')
if req.status_code == 200:
    content = req.content
    soup = BeautifulSoup(content, 'html.parser')
    table = soup.find(name='table')
    table_str = str(table)
    df = pd.read_html(table_str)[0]
    df = df.T.set_index(0).T
    df = df[['Taxas de câmbio', 'Compra']]
    df_att = df
    for x, y in df_att.iterrows():
        taxa = y['Taxas de câmbio']
        compra = y['Compra']
        if taxa[0:3] == "BRL":
            taxa = taxa[3::]
            compra = 1 / float(compra)
            df_att['Taxas de câmbio'][x] = taxa
            df_att['Compra'][x] = compra
        else:
            taxa = taxa[0:3]
            df_att['Taxas de câmbio'][x] = taxa
        moeda[taxa] = float(compra)
    df2 = pd.DataFrame([['BRL', 1]], columns=['Taxas de câmbio', 'Compra'])
    df_att = pd.concat([df2, df_att])


    arq = 'ListaOperacoes.txt'
    if not arqexiste(arq):
        criararquivo(arq)
    while True:
        resposta = menu(
            ['Câmbio de moedas','Ver lista total das operações', 'Ver valor total das operações','Ver valor total das taxas cobradas','Filtrar por data','Filtrar por cliente' ,'Sair',
             ])
        if resposta == 1:
            # Cadastrar
            cabecalho('NOVA CONVERSÃO')
            nome = str(input('Digite o nome do cliente:'))
            hoje = date.today()
            data_da_operação = hoje.strftime("%d/%m/%Y")
            lista_chave = list(moeda.keys())
            lista_valores = list(moeda.values())
            print("MENU DE MOEDAS\n")
            for k in moeda.keys():
                print(f'{lista_chave.index(k)} - {k}')
            print()


            def get_moeda(tipo_moeda: str):
                opcao = int(input(f"Digite o código de moeda de {tipo_moeda}: "))
                return lista_chave[opcao], lista_valores[opcao]


            nome_moeda_origem, valor_moeda_origem = get_moeda("origem")
            nome_moeda_destino, valor_moeda_destino = get_moeda("destino")

            quantia = float(input(f"Quantos(as) {nome_moeda_origem} você quer converter? "))
            taxa_cobrada = quantia * 0.05
            valor_convertido = quantia * 0.95

            if nome_moeda_origem == "BRL":
                lucro = taxa_cobrada
                valor_para_real = quantia
            else:
                lucro = taxa_cobrada * valor_moeda_origem
                valor_para_real = quantia * valor_moeda_origem

            valor_final = round(valor_convertido * valor_moeda_origem / valor_moeda_destino, 2)
            valor_total_operacoes = valor_total_operacoes + valor_para_real
            cadastrar(arq, nome, lucro, valor_final, nome_moeda_origem, nome_moeda_destino, quantia, valor_convertido,
                      data_da_operação, valor_total_operacoes)
            sleep(2)
        elif resposta == 2:
            # Listar
            lerarquivo(arq)
            sleep(2)
        elif resposta == 3:
            valor_total(arq)
            break
        elif resposta == 4:
            taxas(arq)
            break
        elif resposta == 5:
            data_ini = str(input('Digite a data inicial: '))
            data_filtroIni = datetime.strptime(data_ini, "%d/%m/%Y")
            data_fim = str(input('Digite a data final: '))
            data_filtroFim = datetime.strptime(data_fim, "%d/%m/%Y")
            filtro_data(arq, data_filtroIni, data_filtroFim)
            break
        elif resposta == 6:
            nome = input("Digite o nome que deseja filtrar: ")
            filtro_nome(arq, nome)
            break
        elif resposta == 7:
            cabecalho('Saindo do sistema...Até mais.')
            break
        else:
            print('\033[031mERRO! Digite uma opção válida.\33[m')
            sleep(2)