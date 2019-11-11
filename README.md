# Scraping B2W

Scripts para realizar scraping de preços de produtos de sites do grupo B2W (Americanas, Shoptime, Submarino).

## Funcionamento

Cada script irá ler uma planilha do Excel, dentro de uma pasta `input` criada na raíz do repositório. Esta planilha deverá conter duas colunas:

- Nome: nome do produto;
- Link: link para o produto em questão;

Cada script vai ler a planilha de sua respectiva loja. Por exemplo, o script `americanas.py` irá ler a planilha `Americanas.xlsx`.

Ao final da execução, o programa irá gerar uma planilha com as seguintes informações:

- Nome: nome do produto;
- Preço: preço principal do produto;
- Ame: preço do produto utilizando o Ame;
- Crédito: preço do produto para pagamentos utilizando Cartão de Crédito;
- Cartão Loja: preço do produto para pagamentos utilizando cartão da loja;
- Boleto: preço do produto para pagamentos via Boleto;
- URL: link para o produto.

## Rodando

Para rodar os scripts, primeiros instale os pacotes do arquivo `requirements.txt`

`pip install -r requirements.txt`

Depois, execute cada script como desejar

`python americanas.py`

`python submarino.py`

`python shoptime.py`

