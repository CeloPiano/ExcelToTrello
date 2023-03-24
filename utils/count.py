from trello import *
from trello_utils import *

api_key = os.environ.get('API_KEY')
token = os.environ.get('API_TOKEN')

client = TrelloClient(api_key, token)

boards = client.list_boards()

# algoritmo que conta o número de cards no trello em geral
count = 0
for board in boards:
        lists = board.get_lists('all')
    
        for list in lists:
            cards = list.list_cards('open')

            for card in cards:
                count += 1
                                

print(count)
# 505 cards
        

              
  
  
  
        

# board = client.get_board(boards_ids['balanceamento_leite'])

# lists = board.get_lists('all')

# count = 0
# for list in lists:
#     print(f'Nome lista: {list.name} | QTD Cards: {len(list.list_cards())}')
#     print(f'contador anterior {count}')
    
#     count += len(list.list_cards())

# print(count)

# onde está o cartão 
# quantos tem


