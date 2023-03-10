import pandas as pd
from trello import TrelloClient
import os

# pegar todos os cards
token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')
board_id ='640b2a88d9ffacee6755069a'
list_id = '640b2a9048c89f4e41d0777f'

client = TrelloClient(api_key, token)

lista_nomes_cards = []
board_list = client.list_boards()

for board in board_list:
    cards_board = board.open_cards()
    for card in cards_board:
        lista_nomes_cards.append(card.name)
# board = client.get_board(board_id)
# lista_objetos_card = board.all_cards()

print(lista_nomes_cards)

# pegar todos os nomes da tabela

lista_nomes_tabela = []

df = pd.read_excel('tabela_nomes.xlsx')

numero_linhas = df.shape[0]
for linha in range(numero_linhas):
    lista_nomes_tabela.append(df['Nome'][linha])

print(lista_nomes_tabela)

