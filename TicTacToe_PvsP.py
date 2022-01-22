import turtle

tela = turtle.Screen()
tela.setup(800, 800)
tela.title('Jogo da Velha')
tela.setworldcoordinates(-5, -5, 5, 5)
tela.bgcolor('light gray')
tela.tracer(0, 0)
turtle.hideturtle()

def desenhar_tabuleiro():
    turtle.pencolor('black')
    turtle.pensize(10)
    turtle.up()
    turtle.goto(-3, -1)
    turtle.seth(0)
    turtle.down()
    turtle.fd(6)
    turtle.up()
    turtle.goto(-3, 1)
    turtle.seth(0)
    turtle.down()
    turtle.fd(6)
    turtle.up()
    turtle.goto(-1, -3)
    turtle.seth(90)
    turtle.down()
    turtle.fd(6)
    turtle.up()
    turtle.goto(1, -3)
    turtle.seth(90)
    turtle.down()
    turtle.fd(6)

def desenhar_o(x, y):
    turtle.up()
    turtle.goto(x, y - 0.75)
    turtle.seth(0)
    turtle.color('blue')
    turtle.down()
    turtle.circle(0.75, steps = 100)

def desenhar_x(x,y):
    turtle.color('red')
    turtle.up()
    turtle.goto(x - 0.5, y - 0.75)
    turtle.down()
    turtle.goto(x + 0.5, y + 0.75)
    turtle.up()
    turtle.goto(x - 0.5, y + 0.75)
    turtle.down()
    turtle.goto(x + 0.5, y - 0.75)
    
def desenhar_jogada(i, j, letra):
    if letra == ' ': return
    x, y = 2 * (j - 1), -2 * (i - 1)
    if letra == 'X':
        desenhar_x(x, y)
    else:
        desenhar_o(x, y)
    
def desenhar(tabuleiro):
    desenhar_tabuleiro()
    for i in range(3):
        for j in range(3):
            desenhar_jogada(i, j, tabuleiro[i][j])
            
    tela.update()

def gameover(tabuleiro):
    if tabuleiro[0][0] != ' ' and tabuleiro[0][0] == tabuleiro[0][1] and tabuleiro[0][1] == tabuleiro[0][2]: return tabuleiro[0][0]
    if tabuleiro[1][0] != ' ' and tabuleiro[1][0] == tabuleiro[1][1] and tabuleiro[1][1] == tabuleiro[1][2]: return tabuleiro[1][0]
    if tabuleiro[2][0] != ' ' and tabuleiro[2][0] == tabuleiro[2][1] and tabuleiro[2][1] == tabuleiro[2][2]: return tabuleiro[2][0]
    if tabuleiro[0][0] != ' ' and tabuleiro[0][0] == tabuleiro[1][0] and tabuleiro[1][0] == tabuleiro[2][0]: return tabuleiro[0][0]
    if tabuleiro[0][1] != ' ' and tabuleiro[0][1] == tabuleiro[1][1] and tabuleiro[1][1] == tabuleiro[2][1]: return tabuleiro[0][1]
    if tabuleiro[0][2] != ' ' and tabuleiro[0][2] == tabuleiro[1][2] and tabuleiro[1][2] == tabuleiro[2][2]: return tabuleiro[0][2]
    if tabuleiro[0][0] != ' ' and tabuleiro[0][0] == tabuleiro[1][1] and tabuleiro[1][1] == tabuleiro[2][2]: return tabuleiro[0][0]
    if tabuleiro[2][0] != ' ' and tabuleiro[2][0] == tabuleiro[1][1] and tabuleiro[1][1] == tabuleiro[0][2]: return tabuleiro[2][0]
    casas_ocupadas = 0
    for i in range(3):
        for j in range(3):
            casas_ocupadas += (1 if tabuleiro[i][j] != ' ' else 0)
    if casas_ocupadas == 9: return 'Velha'
    else: return 0
    
def play(x, y):
    global vez, tabuleiro
    i = 3 - int(y + 5) // 2
    j = int(x + 5) // 2 - 1
    if i > 2 or j > 2 or i < 0 or j < 0 or tabuleiro[i][j] != ' ': return
    if vez == 'x': tabuleiro[i][j], vez = 'X', 'o'
    else: tabuleiro[i][j], vez = 'O', 'x'
    desenhar(tabuleiro)
    r = gameover(tabuleiro)
    if r == 'X':
        tela.textinput('Game over!', 'X ganhou!')
    elif r == 'O':
        tela.textinput('Game over!', 'O ganhou!')
    elif r == 'Velha':
        tela.textinput('Game over!', 'Deu Velha!')
	
    if r != 0:
    	tela.clear()
    	tela.bgcolor('light gray')
    	tela.tracer(0, 0)
    	turtle.hideturtle()
    	tabuleiro = [[' ' for i in range(3)] for j in range(3)]
    	desenhar(tabuleiro)
    	vez = 'x'
    	tela.onclick(play)
    	turtle.mainloop()
    
tabuleiro = [[' ' for i in range(3)] for j in range(3)]
desenhar(tabuleiro)
vez = 'x'
tela.onclick(play)
turtle.mainloop()
