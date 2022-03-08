import numpy as np
from copy import deepcopy

game = np.array([[1, 2, 3, 3],
				 [3, 2, 1, 3],
				 [2, 1, 1, 2],
				 [0, 0, 0, 0],
				 [0, 0, 0, 0]])

game1 = np.array([[1, 2, 3, 4],
	 			  [5, 6, 7, 8],
	 			  [5, 5, 3, 9],
				  [10, 6, 11, 9],
				  [12, 9, 2, 2],
				  [8, 5, 7, 10],
				  [3, 11, 7, 3],
				  [1, 9, 4, 11],
				  [8, 1, 12, 6],
				  [12, 2, 7, 4],
				  [11, 1, 6, 10],
				  [12, 4, 10, 8],
				  [0, 0, 0, 0],
				  [0, 0, 0, 0]])

game2 = np.array([[1, 2, 3, 4],
				  [2, 5, 6, 1],
				  [7, 6, 4, 8],
				  [9, 10, 7, 11],
				  [12, 2, 3, 10],
				  [13, 1, 3, 11],
				  [9, 11, 10, 13],
				  [5, 6, 9, 5],
				  [8, 4, 8, 10],
				  [5, 8, 12, 11],
				  [6, 13, 12, 2],
				  [9, 3, 1, 13],
				  [7, 4, 12, 7],
				  [0, 0, 0, 0],
				  [0, 0, 0, 0]])

def is_valid(game):
	r, c = game.shape
	values = {}
	for i in range(r):
		for j in range(c):
			if game[i, j] not in values:
				values[game[i, j]] = 1
			else:
				values[game[i, j]] += 1
				
	for value in np.unique(game):
		if value == 0 and values[value] != 8:
			return False
		elif value != 0 and values[value] != 4:
			print(value)
			return False
			
	return True

def find_moves(game):
	r, c = game.shape
	possible_moves = []
	for i in range(r):
		if game[i, 0] == 0:
			continue
		elif 0 in game[i, :]:
			piece = np.where(game[i, :] == 0)[0][0] - 1
		elif len(np.unique(game[i, :])) == 1:
			continue
		else:
			piece = 3
			
		for j in range(r):
			if i != j:
				if game[j, 0] == 0:
					possible_moves.append((i, piece, j, 0))
				elif game[j, 0] == game[i, piece] and game[j, 1] == 0:
					possible_moves.append((i, piece, j, 1))
				elif game[j, 1] == game[i, piece] and game[j, 2] == 0:
					possible_moves.append((i, piece, j, 2))
				elif game[j, 2] == game[i, piece] and game[j, 3] == 0:
					possible_moves.append((i, piece, j, 3))
				
	return possible_moves
	
def make_move(game, move):
	moved_game = deepcopy(game)
	rs, cs, rt, ct = move
	moved_game[rt, ct] = moved_game[rs, cs]
	moved_game[rs, cs] = 0
	return moved_game
	
def make_moves(game, moves, printing = False):
	moved_game = deepcopy(game)
	if printing:
		print(moved_game)
		print(f(moved_game, []))
		
	for i in range(len(moves)):
		moved_game = make_move(moved_game, moves[i])
		if printing:
			print(moved_game)
			print(f(moved_game, moves[:i + 1]))
			print()
	
	return moved_game
	
def is_solved(game):
	for i in range(game.shape[0]):
		if len(np.unique(game[i, :])) != 1:
			return False
			
	return True
	
def h(game):
	if is_solved(game):
		return 0
	
	cost = 0
	for i in range(game.shape[0]):
		if game[i, 1] != game[i, 0]:
			cost += 3
			if game[i, 2] == game[i, 0]:
				cost += 2
			
			if game[i, 3] == game[i, 0]:
				cost += 1
		elif game[i, 2] != game[i, 0]:
			cost += 2
			if game[i, 3] == game[i, 0]:
				cost += 1
		elif game[i, 3] != game[i, 0]:
			cost += 1
	
	cost += (game.shape[0] - len(np.unique(game[:, 0]))) * 4
	cost += (game.shape[0] - len(np.unique(game[:, 1]))) * 3
	cost += (game.shape[0] - len(np.unique(game[:, 2]))) * 2
	cost += (game.shape[0] - len(np.unique(game[:, 3]))) * 1
	
	return cost
	
def f(game, moves):
	return len(moves) + h(game)
	
def breadth_first_solve(game, max_iter = 10000):
	o_games = [game.tolist()]
	o_moves = [[]]
	c_games = []
	c_moves = []
	k = 0
	while True and k < max_iter:
		position = np.array(o_games.pop(0))
		moves = o_moves.pop(0)
		if is_solved(position):
			return moves
			
		possible_moves = find_moves(position)
		for move in possible_moves:
			aux_position = deepcopy(position)
			aux_position = make_move(aux_position, move).tolist()
			if aux_position not in (o_games + c_games):
				o_games.append(aux_position)
				o_moves.append(moves + [move])
				
		c_games.append(position.tolist())
		c_moves.append(moves)
		k += 1
	
