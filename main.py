from trello import TrelloClient
import pandas as pd
import os

from trello_utils import *

# PEGAR DO TRELLO trello.com/app-key 

token = os.environ.get('API_TOKEN')


api_key = os.environ.get('API_KEY')

# SELECIONAR o quadro que os card vão ficar

board_id = boards_ids['mesa']

# SELECIONAR a lista que vao entrar os cards 

list_id = '63ce8559da3148015c88ec8f'

# pegar o client

client = TrelloClient(api_key, token)

# CRIA UMA LISTA COM TODOS OS NOMES JÁ EXISTENTES NO QUADRO (puxa do banco do trello todos os nomes) (é por quadro)
lista_nome_card_existente = []
lista_nome_card_existente = verifica_nomes(client)
    
# Acessar o excel
# colocar todos os clientes em uma lista com seus respectivos campos

# Panda lê do excel 
df = pd.read_excel('tabela_clientes.xlsx')

# pegar o numero das linhas (shape retorna uma tupla quantidade de (qtdLinhas,qtdColunas))

numero_linhas = df.shape[0]

# lista para fazer a filtragem (Aqui devo adicionar correspondente a tabela .xlsx) não tem as Corretoras
lista_colunas_corretas = ['Nome', 'CPF', "Situacao", "Perfil", "Planejador", "Corretora"]

# iteração nas linhas para juntar todos os argumentos por cliente e adicionar no trello
# Ordem: Nome, Corretora, CPF, Situação, Perfil, Nome do Planejador/Planejador

# lista que é preenchida com os usuários adicionados na execução do momento
lista_nomes_adicionados_atual = []

for linha in range(numero_linhas):
    # lista para alocar os argumentos
    argumentos = {}
    
    # como podemos ter varias corretoras seu espaço no map é uma lista
    argumentos['Corretora'] = []
    
    for coluna in df.columns:
        
        # esse é o valor = df[coluna][linha]
        valor = df[coluna][linha]
            
        # fazer a filtragem da coluna aqui nao incluimos as corretoras(caso especial)
        if coluna in lista_colunas_corretas:
            
            # preencher o map com os valores correspondentes a cada nome da coluna
            # valor da coluna daquele cliente
                
            value = df[coluna][linha]
            argumentos[coluna] = value
            
            if coluna == 'Situacao':
                # fitlrar o valor
                if value in situacao_values:
                    value = situacao_values[value]
                    argumentos['Situacao'] = value
                # print(f'Adicionado: {value}')
                
            elif coluna == 'Perfil':
                # filtrar o valor 
                # verificar se a celula esta vazia
                if value in perfil_values:
                    value = perfil_values[value]
                    argumentos['Perfil'] = value
                # print(f'Adicionado: {value}')
                
            elif coluna == 'CPF':
                # print(f'Adicionado: {value}')
                if pd.isna(value):
                    value = 'Não tem CPF na planilha'
                argumentos['CPF'] = value
                
            elif coluna == 'Corretora':
                # a função label_names_add foi criada para o caso "BTG/ GENIAL" do leite (especifico)
                # mas funciona para qualquer outro. 
                
                argumentos['Corretora'] = label_names_add(value)
    
            elif coluna == 'Planejador':
                argumentos['Planejador'] = value
                
                
    corretora = argumentos['Corretora']
    titulo = formatar_string(df['Nome'][linha])
    cpf = argumentos['CPF'] 
    perfil = argumentos['Perfil']
    situacao = argumentos['Situacao']
    planejador = argumentos['Planejador']
    
    # ajustar os perfis
    # aqui fazemos um filtro para não haver nomes repetidos no quadro
    if cpf not in lista_nome_card_existente and titulo not in lista_nome_card_existente and titulo not in lista_nomes_adicionados_atual:
        # aqui o card ja foi verificado e está em processo de adição
        print(f'Criando card da {titulo}...')
        
        #função que adiciona
        geraQuadro(client,board_id,list_id,titulo,'',corretora,cpf,situacao,perfil,planejador)
    
    # essa lista é por requisição, para não ter que fazer uma chamada geral a cada requisição (o que é mais custoso)
    lista_nomes_adicionados_atual.append(titulo)





