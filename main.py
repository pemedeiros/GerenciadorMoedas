import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date

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
nome_cliente = input("Digite o nome do cliente: ")
hoje = date.today()
data_da_operação = hoje.strftime("%d/%m/%Y")

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


lista_chave = list(moeda.keys())
lista_valores = list(moeda.values())
while True:
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
    print(f'Você terá {valor_final} ')
    print(f'Nessa conversão, a empresa ganhou R$ {lucro}')
    print(f'A moeda de origem é {nome_moeda_origem}')
    print(f'A moeda de destino é {nome_moeda_destino}')
    print(f'O valor original foi {quantia}')
    print(f'O valor convertido foi {valor_final}')
    valor_total_operacoes = valor_total_operacoes + valor_para_real
    valor_total_ganho = valor_total_ganho + lucro
    opcao = int(input("Digite 0 para sair"))
    if opcao == 0:
        print(f'O valor total das operações foi R${valor_total_operacoes}')
        print(f'O valor total dos lucros foi R${valor_total_ganho}')
        break


