from trello import TrelloClient

from push import geraQuadro
import pandas as pd


token = 'ATTAca1eb3a295f2138fa934ce83b1d173f107829212be830bb23e6d73f113abc06586803B32'
api_key = '4848089a42753a2e204034c626e7059b'
board_id ='6408e8c5d254de205a5d7759'
list_id = '6408e8c5d254de205a5d7761'




# acessar a excel
# colocar todos os clientes em uma lista com seus respectivos campos



# aqui criamos o quadro com todos os argumentos...
titulo = 'TESTE 1000'
desc = 'Aqui vai dar certo a label'
corretoras = ['BTG']
cpf = '07823507129'
situacao = 'Ativo'
perfil = 'Moderado'
planejador = 'Pedro Jobim'
geraQuadro(api_key,token,board_id,list_id,titulo,desc,corretoras,cpf,situacao,perfil,planejador)




