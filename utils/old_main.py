from trello import TrelloClient
import pandas as pd
import os
import difflib

from trello_utils import *

# correção de nomes (aqui temos todas as opções do trello de campos personalizados quando se trata de listas)
entradas_campos_personalizados = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabrihel Beigelman", "Igor Falcão", "João Pessini", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo"]

token = os.environ.get('API_TOKEN')
api_key = os.environ.get('API_KEY')

# selecionar o quadro que os card vão ficar
board_id = boards_ids['balanceamento_jobim']

# selecionar o a lista que vao entrar os cards 
list_id = '63e23e54e799fdd213174e03'

# pegar o client
client = TrelloClient(api_key, token)

# CRIA UMA LISTA COM TODOS OS NOMES JÁ EXISTENTES NO QUADRO (puxa do banco do trello todos os nomes) (é por quadro)
lista_nome_card_existente = []
lista_nome_card_existente = verifica_nomes(client)
# print(lista_nome_card_existente)
    
# Acessar o excel
# colocar todos os clientes em uma lista com seus respectivos campos
# Panda lê do excel 
df = pd.read_excel('tabela_clientes_jobim.xlsx')

# pegar o numero das linhas (shape retorna uma tupla quantidade de (qtdLinhas,qtdColunas))
numero_linhas = df.shape[0]

# lista para fazer a filtragem (Aqui devo adicionar correspondente a tabela .xlsx) não tem as Corretoras
lista_colunas_corretas = ['Nome', 'CPF', "Situacao", "Perfil", "Planejador"]

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
            
            # verifica se não está no final da planilha
            if indice_linha < numero_linhas - 1: 
                # print(df['Nome'][indice_linha + 1])
                if df['Nome'][indice_linha] == df['Nome'][indice_linha + 1]:
                    argumentos[coluna].append(df['Corretoras'][indice_linha + 1])
    
    titulo = formatar_string(argumentos['Nome']) 
    planejador = argumentos['Planejador']
    corretoras = argumentos['Corretoras'] 
    perfil = argumentos['Perfil']
    cpf = argumentos['CPF'] 
    situacao = argumentos['Situacao']
    
    # ajustar os perfis
    # aqui fazemos um filtro para não haver nomes repetidos no quadro
    if cpf not in lista_nome_card_existente and titulo not in lista_nome_card_existente and titulo not in lista_nomes_adicionados_atual:
        # geramos o quadro depois de verificar onde 
        print(f'Criando card da {titulo}...')
        geraQuadro(client,board_id,list_id,titulo,'',corretoras,cpf,situacao,perfil,planejador)
    
    # essa lista é por requisição, para não ter que fazer uma chamada geral a cada requisição (o que é mais custoso)
    lista_nomes_adicionados_atual.append(titulo)
    indice_linha += 1





