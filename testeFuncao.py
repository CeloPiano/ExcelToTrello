from trello import TrelloClient

from push import geraQuadro
import pandas as pd
import os

token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

board_id ='6408e8c5d254de205a5d7759'
list_id = '6408e8c5d254de205a5d7761'

# acessar a excel
# colocar todos os clientes em uma lista com seus respectivos campos



# temos que chamar isso iterativamente pra cada coluna 
# aqui criamos o quadro com todos os argumentos...
titulo = 'Joseph Climber'
desc = 'Aqui vai dar certo a label'
corretoras = ['Genial', 'BTG']
cpf = '07823507129'
situacao = 'Ativo'
perfil = 'Moderado'
planejador = 'Pedro Jobim'
geraQuadro(api_key,token,board_id,list_id,titulo,desc,corretoras,cpf,situacao,perfil,planejador)
