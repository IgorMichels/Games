'''
Sudoku solver
Solves almost all puzzles

Author : Igor Patrício Michels
		 Fernanda Luísa Silva Gomes (https://github.com/fernandalsgomes)
'''

import numpy as np
from os import system, name
from copy import deepcopy

if name == 'nt':
	limpar = 'cls'
else:
	limpar = 'clear'

def solved(puzzle):
	if 0 in puzzle:
		return False
		
	for i in range(puzzle.shape[0]):
		if len(np.unique(puzzle[i])) != 9:
			return False
			
		if len(np.unique(puzzle[:, i])) != 9:
			return False
			
	for i in range(3):
		for j in range(3):
			if len(np.unique(puzzle[3 * i : 3 * i + 3, 3 * j : 3 * j + 3])) != 9:
				return False
				
	return True
	
def print_puzzle(puzzle):
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
	print('\033[94m{}\033[0m'.format(luc + 8 * (h + uc) + h + ruc))
	cont = 0
	for i in range(9):
		cont += 1
		line = '\033[94m{}\033[0m'.format(v)
		for j in range(9):
			if puzzle[i, j] == 0:
				line += ' '
			elif puzzle[i, j] == 10:
				line += '?'
			else:
				line += str(puzzle[i, j])
				
			if j == 2 or j == 5 or j == 8:
				line += '\033[94m{}\033[0m'.format(v)
			else:
				line += v
			
		print(line)
		if cont == 9:
			print('\033[94m{}\033[0m'.format(lbc + 8 * (h + bc) + h + rbc))
		elif cont == 3 or cont == 6:
			print('\033[94m{}\033[0m'.format(lc + 8 * (h + c) + h + rc))
		else:
			print('\033[94m{}\033[0m'.format(lc), 2 * (h + c) + h, '\033[94m{}\033[0m'.format(c), 2 * (h + c) + h, '\033[94m{}\033[0m'.format(c), 2 * (h + c) + h, '\033[94m{}\033[0m'.format(rc), sep = '')
	
