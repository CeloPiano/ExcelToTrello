import difflib
import numpy as np
import math

entradas_campos_personalizados = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabriel Beigelman", "Igor Falcão", "João Pessine", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo"]

valor = 'Ativo'
valor_corrigido = difflib.get_close_matches(valor, entradas_campos_personalizados)

# print(valor_corrigido)


import pandas as pd

df = pd.read_excel('tabela_clientes_leite.xlsx')
valor = df['CPF'][95]
# valor = df['CPF']

# nan = float('nan')
# if not math.isnan(valor):
#     print('é VAZIO')
# else:
#     print('VAZIUUUUU')

valor2 = df.loc[95,'CPF']
print(valor2)
# print(valor)
print(pd.isna(valor))








