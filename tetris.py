import pygame
import random

pygame.font.init()

# Configurações da tela
largura_tela = 800
altura_tela = 700
largura_jogo = 300
altura_jogo = 600
bloco_tamanho = 30

janela_jogo_x = (largura_tela - largura_jogo) // 2
janela_jogo_y = altura_tela - altura_jogo - 50

# Formatos das peças (Tetriminos)
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# Lista de formas e cores
formas = [S, Z, I, O, J, L, T]
cores = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]

class Tetrimino:
    def __init__(self, x, y, forma):
        self.x = x
        self.y = y
        self.forma = forma
        self.cor = cores[formas.index(forma)]
        self.rotacao = 0

def criar_grade(travado={}):
    grade = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]
    
    for y in range(len(grade)):
        for x in range(len(grade[y])):
            if (x, y) in travado:
                cor = travado[(x, y)]
                grade[y][x] = cor
    return grade

def converter_forma(forma):
    posicoes = []
    formato = forma.forma[forma.rotacao % len(forma.forma)]

    for i, linha in enumerate(formato):
        linha = list(linha)
        for j, coluna in enumerate(linha):
            if coluna == '0':
                posicoes.append((forma.x + j, forma.y + i))

    for i, pos in enumerate(posicoes):
        posicoes[i] = (pos[0] - 2, pos[1] - 4)
    return posicoes

def espaco_valido(forma, grade):
    posicoes_aceitaveis = [[(j, i) for j in range(10) if grade[i][j] == (0, 0, 0)] for i in range(20)]
    posicoes_aceitaveis = [j for sub in posicoes_aceitaveis for j in sub]
    formatadas = converter_forma(forma)

    for pos in formatadas:
        if pos not in posicoes_aceitaveis:
            if pos[1] >= 0:
                return False
    return True

def linhas_completas(grade, travado):
    incrementador = 0
    for y in range(len(grade)-1, -1, -1):
        linha = grade[y]
        if (0, 0, 0) not in linha:
            incrementador += 1
            ind = y
            for x in range(len(linha)):
                try:
                    del travado[(x, y)]
                except:
                    continue
    if incrementador > 0:
        for chave in sorted(list(travado), key=lambda x: x[1])[::-1]:
            x, y = chave
            if y < ind:
                novaChave = (x, y + incrementador)
                travado[novaChave] = travado.pop(chave)
    return incrementador

def desenhar_texto_meio(texto, tamanho, cor, superficie):
    fonte = pygame.font.SysFont('comicsans', tamanho, bold=True)
    label = fonte.render(texto, 1, cor)
    superficie.blit(label, (janela_jogo_x + largura_jogo/2 - (label.get_width() / 2), janela_jogo_y + altura_jogo/2 - label.get_height()/2))

