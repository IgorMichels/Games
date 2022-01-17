from copy import deepcopy
import numpy as np

# table of borders
luc = '\u250c'
uc  = '\u252C'
ruc = '\u2510'
lc  = '\u251C'
c   = '\u253C'
rc  = '\u2524'
blc = '\u2514'
bc  = '\u2534'
brc = '\u2518'
h   = '\u2500'
v   = '\u2502'

# colors
w = '\033[97m\033[107m\u2588\033[0m'
o = '\033[95m\033[105m\u2588\033[0m'
g = '\033[92m\033[102m\u2588\033[0m'
b = '\033[94m\033[104m\u2588\033[0m'
r = '\033[91m\033[101m\u2588\033[0m'
y = '\033[93m\033[103m\u2588\033[0m'

cube = [[[w, w, w],
		 [w, w, w], # F
		 [w, w, w]],
		[[o, o, o],
		 [o, o, o], # U
		 [o, o, o]],
		[[g, g, g],
		 [g, g, g], # L
		 [g, g, g]],
		[[b, b, b],
		 [b, b, b], # R
		 [b, b, b]],
		[[r, r, r],
		 [r, r, r], # D
		 [r, r, r]],
		[[y, y, y],
		 [y, y, y], # B
		 [y, y, y]]]

cube = [np.matrix(face) for face in cube]

def rotate_face(cube, face):
	cube[face] = cube[face].T
	aux = deepcopy(cube[face][:, 0])
	cube[face][:, 0] = cube[face][:, 2]
	cube[face][:, 2] = aux
		 
def F(cube):
	rotate_face(cube, 0)
	aux = deepcopy(cube[1][2, :])
	cube[1][2, :] = cube[2][:, 2].T
	cube[2][:, 2] = cube[4][0, :].T
	cube[4][0, :] = cube[3][:, 0].T
	cube[3][:, 0] = aux.T
	
	aux = cube[1][2, 0]
	cube[1][2, 0] = cube[1][2, 2]
	cube[1][2, 2] = aux
	
	aux = cube[4][0, 0]
	cube[4][0, 0] = cube[4][0, 2]
	cube[4][0, 2] = aux

def F2(cube):
	F(cube)
	F(cube)
	
def Fp(cube):
	F2(cube)
	F(cube)

def U(cube):
	rotate_face(cube, 1)
	aux = deepcopy(cube[0][0, :])
	cube[0][0, :] = cube[3][0, :]
	cube[3][0, :] = cube[5][2, :]
	cube[5][2, :] = cube[2][0, :]
	cube[2][0, :] = aux
	
	aux = cube[3][0, 0]
	cube[3][0, 0] = cube[3][0, 2]
	cube[3][0, 2] = aux
	
	aux = cube[5][2, 0]
	cube[5][2, 0] = cube[5][2, 2]
	cube[5][2, 2] = aux

def U2(cube):
	U(cube)
	U(cube)
	
def Up(cube):
	U2(cube)
	U(cube)

def L(cube):
	rotate_face(cube, 2)
	aux = deepcopy(cube[0][:, 0])
	cube[0][:, 0] = cube[1][:, 0]
	cube[1][:, 0] = cube[5][:, 0]
	cube[5][:, 0] = cube[4][:, 0]
	cube[4][:, 0] = aux

def L2(cube):
	L(cube)
	L(cube)
	
def Lp(cube):
	L2(cube)
	L(cube)

def R(cube):
	rotate_face(cube, 3)
	aux = deepcopy(cube[0][:, 2])
	cube[0][:, 2] = cube[4][:, 2]
	cube[4][:, 2] = cube[5][:, 2]
	cube[5][:, 2] = cube[1][:, 2]
	cube[1][:, 2] = aux

def R2(cube):
	R(cube)
	R(cube)

def Rp(cube):
	R2(cube)
	R(cube)

def D(cube):
	rotate_face(cube, 4)
	aux = deepcopy(cube[0][2, :])
	cube[0][2, :] = np.fliplr(cube[2][2, :])
	cube[2][2, :] = np.fliplr(cube[5][0, :])
	cube[5][0, :] = np.fliplr(cube[3][2, :])
	cube[3][2, :] = np.fliplr(aux)
	
	aux = cube[0][2, 0]
	cube[0][2, 0] = cube[0][2, 2]
	cube[0][2, 2] = aux
	
	aux = cube[3][2, 0]
	cube[3][2, 0] = cube[3][2, 2]
	cube[3][2, 2] = aux

def D2(cube):
	D(cube)
	D(cube)
	
def Dp(cube):
	D2(cube)
	D(cube)

def B(cube):
	rotate_face(cube, 5)
	aux = deepcopy(cube[1][0, :])
	cube[1][0, :] = cube[3][:, 2].T
	cube[3][:, 2] = cube[4][2, :].T
	cube[4][2, :] = cube[2][:, 0].T
	cube[2][:, 0] = aux.T
	
	aux = cube[2][0, 0]
	cube[2][0, 0] = cube[2][2, 0]
	cube[2][2, 0] = aux
	
	aux = cube[3][0, 2]
	cube[3][0, 2] = cube[3][2, 2]
	cube[3][2, 2] = aux