def input_puzzle():
	puzzle = np.zeros((9, 9), dtype = int)
	for i in range(9):
		for j in range(9):
			puzzle[i, j] = 10
			inputed = False
			while not inputed:
				system(limpar)
				print_puzzle(puzzle)
				v = int(input("Qual o valor dessa casa? "))
				row = v not in puzzle[i, :]
				column = v not in puzzle[:, j]
				subgrid = v not in puzzle[3 * (i // 3) : 3 * (i // 3) + 3, 3 * (j // 3) : 3 * (j // 3) + 3]
				rng = 0 < v < 10
				if v == 0 or (row and column and subgrid and rng):
					puzzle[i, j] = v
					inputed = True
				
	return puzzle
	
def options(puzzle):
	options = []
	for i in range(9):
		options.append([])
		row = puzzle[i, :]
		for j in range(9):
			options[-1].append([])
			col = puzzle[:, j]
			sub = puzzle[3 * (i // 3) : 3 * (i // 3) + 3, 3 * (j // 3) : 3 * (j // 3) + 3]
			if puzzle[i, j] == 0:
				for k in range(1, 10):
					if (k not in row) and (k not in col) and (k not in sub):
						options[-1][-1].append(k)
			else:
				options[-1][-1].append(puzzle[i, j])
					
	return options
	
def solve(puzzle):
	while not solved(puzzle):
		opt = options(puzzle)
		added = False
		for row in opt:
			if [] in row:
				return puzzle
			
		for i in range(9):
			for j in range(9):
				if puzzle[i, j] == 0 and len(opt[i][j]) == 1:
					puzzle[i, j] = opt[i][j][0]
					opt = options(puzzle)
					added = True
					
		for i in range(9):
			for k in range(1, 10):
				cont_row = 0
				ind_row = 0
				cont_col = 0
				ind_col = 0
				for j in range(9):
					if k in opt[i][j]:
						cont_row += 1
						ind_row = j
						
					if k in opt[j][i]:
						cont_col += 1
						ind_col = j
						
				if puzzle[i, ind_row] == 0 and cont_row == 1:
					puzzle[i, ind_row] = k
					opt = options(puzzle)
					added = True
					
				if puzzle[ind_col, i] == 0 and cont_col == 1:
					puzzle[ind_col, i] = k
					opt = options(puzzle)
					added = True
		
		for k in range(1, 10):
			aux1 = np.zeros((3, 3), dtype = int)
			aux2 = np.zeros((3, 3, 2), dtype = int)
			for i in range(9):
				for j in range(9):
					if k in opt[i][j]:
						aux1[i // 3, j // 3] += 1
						aux2[i // 3, j // 3, 0] = i
						aux2[i // 3, j // 3, 1] = j
						
			for i in range(3):
				for j in range(3):
					if puzzle[aux2[i, j, 0], aux2[i, j, 1]] == 0 and aux1[i, j] == 1:
						puzzle[aux2[i, j, 0], aux2[i, j, 1]] = k
						opt = options(puzzle)
						added = True
		
		if not added:
			for i in range(9):
				for j in range(9):
					if len(opt[i][j]) == 2:
						aux1 = deepcopy(puzzle)
						aux1[i, j] = opt[i][j][0]
						pos1 = solve(aux1)
						if solved(pos1):
							return pos1
							
						aux2 = deepcopy(puzzle)
						aux2[i, j] = opt[i][j][1]
						pos2 = solve(aux2)
						if solved(pos2):
							return pos2
		
	return puzzle
	
puzzle1 = np.array([[3, 1, 5, 6, 0, 0, 0, 0, 4],
				    [0, 9, 0, 0, 0, 0, 2, 0, 0],
				    [2, 0, 0, 5, 9, 0, 0, 1, 3],
				    [0, 6, 0, 1, 7, 5, 0, 0, 0],
				    [1, 8, 0, 3, 0, 0, 7, 0, 0],
				    [5, 3, 0, 0, 4, 0, 0, 9, 6],
				    [0, 2, 9, 0, 5, 1, 0, 7, 8],
				    [0, 0, 0, 0, 3, 0, 0, 2, 0],
				    [7, 4, 3, 0, 0, 2, 5, 0, 0]])
	
puzzle2 = np.array([[0, 9, 0, 8, 0, 7, 4, 0, 0],
				    [0, 0, 5, 0, 0, 0, 0, 6, 0],
				    [0, 0, 0, 0, 2, 0, 0, 0, 0],
				    [0, 0, 0, 0, 9, 0, 2, 0, 0],
				    [6, 0, 0, 2, 0, 1, 0, 4, 0],
				    [0, 1, 0, 0, 3, 0, 0, 0, 0],
				    [9, 0, 0, 0, 0, 0, 0, 0, 7],
				    [0, 7, 0, 1, 0, 4, 8, 0, 0],
				    [0, 0, 0, 0, 0, 3, 0, 0, 0]])

puzzle3 = np.array([[0, 0, 6, 0, 0, 0, 0, 0, 0],
				    [9, 2, 0, 0, 0, 3, 4, 0, 0],
				    [0, 0, 0, 0, 8, 0, 0, 0, 1],
				    [5, 6, 0, 0, 3, 0, 0, 8, 0],
				    [0, 0, 7, 0, 0, 0, 5, 0, 0],
				    [0, 0, 4, 0, 0, 6, 0, 0, 0],
				    [7, 0, 0, 0, 0, 0, 0, 0, 0],
				    [0, 0, 0, 9, 0, 0, 0, 4, 0],
				    [3, 5, 0, 0, 0, 2, 9, 0, 0]])

puzzle4 = np.array([[8, 0, 5, 0, 0, 9, 3, 0, 0],
				    [2, 0, 0, 0, 0, 0, 0, 0, 0],
				    [0, 0, 0, 6, 0, 0, 0, 0, 9],
				    [0, 4, 0, 0, 0, 0, 2, 0, 0],
				    [9, 0, 3, 0, 0, 6, 8, 0, 0],
				    [0, 0, 0, 0, 1, 0, 0, 7, 0],
				    [0, 2, 0, 0, 0, 5, 0, 0, 0],
				    [5, 0, 4, 7, 0, 0, 0, 8, 0],
				    [0, 6, 0, 0, 0, 0, 4, 0, 0]])

print_puzzle(puzzle1)
print_puzzle(solve(puzzle1))

print_puzzle(puzzle2)
print_puzzle(solve(puzzle2))

print_puzzle(puzzle3)
print_puzzle(solve(puzzle3))

print_puzzle(puzzle4)
print_puzzle(solve(puzzle4))
