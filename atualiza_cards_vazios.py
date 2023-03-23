import difflib
from trello import TrelloClient
from trello_utils import *
import os
import pandas as pd
import numpy as np


# funcao para acessar os nomes que estão na planilha e pegar o index do nome
def index(lista, string):
    indices = np.where(lista == string)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        return -1
    
def return_best_match(value):
    filtred_value = difflib.get_close_matches(value, planejador_values)
    if len(filtred_value) > 0:
        filtred_value = filtred_value[0]
        return filtred_value
    else:
        return 0
    
token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

client = TrelloClient(api_key, token)


# SELECIONAR O BOARD 
board = client.get_board(boards_ids['mesa'])


# aqui criei uma lista com todos os objetos custom fields que quero preencher em cada card

custom_field_board_filtred = {}
custom_field_board_list = board.get_custom_field_definitions()
for custom_field_definition in custom_field_board_list:
    if custom_field_definition.name[0] != '_':
        custom_field_board_filtred[custom_field_definition.name] = custom_field_definition
        
# custom_field_board_filtred
# {'⚠': <CustomFieldDefinition ⚠>, 
#  'CPF/CNPJ': <CustomFieldDefinition CPF/CNPJ>,
#  'Conta': <CustomFieldDefinition Conta>,
#  'Perfil': <CustomFieldDefinition Perfil>,
#  'Perfil Previdência': <CustomFieldDefinition Perfil Previdência>,
#  'Perfil Offshore': <CustomFieldDefinition Perfil Offshore>,
#  'Situação': <CustomFieldDefinition Situação>,
#  'Planejador': <CustomFieldDefinition Planejador>,
#  'Liquidação': <CustomFieldDefinition Liquidação>}


labels_list = board.get_labels()

# pegar os objetos labels que irá usar caso o nome for btg ou genial...add()
name_label = {}
for object_label in labels_list:
    name = object_label.name
    name_label[name] = object_label

# name_label
# {'Balanceamento': <Label Balanceamento>
# , 'Genial': <Label Genial>
# , 'Resgate': <Label Resgate>
# , 'BTG': <Label BTG>
# , 'Previdência': <Label Previdência>
# , 'Somente Resgate': <Label Somente Resgate>
# , 'Ausente Tabela de Clientes': <Label Ausente Tabela de Clientes>
# , 'Não Mexer': <Label Não Mexer>
# , 'Conta Bloqueada': <Label Conta Bloqueada>
# , 'Interactive Brokers': <Label Interactive Brokers>
# , 'Órama': <Label Órama>
# , 'Intaxável': <Label Intaxável>}


# essa cliente não foi adaptada ao que o mario queria (preencher de acordo com a planilha)
# print(board.all_cards()[15].customFields)


#iterar dentro do quadro e ir tentando achar o padrao 
# achou: adicionar as informações correspondentes no cartão 
# os fields (set )
# as labels (usar ideia da main)


# pegar na tabela o nome das colunas

df = pd.read_excel('tabela_nomes_2.xlsx')
column_names = df.columns
lines_names = df['Nome'].values

map_column_value = {}
for column in column_names:
    map_column_value[column] = ''


cards_list = board.all_cards()

for card in cards_list:
    custom_fields_list = card.customFields
    
    # if len(custom_fields_list) <= 2:
    print(f'NOME DO CARD: {card.name}')
    
    # aqui pegamos o indice do nome do card na planilha referente ao nome
    card_name = card.name
    filtred_name = difflib.get_close_matches(card_name, lines_names)
    
    if len(filtred_name) > 0:
        name_index = index(lines_names,filtred_name[0])
    else:
        name_index = 'no_name'
        # aqui se não tiver um nome na planilha:
        print(f'{card_name} não tem nenhum nome parecido na planilha, não relizando ação!')
    
    equal_names = True
    
    # verificação pra ver se está na planilha:
    if name_index != 'no_name':
        if card.name != filtred_name[0]:
            print("NOMES DIFERENTES! POSSIVEL USUARIO FORA DA PLANILHA")
            print(filtred_name)
            equal_names = False

    # aqui eu tenho o name_index, depois é só adicionar o restante nas colunas...
    # cpf/cnpj Conta Perfil Situação Planejador Liquidação 
    if name_index != 'no_name' and equal_names:
        print('adicionando campos personalizados')
        print(df['Nome'][name_index])
        for column in column_names:
            value = df[column][name_index]
            # preencher o map com os valores correspondentes a cada nome da coluna
            # valor da coluna daquele cliente
            map_column_value[column] = value

            if column == 'Planejador':
                # fitrar o valor pra não dar problema
                if value != 0:
                    value = return_best_match(value)
                    if value != 0:
                        card.set_custom_field(value, custom_field_board_filtred['Planejador'])
                        print(f'Adicionado: {value}')
                
            elif column == 'Situacao':
                # fitlrar o valor
                if value in situacao_values:
                    value = situacao_values[value]
                card.set_custom_field(value, custom_field_board_filtred['Situação'])
                print(f'Adicionado: {value}')
                
            elif column == 'Perfil':
                # filtrar o valor 
                if value in perfil_values:
                    value = perfil_values[value]
                    card.set_custom_field(value, custom_field_board_filtred['Perfil'])
                print(f'Adicionado: {value}')
                
            elif column == 'CPF':
                card.set_custom_field(value, custom_field_board_filtred['CPF/CNPJ'])
                print(f'Adicionado: {value}')
            




            
            # print(map_column_value)
            
            
            # cpf
            # perfil
            # situacao
            # planejador
            
            # card.set_custom_field(value, custom_field_object)
            
            # pegar objeto campo
            # if len(filtred_column) > 0:
                # custom_field_object = custom_field_board_filtred[filtred_column[0]]
                # print(custom_field_object)
            # filtrar value...
            # filtred_value = difflib.get_close_matches(value, custom_field_values)
            
            # print(custom_field_object[0])
            # print(filtred_column[0])
            # print(filtred_value[0])
            # aqui cria o cartão preciso de
            # um valor (que encaixe com os padrões estipulados pelo campo)
            # o objeto em questão
            
            
        
        # pensar em algo inteligente para a parte das labels? verificar o proximo da lista?
        
        
        # {'Nome': 'VANESSA ARREDONDO COELHO'
        # , 'Planejador': 'Leonardo Pavan'
        # , 'PL': 61650.0
        # , 'Situacao': 1
        # , 'RF': 0.0
        # , 'Corretora': 'BTG'
        # , 'Perfil': 3.0
        # , 'Suitability': nan
        # , 'Sexo': nan
        # , 'CPF': '050.704.581-59'
        # , 'Tipo Cliente': nan
        # , 'Sinacor': -100
        # , 'Email': 'nessaacoelho23@gmail.com'
        # , 'Habilitacao': nan
        # , 'Profissao': nan
        # , 'Telefone': nan}
        