from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import os

print("AMERICANAS")
load_path = os.path.join("input", "Americanas.xlsx")

df = pd.DataFrame(columns=["Nome", "Preço", "Ame", "Crédito", "Cartão Loja", "Boleto", "URL"])
links_df = pd.read_excel(load_path, header=None, index_col=0, names=["Nome","Link"])

for index, link in enumerate(links_df["Link"]):
    print("Accessando link numero {}".format(index+1))
    product = BeautifulSoup(requests.get(link).text, "html.parser")
    prod_name = ""
    prod_price = ""
    prod_price_ame = ""
    prod_price_cloja = ""
    prod_price_cred = ""
    prod_price_boleto = ""
    
    try:
        prod_name = product.find("h1", {"id": "product-name-default"}).text
        prod_price = product.find("span", {"class": "sales-price"}).text
        for item in product.find("div", {"class": "buybox-b-panel"}).select('div[class*="FlexboxUI"]'):
            item_str = item.text.lower()
            item_str_orig = item.text
            
            if "r$" in item_str:
                if "americanas.com" in item_str:
                    prod_price_cloja = item_str_orig
                elif "ame" in item_str:
                    prod_price_ame = item_str_orig
                elif "boleto" in item_str:
                    prod_price_boleto = item_str_orig
                elif "crédito" in item_str:
                    prod_price_cred = item_str_orig
                    
    except:
        prod_name = prod_price = prod_price_ame = prod_price_boleto = prod_price_cloja = prod_price_cred = "ERRO"
        print("Erro ao ler link a seguir, verificar estoque: {}".format(link))

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

if not os.path.isdir("output"):
    os.mkdir("output")

print("Salvando arquivo na pasta output")
path_save = os.path.join("output", "Americanas.xlsx")
df.to_excel(path_save)