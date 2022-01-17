import numpy as np
from os import system

w = '\033[97m\033[107m\u2588\033[0m'
b = '\033[94m\033[104m\u2588\033[0m'
r = '\033[91m\033[101m\u2588\033[0m'
dic = {0 : w, 1 : r, 2 : b}

luc = '\u250c'
uc  = '\u252C'
ruc = '\u2510'
lc  = '\u251C'
c   = '\u253C'
rc  = '\u2524'
lbc = '\u2514'
bc  = '\u2534'
rbc = '\u2518'
h   = '\u2500'
v   = '\u2502'

def print_tabuleiro(tabuleiro):
	cont = 1
	print(luc + (len(tabuleiro) - 1) * (h + uc) + h + ruc)
	print_linha1 = lc + (len(tabuleiro) - 1) * (h + c) + h + rc
	for linha in tabuleiro:
		print_linha2 = v
		for elemento in linha:
			if elemento == 4:
				print_linha2 += ' ' + v
			elif elemento == 3:
				print_linha2 += '?' + v
			else:
				print_linha2 += dic[elemento] + v
			
		print(print_linha2)
		if cont != len(tabuleiro):
			print(print_linha1)
		
		cont += 1
		
	print(lbc + (len(tabuleiro) - 1) * (h + bc) + h + rbc)

def input_tabuleiro(tabuleiro):
	n = len(tabuleiro)
	for i in range(n):
		for j in range(n):
			tabuleiro[i, j] = 3
			print_tabuleiro(tabuleiro)
			cor = int(input(f'Digite a cor da casa selecionada (0 para {w}, 1 para {r} e 2 para {b}): '))
			while cor not in [0, 1, 2]:
				system('clear')
				print('A cor deve ser 0, 1 ou 2')
				print()
				print_tabuleiro(tabuleiro)
				cor = int(input(f'Digite a cor da casa selecionada (0 para {w}, 1 para {r} e 2 para {b}): '))
			
			tabuleiro[i, j] = cor
			system('clear')
			
	return tabuleiro

def verifica_validade(tabuleiro):
	n = len(tabuleiro) // 2
	for i in range(2 * n):
		# testando quantidade de cada cor nas linhas e colunas
		a = [0, 0]
		v = [0, 0]
		for j in range(2 * n):
			if tabuleiro[i, j] == 1:
				v[0] += 1
			elif tabuleiro[i, j] == 2:
				a[0] += 1
			
			if tabuleiro[j, i] == 1:
				v[1] += 1
			elif tabuleiro[j, i] == 2:
				a[1] += 1
				
		if (np.array(a + v) > n).any():
			return False
			
		# testando se tem três cores consecutivas iguais
		for j in range(2 * n - 2):
			if tabuleiro[i, j] == tabuleiro[i, j + 1] == tabuleiro[i, j + 2]:
				return False
			
			if tabuleiro[j, i] == tabuleiro[j + 1, i] == tabuleiro[j + 2, i]:
				return False
		
		# testando se tem duas linhas ou colunas iguais
		for j in range(i + 1, 2 * n):
			if (tabuleiro[i, :] == tabuleiro[j, :]).all():
				return False
			
			if (tabuleiro[:, i] == tabuleiro[:, j]).all():
				return False
				
	return True
	
def verifica_solucao(tabuleiro):
	# o tabuleiro precisa ser válido
	if verifica_validade(tabuleiro):
		# e não ter espaços em branco
		if (tabuleiro != 0).all():
			return True

	return False

def dois_consecutivos(tabuleiro):
	# aplica a primeira regra: não podemos ter mais de dois
	# quadrados consecutivos com a mesma cor
	n = len(tabuleiro)
	for i in range(n):
		if tabuleiro[i, 0] == tabuleiro[i, 1] == 1:
			tabuleiro[i, 2] = 2
		elif tabuleiro[i, 0] == tabuleiro[i, 1] == 2:
			tabuleiro[i, 2] = 1
			
		if tabuleiro[i, -1] == tabuleiro[i, -2] == 1:
			tabuleiro[i, -3] = 2
		elif tabuleiro[i, -1] == tabuleiro[i, -2] == 2:
			tabuleiro[i, -3] = 1
		
		if tabuleiro[0, i] == tabuleiro[1, i] == 1:
			tabuleiro[2, i] = 2
		elif tabuleiro[0, i] == tabuleiro[1, i] == 2:
			tabuleiro[2, i] = 1
			
		if tabuleiro[-1, i] == tabuleiro[-2, i] == 1:
			tabuleiro[-3, i] = 2
		elif tabuleiro[-1, i] == tabuleiro[-2, i] == 2:
			tabuleiro[-3, i] = 1
		
		for j in range(1, n - 2):
			if tabuleiro[i, j] == tabuleiro[i, j + 1] == 1:
				tabuleiro[i, j + 2] = 2
				tabuleiro[i, j - 1] = 2
			elif tabuleiro[i, j] == tabuleiro[i, j + 1] == 2:
				tabuleiro[i, j + 2] = 1
				tabuleiro[i, j - 1] = 1
			
			if tabuleiro[j, i] == tabuleiro[j + 1, i] == 1:
				tabuleiro[j + 2, i] = 2
				tabuleiro[j - 1, i] = 2
			elif tabuleiro[j, i] == tabuleiro[j + 1, i] == 2:
				tabuleiro[j + 2, i] = 1
				tabuleiro[j - 1, i] = 1
				
	return tabuleiro

