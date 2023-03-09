from trello import TrelloClient

# Credenciais da API do Trello
#0 - rio claro; 1 - pessoal
api_key = ['424318e17cda03ff122d58968bcf324b', '4848089a42753a2e204034c626e7059b' ] 
token = ['ATTA7abd42a21afa0055d7c6b34cefbcc39da284ffa465364dc2e972d0346834da6390E98D11', 'ATTAca1eb3a295f2138fa934ce83b1d173f107829212be830bb23e6d73f113abc06586803B32']
board_id = ['63c16753b6af47057a5db2c1', '6408e8c5d254de205a5d7759']
list_id = ['63ce8559da3148015c88ec8f', '6408e8c5d254de205a5d7760']

# 0 formatado, 1 novo
card_id = ['6408e8f57e7a776c0a9d8700', '640935ccb813a23ce454660a']


# Criar um cliente Trello
client = TrelloClient(api_key=api_key[1], token=token[1])

card = client.get_card(card_id[1])

# aqui eu pego o BOARD ID
board = client.get_board(board_id[1])

# aqui eu consigo o objeto custom field
field = board.get_custom_field_definitions()
print(field)
# defino o valor do custom field
valor = 'testeeeeeee'
# aqui mudo o valor e pego do field [0]
campo_em_questao = field[0]
# print(f'TIPO DO CAMPO:{campo_em_questao.field_type}')
card.set_custom_field(valor, campo_em_questao)
print(f'esse field foi mudado {campo_em_questao.name} para: {valor}')

