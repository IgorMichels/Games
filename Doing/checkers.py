import numpy as np

def print_board(board):
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
	
	b = '\033[94m\033[104m\u2588\033[0m'
	r = '\033[91m\033[101m\u2588\033[0m'
	crowned_b = '\033[93m\033[104m\u1f45\033[0m'
	crowned_r = '\033[93m\033[101m\u1f45\033[0m'
	print(luc + 7 * (h + uc) + h + ruc)
	for i in range(8):
		line = v
		for j in range(8):
			if board[i, j, 0] and board[i, j, 2]:
				line += crowned_b
			elif board[i, j, 0]:
				line += b
			elif board[i, j, 1] and board[i, j, 2]:
				line += crowned_r
			elif board[i, j, 1]:
				line += r
			else:
				line += ' '
				
			line += v
		
		print(line)
		if i == 7:
			print(lbc + 7 * (h + bc) + h + rbc)
		else:
			print(lc + 7 * (h + c) + h + rc)
		
def init_board():
	board = np.zeros((8, 8, 3), dtype = bool)
	for i in range(3):
		for j in range(4):
			board[i, 2 * j + (i + 1) % 2, 0] = True
			board[7 - i, 2 * j + i % 2, 1] = True
			
	return board
	
board = init_board()
print_board(board)
