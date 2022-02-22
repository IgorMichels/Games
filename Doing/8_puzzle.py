import numpy as np
from copy import deepcopy
import time

def print_game(game):
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
	
	print(luc + (h + uc) * 2 + h + ruc)
	for i in range(3):
		line = v
		for j in range(3):
			if game[i][j] == 0:
				line += ' ' + v
			else:
				line += str(game[i][j]) + v
				
		print(line)
		if i != 2:
			print(lc + (h + c) * 2 + h + rc)
		else:
			print(lbc + (h + bc) * 2 + h + rbc)

def find_moves(game):
	game = np.array(game)
	r, c = np.where(game == 0)
	r, c = r[0], c[0]
	moves = []
	for change in [-1, 1]:
		if c + change in [0, 1, 2]:
			moves.append([r, c, r, c + change])
			
		if r + change in [0, 1, 2]:
			moves.append([r, c, r + change, c])
			
	return moves

def make_move(game, move):
	new_game = deepcopy(game)
	r0, c0, r1, c1 = move
	new_game[r0][c0], new_game[r1][c1] = new_game[r1][c1], new_game[r0][c0]
	
	return new_game

def make_moves(game, moves, printing = False):
	new_game = deepcopy(game)
	if printing:
		print_game(game)
	
	for move in moves:
		new_game = make_move(new_game, move)
		
		if printing:
			print(move)
			print_game(new_game)
		
	return new_game

def solve_game_bf(game):
	positions = [game]
	moves_to_pos = [[]]
	solution = [[1, 2, 3],
				[4, 5, 6],
				[7, 8, 0]]
				
	k = 0
	while k < len(positions):
		moves = find_moves(positions[k])
		moves_to_now = deepcopy(moves_to_pos[k])
		for move in moves:
			new_game = deepcopy(positions[k])
			new_game = make_move(new_game, move)
			if new_game == solution:
				return moves_to_now + [move]
			elif new_game not in positions:
				positions.append(new_game)
				moves_to_pos.append(moves_to_now + [move])
		
		k += 1
				 
game = [[7, 2, 4],
     	[5, 0, 6],
		[8, 3, 1]]

t = time.time()
moves = solve_game_bf(game)
tf = time.time()
new_game = make_moves(game, moves, True)
print(len(moves), moves)
print(f'{tf - t} seconds.')