def a_star_solve(game, max_iter = 10000):
	o_games = [game.tolist()]
	o_moves = [[]]
	c_games = []
	c_moves = []
	k = 0
	while True and k < max_iter:
		values = []
		for i in range(len(o_games)):
			values.append(f(np.array(o_games[i]), o_moves[i]))
			
		i = np.argmin(values)
		position = np.array(o_games.pop(i))
		moves = o_moves.pop(i)
		if is_solved(position):
			return moves
			
		possible_moves = find_moves(position)
		for move in possible_moves:
			aux_position = deepcopy(position)
			aux_position = make_move(aux_position, move).tolist()
			if aux_position not in (o_games + c_games):
				o_games.append(aux_position)
				o_moves.append(moves + [move])
				
		c_games.append(position.tolist())
		c_moves.append(moves)
		k += 1
	
solution1 = [(2, 3, 13, 0), (6, 3, 2, 3), (6, 2, 12, 0), (7, 3, 6, 2), (9, 3, 7, 3), (9, 2, 12, 1), (4, 3, 9, 2), (4, 2, 9, 3), (4, 1, 13, 1), (3, 3, 13, 2), (3, 2, 6, 3), (8, 3, 3, 2), (4, 0, 8, 3), (1, 3, 4, 0), (1, 2, 12, 2), (1, 1, 3, 3), (11, 3, 4, 1), (5, 3, 11, 3), (5, 2, 12, 3), (5, 1, 1, 1), (5, 0, 4, 2), (3, 3, 5, 0), (3, 2, 5, 1), (3, 1, 5, 2), (10, 3, 3, 1), (10, 2, 5, 3), (11, 3, 3, 2), (11, 2, 3, 3), (7, 3, 11, 2), (7, 2, 11, 3), (7, 1, 13, 3), (7, 0, 10, 2), (0, 3, 7, 0), (11, 3, 7, 1), (11, 2, 7, 2), (11, 1, 7, 3), (8, 3, 11, 1), (8, 2, 11, 2), (8, 1, 10, 3), (8, 0, 4, 3), (2, 3, 0, 3), (2, 2, 8, 0), (1, 1, 2, 2), (1, 0, 2, 3), (0, 3, 8, 1), (0, 2, 8, 2), (0, 1, 1, 0), (9, 3, 1, 1), (9, 2, 1, 2), (9, 1, 1, 3), (9, 0, 11, 3), (10, 3, 0, 1), (10, 2, 0, 2), (10, 1, 0, 3), (6, 3, 10, 1), (6, 2, 10, 2), (6, 1, 10, 3), (6, 0, 8, 3)]

solution2 = [(3, 3, 13, 0), (5, 3, 13, 1), (9, 3, 13, 2), (12, 3, 3, 3), (12, 2, 9, 3), (12, 1, 14, 0), (3, 3, 12, 1), (3, 2, 12, 2), (8, 3, 3, 2), (2, 3, 8, 3), (0, 3, 14, 1), (2, 2, 14, 2), (5, 2, 0, 3), (1, 3, 5, 2), (2, 1, 1, 3), (2, 0, 12, 3), (4, 3, 3, 3), (4, 2, 2, 0), (0, 3, 2, 1), (0, 2, 2, 2), (4, 1, 0, 2), (10, 3, 0, 3), (10, 2, 4, 1), (11, 3, 10, 2), (11, 2, 5, 3), (11, 1, 2, 3), (9, 3, 4, 2), (9, 2, 4, 3), (8, 3, 9, 2), (8, 2, 9, 3), (8, 1, 14, 3), (9, 3, 8, 1), (9, 2, 8, 2), (9, 1, 8, 3), (7, 3, 9, 1), (11, 0, 7, 3), (6, 3, 10, 3), (6, 2, 11, 0), (6, 1, 13, 3), (7, 3, 6, 1), (7, 2, 6, 2), (1, 3, 7, 2), (1, 2, 7, 3), (1, 1, 9, 2), (3, 3, 11, 1), (3, 2, 11, 2), (3, 1, 11, 3), (3, 0, 6, 3), (0, 3, 1, 1), (0, 2, 1, 2), (0, 1, 1, 3), (5, 3, 0, 1), (5, 2, 0, 2), (5, 1, 0, 3), (10, 3, 5, 1), (10, 2, 5, 2), (10, 1, 5, 3), (7, 3, 10, 1), (7, 2, 10, 2), (7, 1, 10, 3), (7, 0, 9, 3)]

if is_valid(game):
	solution = a_star_solve(game)
	print(solution)
	game = make_moves(game, solution, True)
