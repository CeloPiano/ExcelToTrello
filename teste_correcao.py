import difflib

entradas_campos_personalizados = ['Ativo', "Inativo", "Bloqueado", "Excluir", "Portabilidade","Leonardo Pavan",
                                  "Gustavo Nasr", "Gabriel Beigelman", "Igor Falcão", "João Pessine", "Matheus Vilar",
                                  "Laianna Santiago","Pedro Jobim", "Pedro Leite", "Rafael Rabelo", "Rafael Santos",
                                  "Reinaldo Palmeira", "Credito Privado", "Conservador", "Conservador-Moderado","Agressivo"]

valor = 'Ativo'
valor_corrigido = difflib.get_close_matches(valor, entradas_campos_personalizados)

print(valor_corrigido)