def B2(cube):
	B(cube)
	B(cube)
	
def Bp(cube):
	B2(cube)
	B(cube)

def make_moves(cube, sequence):
	for move in sequence:
		eval(move + '(cube)')

def solved(cube):
	for face in cube:
		if (face != face[1, 1]).any():
			return False
			
	return True

def change_view(cube, front, top):
	if front == top:
		raise ValueError('Front color and top color must be different.')
	
	opposites = [[w, y], [o, r], [g, b], [b, r], [r, o], [y, w]]
	for pair in opposites:
		if front in pair and top in pair:
			raise ValueError(f'{front} and {top} are opposites layers.')
	
	order = []
	for face in cube:
		order.append(face[1, 1])
	
	# changing front layer
	if order[0] != front:
		if order[5] == front:
			aux = deepcopy(cube[0])
			cube[0] = cube[5]
			cube[5] = aux
		else:
			front_pos = order.index(front)
			aux = deepcopy(cube[front_pos])
			cube[front_pos] = cube[0]
			cube[0] = aux
			aux = deepcopy(cube[5 - front_pos])
			cube[5 - front_pos] = cube[5]
			cube[5] = aux

	order = []
	for face in cube:
		order.append(face[1, 1])
	
	# changing top layer
	if order[1] != top:
		if order[4] == top:
			aux = deepcopy(cube[1])
			cube[1] = cube[4]
			cube[4] = aux
		else:
			top_pos = order.index(top)
			aux = deepcopy(cube[top_pos])
			cube[top_pos] = cube[1]
			cube[1] = aux
			aux = deepcopy(cube[5 - top_pos])
			cube[5 - top_pos] = cube[4]
			cube[4] = aux
	
def print_cube(cube):
	line1 = ''
	line2 = ''
	line3 = ''
	line4 = ''
	line5 = ''
	line6 = ''
	line7 = ''
	line8 = ''
	for face in cube:
		center = face[1, 1]
		if center == cube[0][1, 1]:
			line1 += 'top:' + ' ' + cube[1][1, 1] + '  '
		elif center == cube[1][1, 1]:
			line1 += 'top:' + ' ' + cube[5][1, 1] + '  '
		elif center == cube[2][1, 1]:
			line1 += 'top:' + ' ' + cube[1][1, 1] + '  '
		elif center == cube[3][1, 1]:
			line1 += 'top:' + ' ' + cube[1][1, 1] + '  '
		elif center == cube[4][1, 1]:
			line1 += 'top:' + ' ' + cube[0][1, 1] + '  '
		elif center == cube[5][1, 1]:
			line1 += 'top:' + ' ' + cube[4][1, 1] + '  '
			
		line2 += luc + h + uc + h + uc + h + ruc + ' '
		line3 += v + face[0, 0] + v + face[0, 1] + v + face[0, 2] + v + ' '
		line4 += lc + h + c + h + c + h + rc + ' '
		line5 += v + face[1, 0] + v + face[1, 1] + v + face[1, 2] + v + ' '
		line6 += lc + h + c + h + c + h + rc + ' '
		line7 += v + face[2, 0] + v + face[2, 1] + v + face[2, 2] + v + ' '
		line8 += blc + h + bc + h + bc + h + brc + ' '
		
	print(line1)
	print(line2)
	print(line3)
	print(line4)
	print(line5)
	print(line6)
	print(line7)
	print(line8)

# fazer essa função
def solve(cube, depth = 0, seq = [], max_depth = 20):
	moves = [['F', 'F2', 'Fp'],
			 ['B', 'B2', 'Bp'],
			 ['R', 'R2', 'Rp'],
			 ['L', 'L2', 'Lp'],
			 ['U', 'U2', 'Up'],
			 ['D', 'D2', 'Dp']]
	
	for face in moves:
		for move in face:
			if seq != []:
				if move[0] != seq[-1][0]:
					new_cube = deepcopy(cube)
					make_moves(new_cube, seq + [move])
					if solved(new_cube):
						return seq + [move]
					elif depth < max_depth:
						sol = solve(cube, depth = depth + 1, seq = seq + [move], max_depth = max_depth)
						if sol != None:
							return sol
			else:
				new_cube = deepcopy(cube)
				make_moves(new_cube, seq + [move])
				if solved(new_cube):
					return seq + [move]
				else:
					sol = solve(cube, depth = depth + 1, seq = seq + [move], max_depth = max_depth)
					if sol != None:
						return sol
		 
sequence = ['Up', 'L2', 'D2', 'F2', 'R2', 'B2', 'R2', 'F2', 'D2', 'Lp', 'Up', 'Rp', 'B', 'Fp', 'Up']
sequence = ['U2', 'D2', 'L2', 'R2']#, 'F2', 'B2']
make_moves(cube, sequence)
print_cube(cube)
sol = solve(cube, depth = 0, seq = [], max_depth = 5)
make_moves(cube, sol)
print(sol)
print_cube(cube)

moves = [['F', 'F2', 'Fp'],
		 ['B', 'B2', 'Bp'],
		 ['R', 'R2', 'Rp'],
		 ['L', 'L2', 'Lp'],
		 ['U', 'U2', 'Up'],
		 ['D', 'D2', 'Dp']]
