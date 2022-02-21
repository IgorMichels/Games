import turtle
import random as rd
from copy import deepcopy

def jogar(tabuleiro, pos, jogador):
    x, y = pos
    tabuleiro[x][y] = jogador
    
    return tabuleiro

def verifica_posicoes_vagas(tabuleiro):
    posicoes_vagas = []
    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == ' ':
                posicoes_vagas.append((i, j))
                
    return posicoes_vagas

def computador_ingenuo(tabuleiro, simbolo):
    posicoes_vagas = verifica_posicoes_vagas(tabuleiro)
    posicao_escolhida = rd.choice(posicoes_vagas)
    return jogar(tabuleiro, posicao_escolhida, simbolo)

def computador_esperto(tabuleiro, jogador_da_vez, proximo_jogador):
    jogadas_permitidas = verifica_posicoes_vagas(tabuleiro)
    if len(jogadas_permitidas) == 9:
        # estamos na primeira jogada,
        # então vamos marcar um canto
        posicao_escolhida = rd.choice(jogadas_permitidas)
        return jogar(tabuleiro, posicao_escolhida, jogador_da_vez)
    elif len(jogadas_permitidas) == 8:
        # estamos na segunda jogada
        if tabuleiro[1][1] == ' ':
            # se o centro estiver livre,
            # jogamos lá
            return jogar(tabuleiro, (1, 1), jogador_da_vez)
        else:
            # se o jogador 1 jogou no centro
            # escolhemos um canto
            posicao_escolhida = (rd.choice([0, 2]), rd.choice([0, 2]))
            return jogar(tabuleiro, posicao_escolhida, jogador_da_vez)
    else:
        rd.shuffle(jogadas_permitidas)
        valor_comparativo = -100
        melhor_jogada = None
        for jogada in jogadas_permitidas:
            tabuleiro_auxiliar = deepcopy(tabuleiro)
            tabuleiro_auxiliar = jogar(tabuleiro_auxiliar, jogada, jogador_da_vez)
            if gameover(tabuleiro_auxiliar) == jogador_da_vez:
                # se dá para ganhar agora, ganhamos
                return jogar(tabuleiro, jogada, jogador_da_vez)

            # se não der, vamos buscar uma jogada que melhore a posição
            valor = minimax(False, tabuleiro_auxiliar, jogador_da_vez, proximo_jogador, 0)
            if valor > valor_comparativo:
                valor_comparativo = valor
                melhor_jogada = jogada

        return jogar(tabuleiro, melhor_jogada, jogador_da_vez)

def minimax(maximizar, tabuleiro, jogador_da_vez, proximo_jogador, profundidade):
    jogadas_permitidas = verifica_posicoes_vagas(tabuleiro)
    estado = gameover(tabuleiro)
    if estado != 0:
        if estado == 'Velha':
            return 0
        elif profundidade % 2 == 0:
            if jogador_da_vez in estado:
                return 1
            else:
                return -1
        else:
            if jogador_da_vez in estado:
                return -1
            else:
                return 1
    
    valores = []
    for jogada in jogadas_permitidas:
        tabuleiro_auxiliar = deepcopy(tabuleiro)
        tabuleiro_auxiliar = jogar(tabuleiro_auxiliar, jogada, proximo_jogador)
        valor = minimax(not maximizar, tabuleiro_auxiliar, proximo_jogador, jogador_da_vez, profundidade + 1)
        valores.append(valor)
        
    if maximizar:
        return max(valores)
    else:
        return min(valores)

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
    turtle.circle(0.75, steps = 1000)

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
    casas_livres = len(verifica_posicoes_vagas(tabuleiro))
    if casas_livres == 0: return 'Velha'
    else: return 0
    
def play(x, y):
    global vez, tabuleiro, jogar_contra_computador_esperto
    i = 3 - int(y + 5) // 2
    j = int(x + 5) // 2 - 1
    if i > 2 or j > 2 or i < 0 or j < 0 or tabuleiro[i][j] != ' ':
    	return
    	
    tabuleiro[i][j] = 'X'
    resultado = gameover(tabuleiro)
    if resultado == 0:
    	if jogar_contra_computador_esperto:
    		tabuleiro = computador_esperto(tabuleiro, 'O', 'X')
    	else:
    		tabuleiro = computador_ingenuo(tabuleiro, 'O')
    	
    desenhar(tabuleiro)
    resultado = gameover(tabuleiro)
    if resultado == 'X':
        tela.textinput('Game over!', 'X ganhou!')
    elif resultado == 'O':
        tela.textinput('Game over!', 'O ganhou!')
    elif resultado == 'Velha':
        tela.textinput('Game over!', 'Deu Velha!')
	
    if resultado != 0:
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
jogar_contra_computador_esperto = True
tela.onclick(play)
turtle.mainloop()
