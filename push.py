from trello import TrelloClient

class Label:
    def __init__(self,id,name):
        self.id = id
        self.name = name


# aqui label é uma lista com nomes das corretoras que esse cliente tem.
def geraQuadro(api_key, token, board_id, list_id, card_title, card_desc, corretoras,cpf,situacao,perfil,planejador):
    
    # lembrar de ajustar
    id_label_genial = '640b2a9991ff5e2b6becb575'
    id_label_btg = '640b2a9991ff5e2b6becb581'
    id_label_orama = '640b2b58696f8f5aefced4a6'
    
    # legenda das corretoras
    # aqui criei uma classe corretora, pra função add_card poder utilizar o nome.id para acessar o id...
    genial = Label(id_label_genial, 'Genial')
    btg = Label(id_label_btg, 'BTG')
    orama = Label(id_label_orama, 'Orama')
    interactive = 'a adicionar'
    netx = 'a adicionar'
    
    nomeCorretora = {
        'Genial' : genial,
        'BTG' : btg,
        'Órama': orama 
    }

    # Criar um cliente Trello
    client = TrelloClient(api_key, token)

    # Obter o quadro em que deseja adicionar o card
    board = client.get_board(board_id)

    # Obter a lista em que deseja adicionar o card
    list = board.get_list(list_id)

    # pegar os objetos costumFields
    lista_custom_fields = board.get_custom_field_definitions()
   
    # parte que adiciona as labels contidas na lista de labels (joga tudo dentro da lista labeadicionar)
    labelAdicionar = []
    if len(corretoras) > 1:
        for corretora in corretoras:
            print(corretora)
            labelAdicionar.append(nomeCorretora[corretora])
    else:
        labelAdicionar.append(nomeCorretora[corretoras[0]])
    
    # adicionar o cartão com os campos personalizados(criar função) LABEL é uma lista com as classes label
    card = list.add_card(name=card_title, desc=card_desc, labels=labelAdicionar)
    
    # adicionando o costum field ao cartão...
    for i in range(4):
        campo_em_questao = lista_custom_fields[i] #escrita no cardeno
        if campo_em_questao.name == "Situação":
            valor_custom_field = situacao
        elif campo_em_questao.name == "Planejador":
            valor_custom_field = planejador
        elif campo_em_questao.name == "Perfil":
            valor_custom_field = perfil
        else:
            valor_custom_field = cpf
        card.set_custom_field(valor_custom_field, campo_em_questao)