import time
import numpy as np
import random as rd
from copy import deepcopy
from os import system, name

if name == 'nt':
	limpar = 'cls'
else:
	limpar = 'clear'

def print_position(position):
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
			if position[i][j] == 0:
				line += ' ' + v
			else:
				line += str(position[i][j]) + v
				
		print(line)
		if i != 2:
			print(lc + (h + c) * 2 + h + rc)
		else:
			print(lbc + (h + bc) * 2 + h + rbc)

def check_parity(position):
	game = []
	for row in position:
		game += row
		
	game.remove(0)
	game = np.array(game)
	parity = 0
	for i in range(len(game)):
		parity += sum(game[i:] > game[i])
		
	return parity % 2

def generate_game():
	while True:
		game = [*range(9)]
		rd.shuffle(game)
		game = np.array(game).reshape((3, 3))
		game = game.tolist()
		if check_parity(game) == 0:
			return game

def find_moves(position):
	r, c = find_piece(position, 0)
	moves = []
	for change in [-1, 1]:
		if c + change in [0, 1, 2]:
			moves.append([r, c, r, c + change])
			
		if r + change in [0, 1, 2]:
			moves.append([r, c, r + change, c])
			
	return moves

def make_move(position, move):
	new_position = deepcopy(position)
	r0, c0, r1, c1 = move
	new_position[r0][c0], new_position[r1][c1] = new_position[r1][c1], new_position[r0][c0]
	
	return new_position

def make_moves(position, moves, printing = False):
	new_position = deepcopy(position)
	if printing:
		print_position(position)
	
	for move in moves:
		new_position = make_move(new_position, move)
		
		if printing:
			print(move)
			print_position(new_position)
		
	return new_position

def solve_game_bf(game, goal, max_iter = 10000):
	if check_parity(game) == 1:
		print('Game without solution')
		return None
	
	positions = [game]
	moves_to_pos = [[]]
	k = 0
	while k < len(positions) and k < max_iter:
		moves = find_moves(positions[k])
		moves_to_now = deepcopy(moves_to_pos[k])
		for move in moves:
			new_position = deepcopy(positions[k])
			new_position = make_move(new_position, move)
			if new_position == goal:
				return moves_to_now + [move]
			elif new_position not in positions:
				positions.append(new_position)
				moves_to_pos.append(moves_to_now + [move])
		
		k += 1

def h(position, goal):
	cost = 0
	for i in range(1, 9):
		r1, c1 = find_piece(position, i)
		r2, c2 = find_piece(goal, i)
		
		cost += abs(r1 - r2)
		cost += abs(c1 - c2)
		
	return cost
	
def f(position, goal, moves):
	g_cost = len(moves)
	h_cost = h(position, goal)
	
	return g_cost + h_cost
	
def solve_game_a_star(game, goal, max_iter = 100000):
	if check_parity(game) == 1:
		print('Game without solution')
		return None
	elif game == goal:
		print('Game already solved')
		return []
	
	open_positions = [game]
	close_positions = []
	moves_to_o_pos = [[]]
	moves_to_c_pos = []
	it = 0
	while it < max_iter:
		f_values = []
		for i, pos in enumerate(open_positions):
			f_values.append(f(pos, goal, moves_to_o_pos[i]))
			
		i = np.argmin(f_values)
		position = open_positions.pop(i)
		moves = moves_to_o_pos.pop(i)
		new_positions, new_moves = possible_positions(position, moves, goal)
		if new_positions == True:
			return new_moves
		
		for i, pos in enumerate(new_positions):
			if pos not in open_positions and pos not in close_positions:
				open_positions.append(pos)
				moves_to_o_pos.append(new_moves[i])
				
		close_positions.append(position)
		moves_to_c_pos.append(moves)
		it += 1

def possible_positions(position, moves, goal):
	possible_moves = find_moves(position)
	new_positions = []
	new_moves = []
	for move in possible_moves:
		new_position = deepcopy(position)
		new_position = make_move(new_position, move)
		if new_position == goal:
			return True, moves + [move]
		
		new_positions.append(new_position)
		new_moves.append(moves + [move])
		
	return new_positions, new_moves

def find_piece(position, piece):
	arr_position = np.array(position)
	r, c = np.where(arr_position == piece)
	r, c = r[0], c[0]
	
	return [r, c]

def input_move():
	move = ''
	while len(move) != 1 or not move.isdigit():
		move = input('Which piece do you want to move? ')
		
	return int(move)

def playable(game = None, goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]):
	if game is None:
		game = generate_game()
	
	position = deepcopy(game)
	while position != goal:
		possible_moves = find_moves(position)
		zero_pos = find_piece(position, 0)
		print('Goal:')
		print_position(goal)
		print()
		print('Make a move:')
		print_position(position)
		piece = input_move()
		move = zero_pos + find_piece(position, piece)
		while move not in possible_moves:
			print('Invalid move')
			piece = input_move()
			move = zero_pos + find_piece(position, piece)
			
		position = make_move(position, move)
		system(limpar)
	
	print_position(position)
	print('Congratulations! You\'ve solved this puzzle!')

system(limpar)
playable()