def verifica_meio(tabuleiro):
	# outra forma de aplicar a primeira regra, com foco em outro caso
	n = len(tabuleiro)
	for i in range(n):
		for j in range(1, n - 1):
			if tabuleiro[i, j - 1] == tabuleiro[i, j + 1] == 1:
				tabuleiro[i, j] = 2
			
			if tabuleiro[j - 1, i] == tabuleiro[j + 1, i] == 1:
				tabuleiro[j, i] = 2
			
			if tabuleiro[i, j - 1] == tabuleiro[i, j + 1] == 2:
				tabuleiro[i, j] = 1
			
			if tabuleiro[j - 1, i] == tabuleiro[j + 1, i] == 2:
				tabuleiro[j, i] = 1
	
	return tabuleiro

def completar_linha(tabuleiro):
	# aplica a segunda regra: as linhas/colunas devem ter a mesma quantidade
	# de quadrados azuis e vermelhos
	n = len(tabuleiro) // 2
	for i in range(2 * n):
		if sum(tabuleiro[i, :] == 1) == n and (tabuleiro[i, :] == 0).any():
			for j in range(2 * n):
				if tabuleiro[i, j] == 0:
					tabuleiro[i, j] = 2
					
		if sum(tabuleiro[i, :] == 2) == n and (tabuleiro[i, :] == 0).any():
			for j in range(2 * n):
				if tabuleiro[i, j] == 0:
					tabuleiro[i, j] = 1
					
		if sum(tabuleiro[:, i] == 1) == n and (tabuleiro[:, i] == 0).any():
			for j in range(2 * n):
				if tabuleiro[j, i] == 0:
					tabuleiro[j, i] = 2
					
		if sum(tabuleiro[:, i] == 2) == n and (tabuleiro[:, i] == 0).any():
			for j in range(2 * n):
				if tabuleiro[j, i] == 0:
					tabuleiro[j, i] = 1
					
	return tabuleiro

def vetores_iguais(tabuleiro):
	# aplica a terceira regra: não podemos ter duas linhas/colunas iguais
	n = len(tabuleiro)
	for i in range(n):
		if sum(tabuleiro[i, :] == 0) == 2:
			for j in range(n):
				if j != i:
					if sum(tabuleiro[i, :] != tabuleiro[j, :]) == 2:
						for k in range(n):
							if tabuleiro[i, k] == 0:
								if tabuleiro[j, k] == 1:
									tabuleiro[i, k] = 2
								elif tabuleiro[j, k] == 2:
									tabuleiro[i, k] = 1
		
		if sum(tabuleiro[:, i] == 0) == 2:
			for j in range(n):
				if i != j:
					if sum(tabuleiro[:, i] != tabuleiro[:, j]) == 2:
						for k in range(n):
							if tabuleiro[k, i] == 0:
								if tabuleiro[k, j] == 1:
									tabuleiro[k, i] = 2
								elif tabuleiro[j, k] == 2:
									tabuleiro[k, i] = 1
	
	return tabuleiro

def resolve(tabuleiro):
	while not verifica_solucao(tabuleiro):
		tabuleiro = dois_consecutivos(tabuleiro)
		tabuleiro = verifica_meio(tabuleiro)
		tabuleiro = completar_linha(tabuleiro)
		tabuleiro = vetores_iguais(tabuleiro)
		
	return tabuleiro

system('clear')
n = float(input('Qual a dimensão do tabuleiro? '))
while n.is_integer() == False or int(n) % 2 == 1 or int(n) < 3:
	system('clear')
	print('A dimensão deve ser um inteiro par maior que 2!')
	n = float(input('Qual a dimensão do tabuleiro? '))
	
system('clear')
n = int(n)
tabuleiro = [[4 for i in range(n)] for j in range(n)]
tabuleiro = np.array(tabuleiro, dtype = int)
tabuleiro = input_tabuleiro(tabuleiro)

print_tabuleiro(tabuleiro)
tabuleiro = resolve(tabuleiro)
print_tabuleiro(tabuleiro)

'''
system('clear')
n = 8
tabuleiro = np.array([[0, 0, 0, 2, 0, 0, 0, 2],
					  [0, 0, 0, 0, 1, 0, 0, 0],
					  [0, 0, 1, 0, 0, 0, 1, 0],
					  [0, 0, 0, 1, 0, 0, 0, 0],
					  [2, 0, 0, 0, 0, 1, 1, 0],
					  [0, 2, 0, 0, 0, 0, 0, 0],
					  [0, 0, 0, 0, 1, 0, 0, 1],
					  [0, 0, 1, 0, 0, 2, 2, 0]],
					  dtype = int)
					  
print_tabuleiro(tabuleiro)
tabuleiro = resolve(tabuleiro)
print_tabuleiro(tabuleiro)
'''
