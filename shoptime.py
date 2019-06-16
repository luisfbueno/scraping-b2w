from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os
import random
import time

# lista de user agents para usar
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

print("SHOPTIME")
# Montando o path de leitura do arquivo de origem
load_path = os.path.join("input", "Americanas.xlsx")

# Criando tabela de saída
df = pd.DataFrame(columns=["Nome", "Preço", "Ame", "Crédito", "Cartão Loja", "Boleto", "URL"])
# Lendo excel com os links
links_df = pd.read_excel(load_path, header=None, index_col=0, names=["Nome","Link"])

# Iterando os links
for index, link in enumerate(links_df["Link"]):
    print("Accessando link numero {}".format(index+1))
    user_agent = random.choice(user_agent_list)
    headers = {'User-Agent': user_agent}
    link = link.replace("americanas", "shoptime")
    # Fazendo a requisicao criando objeto do BeauifulSoup
    product = BeautifulSoup(requests.get(link, headers=headers).text, "html.parser")
    # Inicializando variaveis 
    prod_name = ""
    prod_price = ""
    prod_price_ame = ""
    prod_price_cloja = ""
    prod_price_cred = ""
    prod_price_boleto = ""
    
    try:
        # Ler nome do produto
        prod_name = product.find("h1", {"id": "product-name-default"}).text
        # Ler preco do produto
        prod_price = product.find("span", {"class": "sales-price"}).text
        # Itera divs com a classe especificada dentro do painel
        for item in product.find("div", {"class": "buy-box"}).select('div[class*="FlexboxUI"]'):
            # Salva string original e a string com letras minusculas
            item_str = item.text.lower()
            item_str_orig = item.text

            # Verifica se a string contem r$, indicando um preco
            if "r$" in item_str:
                # Salva a variavel de acordo com o tipo
                if "shoptime" in item_str:
                    prod_price_cloja = item_str_orig
                elif "ame" in item_str:
                    prod_price_ame = item_str_orig
                elif "boleto" in item_str:
                    prod_price_boleto = item_str_orig
                elif "crédito" in item_str:
                    prod_price_cred = item_str_orig
                    
    except:
        # Se ocorrer erro no processo acima, salva todas como ERRO
        prod_name = prod_price = prod_price_ame = prod_price_boleto = prod_price_cloja = prod_price_cred = "ERRO"
        print("Erro ao ler link a seguir, verificar estoque: {}".format(link))

    # Salva as variaveis em uma lista e salva na tabela de saida
    row = [
        prod_name,
        prod_price,
        prod_price_ame,
        prod_price_cred,
        prod_price_cloja,
        prod_price_boleto,
        link
    ]
    df.loc[len(df)] = row
    # Espera um segundo para ir para a proxima requisição
    time.sleep(1)

# Se nao existir pasta de output, cria uma
if not os.path.isdir("output"):
    os.mkdir("output")

print("Salvando arquivo na pasta output")
path_save = os.path.join("output", "Shoptime.xlsx")
df.to_excel(path_save)