def desenhar_grade(surface, grade):
    for y in range(len(grade)):
        for x in range(len(grade[y])):
            pygame.draw.rect(surface, grade[y][x], (janela_jogo_x + x*bloco_tamanho, janela_jogo_y + y*bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

    for i in range(len(grade)):
        pygame.draw.line(surface, (128, 128, 128), (janela_jogo_x, janela_jogo_y + i * bloco_tamanho), (janela_jogo_x + largura_jogo, janela_jogo_y + i * bloco_tamanho))
        for j in range(len(grade[i])):
            pygame.draw.line(surface, (128, 128, 128), (janela_jogo_x + j * bloco_tamanho, janela_jogo_y), (janela_jogo_x + j * bloco_tamanho, janela_jogo_y + altura_jogo))

def desenhar_fenetre(surface, grade):
    surface.fill((0, 0, 0))
    pygame.font.init()
    fonte = pygame.font.SysFont('comicsans', 60)
    label = fonte.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, (janela_jogo_x + largura_jogo/2 - (label.get_width()/2), 30))

    #desenhar_grade(surface, grid) # Não precisa desenhar a grade aqui, já está em main

    for i in range(len(grade)):
        for j in range(len(grade[i])):
            pygame.draw.rect(surface, grade[i][j], (janela_jogo_x + j * bloco_tamanho, janela_jogo_y + i * bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

def desenhar_proxima_peca(surface, peca):
    fonte = pygame.font.SysFont('comicsans', 30)
    label = fonte.render('Próxima Peça:', 1, (255, 255, 255))

    sx = janela_jogo_x + largura_jogo + 50
    sy = janela_jogo_y + altura_jogo/2 - 100

    formato = peca.forma[peca.rotacao % len(peca.forma)]

    for i, linha in enumerate(formato):
        linha = list(linha)
        for j, coluna in enumerate(linha):
            if coluna == '0':
                pygame.draw.rect(surface, peca.cor, (sx + j*bloco_tamanho, sy + i*bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

    surface.blit(label, (sx, sy - 30))


def main():
    travado = {}
    grade = criar_grade(travado)

    muda_peca = False
    rodando = True
    corrente_peca = Tetrimino(5, 0, random.choice(formas))
    proxima_peca = Tetrimino(5, 0, random.choice(formas))
    relogio = pygame.time.Clock()
    queda_velocidade = 0.27
    queda_tempo = 0
    pontuacao = 0

    janela = pygame.display.set_mode((largura_tela, altura_tela))
    pygame.display.set_caption('Tetris')

    def redraw_janela(surface, grade, pontuacao=0):
        surface.fill((0, 0, 0))
        pygame.font.init()
        fonte = pygame.font.SysFont('comicsans', 60)
        label = fonte.render('TETRIS', 1, (255, 255, 255))

        surface.blit(label, (janela_jogo_x + largura_jogo/2 - (label.get_width()/2), 30))

        # Pontuação
        fonte = pygame.font.SysFont('comicsans', 30)
        label = fonte.render('Pontuação: ' + str(pontuacao), 1, (255,255,255))

        sx = janela_jogo_x + largura_jogo + 50
        sy = janela_jogo_y + altura_jogo/2 - 100

        surface.blit(label, (sx + 20, sy + 160))

        for i in range(len(grade)):
            for j in range(len(grade[i])):
                pygame.draw.rect(surface, grade[i][j], (janela_jogo_x + j * bloco_tamanho, janela_jogo_y + i * bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

        # Desenha a grade e a peça caindo
        desenhar_grade(surface, grade)

        if corrente_peca: #Garante que a peça existe antes de tentar converter
            for pos in converter_forma(corrente_peca):
                pygame.draw.rect(surface, corrente_peca.cor, (janela_jogo_x + pos[0]*bloco_tamanho, janela_jogo_y + pos[1]*bloco_tamanho, bloco_tamanho, bloco_tamanho), 0)

        # Desenha a próxima peça
        desenhar_proxima_peca(surface, proxima_peca)
        pygame.display.update()


    def perdeu(travado):
        for pos in travado:
            if pos[1] < 1:
                return True
        return False


    while rodando:
        grade = criar_grade(travado)
        queda_tempo += relogio.get_rawtime()
        relogio.tick()

        if queda_tempo/1000 > queda_velocidade:
            queda_tempo = 0
            corrente_peca.y += 1
            if not (espaco_valido(corrente_peca, grade)) and corrente_peca.y > 0:
                corrente_peca.y -= 1
                muda_peca = True

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.display.quit()
                quit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    corrente_peca.x -= 1
                    if not espaco_valido(corrente_peca, grade):
                        corrente_peca.x += 1
                if evento.key == pygame.K_RIGHT:
                    corrente_peca.x += 1
                    if not espaco_valido(corrente_peca, grade):
                        corrente_peca.x -= 1
                if evento.key == pygame.K_DOWN:
                    corrente_peca.y += 1
                    if not espaco_valido(corrente_peca, grade):
                        corrente_peca.y -= 1
                if evento.key == pygame.K_UP:
                    corrente_peca.rotacao += 1
                    if not espaco_valido(corrente_peca, grade):
                        corrente_peca.rotacao -= 1
        
        forma_pos = converter_forma(corrente_peca)

        for i in range(len(forma_pos)):
            x, y = forma_pos[i]
            if y > -1:
                grade[y][x] = corrente_peca.cor
        
        if muda_peca:
            for pos in forma_pos:
                p = (pos[0], pos[1])
                travado[p] = corrente_peca.cor
            corrente_peca = proxima_peca
            proxima_peca = Tetrimino(5, 0, random.choice(formas))
            muda_peca = False
            pontuacao += linhas_completas(grade, travado) * 100

        redraw_janela(janela, grade, pontuacao)

        if perdeu(travado):
            desenhar_texto_meio("Você Perdeu!", 80, (255,255,255), janela)
            pygame.display.update()
            pygame.time.delay(2000)
            rodando = False
            break



    pygame.quit()

if __name__ == '__main__':
    main()