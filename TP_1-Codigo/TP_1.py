import pygame
import math

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
LARGURA, ALTURA = 800, 600
MEIO_X, MEIO_Y = LARGURA // 2, ALTURA // 2

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Transformações Geométricas 2D e Rasterização')

# Listas para armazenar as formas desenhadas
pontos = []
linhas = []  # Cada linha é uma tupla: ((x0, y0), (x1, y1))
circunferencias = []  # Cada circunferência é uma tupla: (xc, yc, raio)

# Variável para armazenar a função selecionada
funcao_selecionada = None

# Variáveis para seleção de pontos
ponto_inicial = None
ponto_final = None
aguardando_ponto_final = False

# Fonte para textos
fonte = pygame.font.SysFont(None, 20)

# Função para desenhar os eixos cartesianos
def desenhar_eixos():
    # Limpa a tela
    tela.fill(PRETO)
    # Desenha o eixo X
    pygame.draw.line(tela, ROXO, (0, MEIO_Y), (LARGURA, MEIO_Y))
    # Desenha o eixo Y
    pygame.draw.line(tela, ROXO, (MEIO_X, 0), (MEIO_X, ALTURA))

# Função para converter coordenadas de tela para coordenadas do plano cartesiano
def tela_para_cartesiano(x, y):
    x_c = x - MEIO_X
    y_c = MEIO_Y - y
    return x_c, y_c

# Função para converter coordenadas do plano cartesiano para coordenadas de tela
def cartesiano_para_tela(x, y):
    x_t = x + MEIO_X
    y_t = MEIO_Y - y
    return x_t, y_t

# Função para plotar um pixel no plano cartesiano
def plotar_pixel(x, y, cor=BRANCO):
    x_t, y_t = cartesiano_para_tela(x, y)
    if 0 <= x_t < LARGURA and 0 <= y_t < ALTURA:
        tela.set_at((int(x_t), int(y_t)), cor)

# Funções para desenhar as formas armazenadas
def desenhar_pontos():
    for ponto in pontos:
        plotar_pixel(ponto[0], ponto[1])

def desenhar_linhas():
    for linha in linhas:
        x0, y0 = linha[0]
        x1, y1 = linha[1]
        linha_bresenham(x0, y0, x1, y1)

def desenhar_circunferencias():
    for circ in circunferencias:
        xc, yc, raio = circ
        circunferencia_bresenham(xc, yc, raio)

# Função para desenhar os botões
def desenhar_botoes():
    botoes = []
    opcoes = [
        'Plotar Pixel',
        'Linha DDA',
        'Linha Bresenham',
        'Circunferência',
        'Transladar',
        'Rotacionar',
        'Escalar',
        'Reflexão X',
        'Reflexão Y',
        'Reflexão XY'
    ]
    x, y = 10, 10
    largura_botao, altura_botao = 130, 30

    for opcao in opcoes:
        retangulo = pygame.Rect(x, y, largura_botao, altura_botao)
        pygame.draw.rect(tela, CINZA, retangulo)
        texto = fonte.render(opcao, True, PRETO)
        tela.blit(texto, (x + 5, y + 5))
        botoes.append((retangulo, opcao))
        y += altura_botao + 5

    return botoes

