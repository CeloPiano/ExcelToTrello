from trello import TrelloClient
from trello_utils import *
import os

token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

# board_id_balanceamento_gabrihel = 63e1640fbc36c310635b378f
# board_id_balanceamento_pavan = 63dbb367679209e065af6778
# board_id_balanceamento_jobim = 63d42ddfc57497c8519a6051
# board_id_balanceamento_leite = 63d1729455b75c9c088d4d63
# board_id_balanceamento_reinaldo = 63d1846873c8680ef01623b2
# board_id_taxa = 63f80795ba5f212548c315ce
# board_id_mesa = 63c16753b6af47057a5db2c1


# selecionar o quadro que os card vão ficar
board_id = boards_ids['mesa']

# selecionar o a lista que vao entrar os cards 
list_id = '63e2c6f3939a938da5f0ac95'


client = TrelloClient(api_key, token)

# pegar para cada card do board
# cada campo personalizado trocar o valor dos que não tem _ para os que tem

board = client.get_board(board_id)

# print(board.get_cards()[2])


all_board_cards = board.all_cards()

# print(all_board_cards[0].name)

for card in all_board_cards:
    print(f'Realizando as mudanças do card: {card.name}')
    custom_fields_list = card.customFields 
    custom_fields_board_list = board.get_custom_field_definitions() 
    
    # print(custom_fields_board_list[2].name)
    # print(custom_fields_list[0].name)

    if len(custom_fields_list) > 0:
        for custom_field_under in custom_fields_list:
            #verificar se tem um custom field com o mesmo nome mas sem '_'
            if custom_field_under.name[0] == '_':
                # print("tem underline!")
                for custom_field in custom_fields_board_list:
                    # print(custom_field.name)
                    # aqui eu pego a partir do [1:0] justamente para remover o '_'
                    if custom_field.name == custom_field_under.name[1:]:
                        # aqui temos que pegar os objetos gerados pelo board e não pelo usuário em especial
                        for objeto_correto_custom in custom_fields_board_list:
                            if custom_field_under.name[1:] == objeto_correto_custom.name:
                                print(f'Atribuindo o valor {custom_field_under.value} ao campo {objeto_correto_custom.name}')
                                card.set_custom_field(custom_field_under.value, objeto_correto_custom)
                                                
