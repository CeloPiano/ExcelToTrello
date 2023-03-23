import unicodedata
import difflib
import numpy as np
import pandas as pd

def label_names_add(value):
    # retirar os espaços
    value = value.replace(" ", "")
    labels = []
    
    label = ''
    # criar a label de cada corretora
    for letter in value:
        if letter != '/':
            label += letter
        elif letter == '/':
            labels.append(label)
            label = ''
    labels.append(label)
    
    return labels
    
def best_match(value):
    filtred_value = difflib.get_close_matches(value, planejador_corretoras_values)
    print(f'VALORES FILTRADOS: {filtred_value}')
    if len(filtred_value) > 0:
        filtred_value = filtred_value[0]
        return filtred_value
    else:
        return 0

def index(lista, string):
    indices = np.where(lista == string)[0]
    if len(indices) > 0:
        return indices[0]
    else:
        return -1

# pegar todos os cards não arquivados (open cards) e gera uma lista com todos os nomes e cpfs.
def verifica_nomes(client):
    lista_nomes_cards = []
    board_list = client.list_boards()

    for board in board_list:
        # aqui pegamos apenas os cards que não estão arquivados (os open)
        # pega todos os os nomes dos cards
        if board.name != "Taxa Administrativa":
            print(f"Verificando os cards que estão no quadro {board.name}")
            print(f"Adicionando os card na lista...")
            cards_board = board.open_cards()
            for card in cards_board:
                lista_nomes_cards.append(card.name)
                # como pegar os cpfs? - retorna uma lista e na lista nos iteramos para achar o nome == cpf
                if len(card.customFields) > 0:
                    for customField in card.customFields:
                        # aqui colocamos o nome desejado para o campo personalizado
                        if customField.name == 'CPF/CNPJ':
                            lista_nomes_cards.append(customField.value)
        print('')
    return lista_nomes_cards


def formatar_string(string):
    return unicodedata.normalize('NFKD', string.upper()).encode('ASCII', 'ignore').decode('ASCII')


boards_ids = {'balanceamento_gabrihel' : '63e1640fbc36c310635b378f',
            'balanceamento_pavan' : '63dbb367679209e065af6778',
            'balanceamento_jobim' : '63d42ddfc57497c8519a6051',
            'balanceamento_leite' : '63d1729455b75c9c088d4d63',
            'balanceamento_reinaldo' : '63d1846873c8680ef01623b2',
            'taxa' : '63f80795ba5f212548c315ce',
            'mesa' : '63c16753b6af47057a5db2c1'}

# correção de nomes (aqui temos todas as opções do trello de campos personalizados quando se trata de listas)
planejador_corretoras_values = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabrihel Beigelman", "Igor Falcão", "João Pessini", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo", 
                                  "Órama", "BTG", "Genial", "Pershing", "Sem Conta"]

# na tabela = 1 2 3 4 5
# no trello = 1️⃣ Ativo 2️⃣ Inativo 3️⃣ Bloqueado 4️⃣ Excluir 5️⃣ Portabilidade
situacao_values = {
1 : '1️⃣ Ativo'
, 2: '2️⃣ Inativo'
, 3 : '3️⃣ Bloqueado'
, 4: '4️⃣ Excluir'
, 5 : '5️⃣ Portabilidade'}

# na tabela = 1 2 3 4 5
# no trello = 0️⃣ Crédito Privado  1️⃣ Conservador 2️⃣ Conservador-Moderado 3️⃣ Moderado 4️⃣ Moderado-Agressivo 5️⃣ Agressivo
perfil_values = {
0 : '0️⃣ Crédito Privado'
, 1 : '1️⃣ Conservador'
, 2: '2️⃣ Conservador-Moderado'
, 3:'3️⃣ Moderado'
, 4: '4️⃣ Moderado-Agressivo'
, 5: '5️⃣ Agressivo'}



# aqui label é uma lista com nomes das corretoras que esse cliente tem.
def geraQuadro(client, board_id, list_id, card_title, card_desc, corretoras,cpf,situacao,perfil,planejador):
    
    # Obter o quadro em que deseja adicionar o card
    board = client.get_board(board_id)
    
    # pegar os objetos labels que irá usar caso o nome for btg ou genial...add()
    labels_list = board.get_labels()
    name_label = {}
    for object_label in labels_list:
        name = object_label.name
        name_label[name] = object_label
    
    
    # {'Genial': <Label Genial>
    # 'BTG': <Label BTG>}
    # aqui criei uma classe corretora, pra função add_card poder utilizar o nome.id para acessar o id...

    # Obter a lista em que deseja adicionar o card
    list = board.get_list(list_id)

    # pegar os objetos costumFields
    lista_custom_fields = board.get_custom_field_definitions()
   
    # parte que adiciona as labels contidas na lista de labels (joga tudo dentro da lista labeadicionar)
    # corretoras são os nomes das corretoras, no dicionário name_label temos os nomes das labes com seus respectivos obejetos
    labelAdicionar = []
    if len(corretoras) > 1:
        for corretora in corretoras:

            # filtrar para ter o nome certo da label
            corretora_filtred = best_match(corretora)
            if  corretora_filtred != 0:
                corretora = corretora_filtred
                print(f'Corretora {corretora} filtrada.')
            # print(f'Adicionando o nome da label: {corretora} relacionada ao objeto {name_label[corretora]}')
                
            labelAdicionar.append(name_label[corretora])
    else:
        labelAdicionar.append(name_label[corretoras[0]])
    
    # adicionar o cartão com os campos personalizados(criar função) LABEL é uma lista com as classes label
    card = list.add_card(name=card_title, desc=card_desc, labels=labelAdicionar)
    
    # print(lista_custom_fields)
    # hora de os ucstom fields 
    for i in range(len(lista_custom_fields)):
        # pegando o custom field definition
        campo_em_questao = lista_custom_fields[i]
        
        # pegando seu nome para fazer a verficação
        nome_campo = campo_em_questao.name
        
        if nome_campo == "Situação":
            valor_custom_field = situacao
        elif nome_campo == "Planejador":
            valor_custom_field = planejador
        elif nome_campo == "Perfil":
            valor_custom_field = perfil
        elif nome_campo == 'CPF/CNPJ':
            valor_custom_field = cpf
        else:
            valor_custom_field = ''
            
        if valor_custom_field != '':
            print(f'Adicionando Custom Field: {nome_campo} o valor {valor_custom_field}')
            
            # verificar se é nan (não tem nenhum valor na cell)
            if pd.isna(valor_custom_field):
                print('Cedula nula.')
                
            # se não for, adiciona o custom_field
            else:
                card.set_custom_field(valor_custom_field, campo_em_questao)
    
    
    # custom fields definitions obtidas -> tem que ser do BOARD e não do card
    
    # [<CustomFieldDefinition ⚠>
    # , <CustomFieldDefinition CPF/CNPJ>
    # , <CustomFieldDefinition Conta>
    # , <CustomFieldDefinition Perfil>
    # , <CustomFieldDefinition Perfil Previdência>
    # , <CustomFieldDefinition Perfil Offshore>
    # , <CustomFieldDefinition Situação>, 
    # <CustomFieldDefinition Planejador>,
    # <CustomFieldDefinition Liquidação>]