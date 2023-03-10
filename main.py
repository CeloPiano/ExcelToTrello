from trello import TrelloClient

from push import geraQuadro
import pandas as pd
import os
import difflib
import unicodedata


def formatar_string(string):
    return unicodedata.normalize('NFKD', string.upper()).encode('ASCII', 'ignore').decode('ASCII')

# correção de nomes (aqui temos todas as opções do trello de campos personalizados)
entradas_campos_personalizados = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabrihel Beigelman", "Igor Falcão", "João Pessini", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo"]

token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

# selecionar o quadro que os card vão ficar
board_id ='640b2a88d9ffacee6755069a'

# selecionar o a lista que vao entrar os cards 
list_id = '640b2a9048c89f4e41d0777f'

# CRIA UMA LISTA COM TODOS OS NOMES JÁ EXISTENTES NO QUADRO (puxa do banco do trello todos os nomes) (é por quadro)
client = TrelloClient(api_key, token)
board = client.get_board(board_id)
lista_objetos_card = board.all_cards()
lista_nome_card_existente = []
for elemento in lista_objetos_card:
    # lista de nomes
    lista_nome_card_existente.append(formatar_string(elemento.name))
    # lista de cpfs já adicionados
    # pegar a definition do cpf aqui no caso é a 3 (tirar o print e dar um get na definitions)
    if len(elemento.customFields):
        lista_nome_card_existente.append(elemento.customFields[1].value)
print(lista_nome_card_existente)
    
    
# acessar a excel
# colocar todos os clientes em uma lista com seus respectivos campos
# Panda lê do excel 
df = pd.read_excel('tabela_nomes.xlsx')

# pegar o numero das linhas (shape retorna uma tupla quantidade de (qtdLinhas,qtdColunas))
numero_linhas = df.shape[0]

# lista para fazer a filtragem (Aqui devo adicionar correspondente a tabela .xlsx) não tem as Corretoras
lista_colunas_corretas = ['Nome', 'CPF', "Situação", "Perfil", "Planejador"]

# iteração nas linhas para juntar todos os argumentos por cliente e adicionar no trello
# Ordem: Nome, Corretora, CPF, Situação, Perfil, Nome do Planejador/Planejador
indice_linha = 0
lista_nomes_adicionados_atual = []
for linha in range(numero_linhas):
    # lista para alocar os argumentos
    argumentos = {}
    # como podemos ter varias corretoras seu espaço no map é uma lista
    argumentos['Corretoras'] = []
    for coluna in df.columns:
        
        # esse é o valor = df[coluna][linha]
        valor = df[coluna][linha]
            
        # fazer a filtragem da coluna aqui nao incluimos as corretoras(caso especial)
        if coluna in lista_colunas_corretas:
            valores_corrigidos = difflib.get_close_matches(valor, entradas_campos_personalizados)
            if len(valores_corrigidos) != 0 and coluna != 'Nome':
                valor_corrigido = valores_corrigidos[0]
                # print(valores_corrigidos)
                # print(valor_corrigido)
                argumentos[coluna] = valor_corrigido
            else:
                argumentos[coluna] = valor
        # verificar se o proximo tem o mesmo nome, se tiver adiciona mais a corretora (so adiciona se tiver 2 corretoras)
        if coluna == 'Corretoras':
            argumentos[coluna].append(valor)
            
            if indice_linha < numero_linhas - 1: 
                print(df['Nome'][indice_linha + 1])
                if df['Nome'][indice_linha] == df['Nome'][indice_linha + 1]:
                    argumentos[coluna].append(df['Corretoras'][indice_linha + 1])
    
    titulo = formatar_string(argumentos['Nome']) 
    corretoras = argumentos['Corretoras'] 
    cpf = argumentos['CPF'] 
    situacao = argumentos['Situação'] 
    perfil = argumentos['Perfil']
    planejador = argumentos['Planejador']
    
    # ajustar os perfis
    # aqui fazemos um filtro para não haver nomes repetidos no quadro
    if cpf not in lista_nome_card_existente and titulo not in lista_nome_card_existente and titulo not in lista_nomes_adicionados_atual:
        # geramos o quadro
        print(f'Criando card da {titulo}...')
        geraQuadro(api_key,token,board_id,list_id,titulo,'',corretoras,cpf,situacao,perfil,planejador)
    
    # essa lista é por requisição, para não ter que fazer uma chamada geral a cada requisição
    lista_nomes_adicionados_atual.append(titulo)
    indice_linha += 1