# Funções de transformação
def transladar_pontos(pontos, dx, dy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x + dx
        y_novo = y + dy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def transladar_linhas(linhas, dx, dy):
    novas_linhas = []
    for linha in linhas:
        (x0, y0), (x1, y1) = linha
        x0_novo = x0 + dx
        y0_novo = y0 + dy
        x1_novo = x1 + dx
        y1_novo = y1 + dy
        novas_linhas.append(((x0_novo, y0_novo), (x1_novo, y1_novo)))
    return novas_linhas

def transladar_circunferencias(circunferencias, dx, dy):
    novas_circunferencias = []
    for circ in circunferencias:
        xc, yc, raio = circ
        xc_novo = xc + dx
        yc_novo = yc + dy
        novas_circunferencias.append((xc_novo, yc_novo, raio))
    return novas_circunferencias

def rotacionar_pontos(pontos, angulo):
    novos_pontos = []
    rad = math.radians(angulo)
    cos_ang = math.cos(rad)
    sin_ang = math.sin(rad)
    for x, y in pontos:
        x_novo = x * cos_ang - y * sin_ang
        y_novo = x * sin_ang + y * cos_ang
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def rotacionar_linhas(linhas, angulo):
    novas_linhas = []
    rad = math.radians(angulo)
    cos_ang = math.cos(rad)
    sin_ang = math.sin(rad)
    for linha in linhas:
        (x0, y0), (x1, y1) = linha
        x0_novo = x0 * cos_ang - y0 * sin_ang
        y0_novo = x0 * sin_ang + y0 * cos_ang
        x1_novo = x1 * cos_ang - y1 * sin_ang
        y1_novo = x1 * sin_ang + y1 * cos_ang
        novas_linhas.append(((x0_novo, y0_novo), (x1_novo, y1_novo)))
    return novas_linhas

def rotacionar_circunferencias(circunferencias, angulo):
    novas_circunferencias = []
    rad = math.radians(angulo)
    cos_ang = math.cos(rad)
    sin_ang = math.sin(rad)
    for circ in circunferencias:
        xc, yc, raio = circ
        xc_novo = xc * cos_ang - yc * sin_ang
        yc_novo = xc * sin_ang + yc * cos_ang
        novas_circunferencias.append((xc_novo, yc_novo, raio))
    return novas_circunferencias

def escalar_pontos(pontos, sx, sy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x * sx
        y_novo = y * sy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def escalar_linhas(linhas, sx, sy):
    novas_linhas = []
    for linha in linhas:
        (x0, y0), (x1, y1) = linha
        x0_novo = x0 * sx
        y0_novo = y0 * sy
        x1_novo = x1 * sx
        y1_novo = y1 * sy
        novas_linhas.append(((x0_novo, y0_novo), (x1_novo, y1_novo)))
    return novas_linhas

def escalar_circunferencias(circunferencias, sx, sy):
    novas_circunferencias = []
    s_media = (sx + sy) / 2
    for circ in circunferencias:
        xc, yc, raio = circ
        xc_novo = xc * sx
        yc_novo = yc * sy
        raio_novo = raio * s_media
        novas_circunferencias.append((xc_novo, yc_novo, raio_novo))
    return novas_circunferencias

def refletir_pontos(pontos, eixo):
    novos_pontos = []
    for x, y in pontos:
        if eixo == 'x':
            novos_pontos.append((x, -y))
        elif eixo == 'y':
            novos_pontos.append((-x, y))
        elif eixo == 'xy':
            novos_pontos.append((-x, -y))
    return novos_pontos

def refletir_linhas(linhas, eixo):
    novas_linhas = []
    for linha in linhas:
        (x0, y0), (x1, y1) = linha
        if eixo == 'x':
            x0_novo, y0_novo = x0, -y0
            x1_novo, y1_novo = x1, -y1
        elif eixo == 'y':
            x0_novo, y0_novo = -x0, y0
            x1_novo, y1_novo = -x1, y1
        elif eixo == 'xy':
            x0_novo, y0_novo = -x0, -y0
            x1_novo, y1_novo = -x1, -y1
        novas_linhas.append(((x0_novo, y0_novo), (x1_novo, y1_novo)))
    return novas_linhas

def refletir_circunferencias(circunferencias, eixo):
    novas_circunferencias = []
    for circ in circunferencias:
        xc, yc, raio = circ
        if eixo == 'x':
            xc_novo, yc_novo = xc, -yc
        elif eixo == 'y':
            xc_novo, yc_novo = -xc, yc
        elif eixo == 'xy':
            xc_novo, yc_novo = -xc, -yc
        novas_circunferencias.append((xc_novo, yc_novo, raio))
    return novas_circunferencias

# Funções de rasterização
def linha_dda(x0, y0, x1, y1):
    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)
    dx = x1 - x0
    dy = y1 - y0
    passos = max(abs(dx), abs(dy))
    if passos == 0:
        plotar_pixel(x0, y0)
        return
    incremento_x = dx / passos
    incremento_y = dy / passos
    x, y = x0, y0
    for _ in range(passos + 1):
        plotar_pixel(round(x), round(y))
        x += incremento_x
        y += incremento_y

def linha_bresenham(x0, y0, x1, y1):
    x0, y0 = int(round(x0)), int(round(y0))
    x1, y1 = int(round(x1)), int(round(y1))
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    x, y = x0, y0
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    if dx >= dy:
        err = dx / 2.0
        while x != x1:
            plotar_pixel(x, y)
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
        plotar_pixel(x, y)
    else:
        err = dy / 2.0
        while y != y1:
            plotar_pixel(x, y)
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
        plotar_pixel(x, y)

def circunferencia_bresenham(xc, yc, raio):
    x = 0
    y = raio
    d = 3 - 2 * raio
    plotar_circunferencia_simetrica(xc, yc, x, y)
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        plotar_circunferencia_simetrica(xc, yc, x, y)

def plotar_circunferencia_simetrica(xc, yc, x, y):
    plotar_pixel(xc + x, yc + y)
    plotar_pixel(xc - x, yc + y)
    plotar_pixel(xc + x, yc - y)
    plotar_pixel(xc - x, yc - y)
    plotar_pixel(xc + y, yc + x)
    plotar_pixel(xc - y, yc + x)
    plotar_pixel(xc + y, yc - x)
    plotar_pixel(xc - y, yc - x)

# Função principal
def main():
    global pontos, linhas, circunferencias
    global funcao_selecionada, ponto_inicial, ponto_final, aguardando_ponto_final
    executando = True
    botoes = []

    while executando:
        desenhar_eixos()
        botoes = desenhar_botoes()
        desenhar_pontos()
        desenhar_linhas()
        desenhar_circunferencias()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                # Verifica se o clique foi em algum botão
                clicou_em_botao = False
                for retangulo, opcao in botoes:
                    if retangulo.collidepoint(posicao_mouse):
                        funcao_selecionada = opcao
                        ponto_inicial = None
                        ponto_final = None
                        aguardando_ponto_final = False
                        clicou_em_botao = True
                        break
                if not clicou_em_botao:
                    x_c, y_c = tela_para_cartesiano(*posicao_mouse)
                    if funcao_selecionada == 'Plotar Pixel':
                        pontos.append((x_c, y_c))
                    elif funcao_selecionada in ['Linha DDA', 'Linha Bresenham']:
                        if not ponto_inicial:
                            ponto_inicial = (x_c, y_c)
                            aguardando_ponto_final = True
                        elif aguardando_ponto_final:
                            ponto_final = (x_c, y_c)
                            linhas.append((ponto_inicial, ponto_final))
                            ponto_inicial = None
                            ponto_final = None
                            aguardando_ponto_final = False
                    elif funcao_selecionada == 'Circunferência':
                        if not ponto_inicial:
                            ponto_inicial = (x_c, y_c)
                            aguardando_ponto_final = True
                        elif aguardando_ponto_final:
                            ponto_final = (x_c, y_c)
                            raio = int(math.hypot(ponto_final[0] - ponto_inicial[0], ponto_final[1] - ponto_inicial[1]))
                            circunferencias.append((ponto_inicial[0], ponto_inicial[1], raio))
                            ponto_inicial = None
                            ponto_final = None
                            aguardando_ponto_final = False
                    elif funcao_selecionada == 'Transladar':
                        if not ponto_inicial:
                            # Seleciona o ponto inicial para calcular o vetor de translação
                            ponto_inicial = (x_c, y_c)
                            aguardando_ponto_final = True
                        elif aguardando_ponto_final:
                            # Calcula o vetor de translação e aplica às formas
                            ponto_final = (x_c, y_c)
                            dx = ponto_final[0] - ponto_inicial[0]
                            dy = ponto_final[1] - ponto_inicial[1]
                            pontos = transladar_pontos(pontos, dx, dy)
                            linhas = transladar_linhas(linhas, dx, dy)
                            circunferencias = transladar_circunferencias(circunferencias, dx, dy)
                            ponto_inicial = None
                            ponto_final = None
                            aguardando_ponto_final = False
                            funcao_selecionada = None
                    else:
                        # Se não estiver em modo de função específica, adiciona o ponto
                        pontos.append((x_c, y_c))
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    funcao_selecionada = None
                    ponto_inicial = None
                    ponto_final = None
                    aguardando_ponto_final = False

        # Aplicar transformações se selecionada
        if funcao_selecionada in ['Rotacionar', 'Escalar', 'Reflexão X', 'Reflexão Y', 'Reflexão XY']:
            if funcao_selecionada == 'Rotacionar':
                angulo = 45  # graus
                pontos = rotacionar_pontos(pontos, angulo)
                linhas = rotacionar_linhas(linhas, angulo)
                circunferencias = rotacionar_circunferencias(circunferencias, angulo)
                funcao_selecionada = None
            elif funcao_selecionada == 'Escalar':
                sx, sy = 1.5, 1.5
                pontos = escalar_pontos(pontos, sx, sy)
                linhas = escalar_linhas(linhas, sx, sy)
                circunferencias = escalar_circunferencias(circunferencias, sx, sy)
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão X':
                pontos = refletir_pontos(pontos, 'x')
                linhas = refletir_linhas(linhas, 'x')
                circunferencias = refletir_circunferencias(circunferencias, 'x')
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão Y':
                pontos = refletir_pontos(pontos, 'y')
                linhas = refletir_linhas(linhas, 'y')
                circunferencias = refletir_circunferencias(circunferencias, 'y')
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão XY':
                pontos = refletir_pontos(pontos, 'xy')
                linhas = refletir_linhas(linhas, 'xy')
                circunferencias = refletir_circunferencias(circunferencias, 'xy')
                funcao_selecionada = None

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
