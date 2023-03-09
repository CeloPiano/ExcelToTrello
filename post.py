from trello import TrelloClient

class Label:
    def __init__(self,id,name):
        self.id = id
        self.name = name

genial = Label('6408f1543bd760598eb7cd2c', 'Genial')
btg = Label('6408f15a045603c9f3cf189d', 'BTG')

# Credenciais da API do Trello
#0 - rio claro; 1 - pessoal
api_key = ['424318e17cda03ff122d58968bcf324b', '4848089a42753a2e204034c626e7059b' ] 
token = ['ATTA7abd42a21afa0055d7c6b34cefbcc39da284ffa465364dc2e972d0346834da6390E98D11', 'ATTAca1eb3a295f2138fa934ce83b1d173f107829212be830bb23e6d73f113abc06586803B32']
board_id = ['63c16753b6af47057a5db2c1', '6408e8c5d254de205a5d7759']
list_id = ['63ce8559da3148015c88ec8f', '6408e8c5d254de205a5d7760']

# Criar um cliente Trello
client = TrelloClient(api_key=api_key[1], token=token[1])

# Obter o quadro em que deseja adicionar o card
board = client.get_board(board_id[1])

# Obter a lista em que deseja adicionar o card
list = board.get_list(list_id[1])

# Criar o cartão com campos personalizados
card_title = 'Teste'
card_desc = 'Isso aqui é um teste de integração.'

card = list.add_card(name=card_title, desc=card_desc, labels=[genial,btg])

# criar um campo personalizado
# Obter o objeto CustomField correspondente ao campo personalizado
# campo_personalizado_id = '6408f125285e39309d2323f4'


# valor_do_campo_personalizado = 'text'
# card.set_custom_field(campo_personalizado_id, valor_do_campo_personalizado)

print(card.custom_fields)