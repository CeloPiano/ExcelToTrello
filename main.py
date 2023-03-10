from trello import TrelloClient

from push import geraQuadro
import pandas as pd
import os
import difflib


token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

board_id ='6408e8c5d254de205a5d7759'
list_id = '6408e8c5d254de205a5d7761'





# acessar a excel
# colocar todos os clientes em uma lista com seus respectivos campos

# correção de nomes 
entradas_campos_personalizados = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabriel Beigelman", "Igor Falcão", "João Pessine", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo"]

# Antes CRIAR UMA LISTA COM TODOS OS NOMES JÁ EXISTENTES NO BOAR
client = TrelloClient(api_key, token)
board = client.get_board(board_id)
lista_objetos = board.get_cards()
lista_nome_card_existente = []
for elemento in lista_objetos:
    lista_nome_card_existente.append(elemento.name)


# Panda lê do excel 
df = pd.read_excel('tabela_nomes.xlsx')

# pegar o numero das linhas (shape retorna uma tupla quantidade de (qtdLinhas,qtdColunas))
numero_linhas = df.shape[0]

# lista para fazer a filtragem (Aqui devo adicionar correspondente a tabela)
lista_colunas_corretas = ['Nome', 'Corretoras', 'CPF', "Situação", "Perfil", "Planejador"]

# iteração nas linhas para juntar todos os argumentos por cliente e adicionar no trello
# Ordem: Nome, Corretora, CPF, Situação, Perfil, Nome do Planejador/Planejador
for linha in range(numero_linhas):
    # lista para alocar os argumentos
    argumentos = {}
    
    for coluna in df.columns:
        
        # esse é o valor = df[coluna][linha]
        valor = df[coluna][linha]
            
        # fazer a filtragem da coluna 
        if coluna in lista_colunas_corretas:
            valor_corrigido = difflib.get_close_matches(valor, entradas_campos_personalizados)
            print(valor)
            argumentos[coluna] = valor
            # if len(valor_corrigido) != 0:
            #     print("corrigido!")
            #     argumentos[coluna] = valor_corrigido[0]
            # else:
            #     argumentos[coluna] = valor

    
    titulo = argumentos['Nome'] 
    corretoras = [argumentos['Corretoras']] 
    cpf = argumentos['CPF'] 
    situacao = argumentos['Situação'] 
    perfil = argumentos['Perfil']
    planejador = argumentos['Planejador']
    
    # aqui fazemos um filtro para não haver nomes repetidos
    if titulo not in lista_nome_card_existente:
        geraQuadro(api_key,token,board_id,list_id,titulo,'',corretoras,cpf,situacao,perfil,planejador)


# temos que chamar isso iterativamente pra cada coluna 
# aqui criamos o quadro com todos os argumentos...
# titulo = 'Joseph Climber'
# desc = 'Aqui vai dar certo a label'
# corretoras = ['Genial', 'BTG']
# cpf = '07823507129'
# situacao = 'Ativo'
# perfil = 'Moderado'
# planejador = 'Pedro Jobim'
# geraQuadro(api_key,token,board_id,list_id,titulo,desc,corretoras,cpf,situacao,perfil,planejador)




