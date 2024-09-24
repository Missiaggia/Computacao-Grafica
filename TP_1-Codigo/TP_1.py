import pygame
import math

# Inicialização do Pygame
pygame.init()

# Dimensões da janela (largura e altura)
LARGURA, ALTURA = 1600, 900
MEIO_X, MEIO_Y = LARGURA // 2, ALTURA // 2  # Coordenadas do centro da tela

# Definição de cores (RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)
AZUL = (173, 216, 230)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)

# Configuração da janela do Pygame
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('TP_1 - CG')

# Listas para armazenar as formas desenhadas
pontos = []           # Lista de pontos definidos por: (x0, y0)
linhas_bres = []      # Lista de linhas definidas por: ((x0, y0), (x1, y1))
linhas_DDA = []      # Lista de linhas definidas por: ((x0, y0), (x1, y1))
circunferencias = []  # Lista de circunferências definidas por: (xc, yc, raio)

# Variável para armazenar a função selecionada pelo usuário
funcao_selecionada = None

# Variáveis para seleção de pontos durante a interação com o usuário
ponto_inicial = None
ponto_final = None
aguardando_ponto_final = False

# Fonte para textos (usada nos botões)
fonte = pygame.font.SysFont(None, 20)

# Função para desenhar os eixos cartesianos na tela
def desenhar_eixos():
    # Limpa a tela com a cor preta
    tela.fill(PRETO)
    # Desenha o eixo X (horizontal) em roxo
    pygame.draw.line(tela, ROXO, (0, MEIO_Y), (LARGURA, MEIO_Y))
    # Desenha o eixo Y (vertical) em roxo
    pygame.draw.line(tela, ROXO, (MEIO_X, 0), (MEIO_X, ALTURA))

# Função para converter coordenadas de tela para coordenadas do plano cartesiano
def tela_para_cartesiano(x, y):
    x_c = x - MEIO_X      # Ajusta o ponto x em relação ao centro da tela
    y_c = MEIO_Y - y      # Inverte o eixo Y e ajusta em relação ao centro
    return x_c, y_c

# Função para converter coordenadas do plano cartesiano para coordenadas de tela
def cartesiano_para_tela(x, y):
    x_t = x + MEIO_X      # Ajusta o ponto x para a posição na tela
    y_t = MEIO_Y - y      # Inverte o eixo Y e ajusta para a posição na tela
    return x_t, y_t

# Função para plotar um pixel no plano cartesiano
def plotar_pixel(x, y, cor=BRANCO):
    x_t, y_t = cartesiano_para_tela(x, y)
    # Verifica se o pixel está dentro dos limites da tela
    if 0 <= x_t < LARGURA and 0 <= y_t < ALTURA:
        tela.set_at((int(x_t), int(y_t)), cor)

# Função para desenhar todos os pontos armazenados
def desenhar_pontos():
    for ponto in pontos:
        plotar_pixel(ponto[0], ponto[1])

# Função para desenhar todas as linhas armazenadas
def desenhar_linhas_bres():
    for linha in linhas_bres:
        x0, y0 = linha[0]
        x1, y1 = linha[1]
        linha_bresenham(x0, y0, x1, y1)

def desenhar_linhas_DDA():
    for linha in linhas_DDA:
        x0, y0 = linha[0]
        x1, y1 = linha[1]
        linha_dda(x0, y0, x1, y1)

# Função para desenhar todas as circunferências armazenadas
def desenhar_circunferencias():
    for circ in circunferencias:
        xc, yc, raio = circ
        circunferencia_bresenham(xc, yc, raio)

# Função para desenhar os botões de opções na tela
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
    x, y = 10, 10  # Posição inicial dos botões
    largura_botao, altura_botao = 130, 30  # Tamanho dos botões

    for opcao in opcoes:
        retangulo = pygame.Rect(x, y, largura_botao, altura_botao)
        # Desenha o retângulo do botão
        pygame.draw.rect(tela, CINZA, retangulo)
        # Renderiza o texto da opção
        texto = fonte.render(opcao, True, PRETO)
        # Desenha o texto no botão
        tela.blit(texto, (x + 5, y + 5))
        # Adiciona o botão à lista de botões para detecção de clique
        botoes.append((retangulo, opcao))
        y += altura_botao + 5  # Atualiza a posição Y para o próximo botão

    return botoes

# Funções de transformação geométrica

# Translação de pontos
def transladar_pontos(pontos, dx, dy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x + dx
        y_novo = y + dy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

# Translação de linhas
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

# Translação de circunferências
def transladar_circunferencias(circunferencias, dx, dy):
    novas_circunferencias = []
    for circ in circunferencias:
        xc, yc, raio = circ
        xc_novo = xc + dx
        yc_novo = yc + dy
        novas_circunferencias.append((xc_novo, yc_novo, raio))
    return novas_circunferencias

# Rotação de pontos em torno da origem
def rotacionar_pontos(pontos, angulo):
    novos_pontos = []
    rad = math.radians(angulo)  # Converte o ângulo para radianos
    cos_ang = math.cos(rad)
    sin_ang = math.sin(rad)
    for x, y in pontos:
        x_novo = x * cos_ang - y * sin_ang
        y_novo = x * sin_ang + y * cos_ang
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

# Rotação de linhas em torno da origem
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

# Rotação de circunferências em torno da origem
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

# Escala de pontos em relação à origem
def escalar_pontos(pontos, sx, sy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x * sx
        y_novo = y * sy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

# Escala de linhas em relação à origem
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

# Escala de circunferências em relação à origem
def escalar_circunferencias(circunferencias, sx, sy):
    novas_circunferencias = []
    s_media = (sx + sy) / 2  # Calcula a média dos fatores de escala para o raio
    for circ in circunferencias:
        xc, yc, raio = circ
        xc_novo = xc * sx
        yc_novo = yc * sy
        raio_novo = raio * s_media
        novas_circunferencias.append((xc_novo, yc_novo, raio_novo))
    return novas_circunferencias

# Reflexão de pontos em relação aos eixos
def refletir_pontos(pontos, eixo):
    novos_pontos = []
    for x, y in pontos:
        if eixo == 'x':
            novos_pontos.append((x, -y))    # Reflexão no eixo X
        elif eixo == 'y':
            novos_pontos.append((-x, y))    # Reflexão no eixo Y
        elif eixo == 'xy':
            novos_pontos.append((-x, -y))   # Reflexão nos eixos X e Y
    return novos_pontos

# Reflexão de linhas em relação aos eixos
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

# Reflexão de circunferências em relação aos eixos
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

# Funções de rasterização (desenho de formas)

# Desenho de linhas usando o algoritmo DDA
def linha_dda(x0, y0, x1, y1):
    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)
    dx = x1 - x0
    dy = y1 - y0
    passos = max(abs(dx), abs(dy))  # Determina o número de passos necessários
    if passos == 0:
        plotar_pixel(x0, y0)
        return
    incremento_x = dx / passos      # Incremento em x a cada passo
    incremento_y = dy / passos      # Incremento em y a cada passo
    x, y = x0, y0
    for _ in range(passos + 1):
        plotar_pixel(round(x), round(y))
        x += incremento_x
        y += incremento_y

# Desenho de linhas usando o algoritmo de Bresenham
def linha_bresenham(x0, y0, x1, y1):
    x0, y0 = int(x0), int(y0)
    x1, y1 = int(x1), int(y1)
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    if dx > 0:
        xincr = 1
    else:
        xincr = -1
        dx = -dx
    if dy > 0:
        yincr = 1
    else:
        yincr = -1
        dy = -dy
    plotar_pixel(x, y)
    if dx > dy:
        p = 2 * dy - dx
        c1 = 2 * dy
        c2 = 2 * (dy - dx)
        for _ in range(dx):
            x += xincr
            if(p < 0):
                p += c1
            else:
                p += c2
                y += yincr
            plotar_pixel(x, y)
    else:
        p = 2 * dx - dy
        c1 = 2 * dx
        c2 = 2 * (dx - dy)
        for _ in range(dy):
            y += yincr
            if(p < 0):
                p += c1
            else:
                p += c2
                x += xincr
            plotar_pixel(x, y)

# Desenho de circunferências usando o algoritmo de Bresenham
def circunferencia_bresenham(xc, yc, raio):
    x = 0
    y = raio
    d = 3 - 2 * raio  # Valor inicial do parâmetro de decisão
    plotar_circunferencia_simetrica(xc, yc, x, y)
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        plotar_circunferencia_simetrica(xc, yc, x, y)

# Função auxiliar para plotar os pontos simétricos da circunferência
def plotar_circunferencia_simetrica(xc, yc, x, y):
    plotar_pixel(xc + x, yc + y)
    plotar_pixel(xc - x, yc + y)
    plotar_pixel(xc + x, yc - y)
    plotar_pixel(xc - x, yc - y)
    plotar_pixel(xc + y, yc + x)
    plotar_pixel(xc - y, yc + x)
    plotar_pixel(xc + y, yc - x)
    plotar_pixel(xc - y, yc - x)

# Função principal do programa
def main():
    global pontos, linhas_bres,linhas_DDA, circunferencias
    global funcao_selecionada, ponto_inicial, ponto_final, aguardando_ponto_final
    executando = True
    botoes = []
    isBres = False
    isDDA = False

    while executando:
        desenhar_eixos()               # Desenha os eixos cartesianos
        botoes = desenhar_botoes()     # Desenha os botões e atualiza a lista de botões
        desenhar_pontos()              # Desenha os pontos armazenados
        desenhar_linhas_bres()              # Desenha as linhas armazenadas
        desenhar_linhas_DDA()              # Desenha as linhas armazenadas
        desenhar_circunferencias()     # Desenha as circunferências armazenadas

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False     # Sai do loop principal e encerra o programa
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
                        pontos.append((x_c, y_c))  # Adiciona o ponto à lista de pontos
                    elif funcao_selecionada in ['Linha DDA', 'Linha Bresenham']:
                        if not ponto_inicial:
                            if funcao_selecionada == 'Linha Bresenham':
                                isBres = True
                            if funcao_selecionada == 'Linha DDA':
                                isDDA = True
                            # Seleciona o primeiro ponto da linha
                            ponto_inicial = (x_c, y_c)
                            aguardando_ponto_final = True
                        elif aguardando_ponto_final:
                            # Seleciona o segundo ponto da linha e adiciona à lista
                            ponto_final = (x_c, y_c)
                            if isBres:
                                linhas_bres.append((ponto_inicial, ponto_final))
                            if isDDA:
                                linhas_DDA.append((ponto_inicial, ponto_final))
                            ponto_inicial = None
                            ponto_final = None
                            aguardando_ponto_final = False
                            isBres = False
                            isDDA = False
                    elif funcao_selecionada == 'Circunferência':
                        if not ponto_inicial:
                            # Seleciona o centro da circunferência
                            ponto_inicial = (x_c, y_c)
                            aguardando_ponto_final = True
                        elif aguardando_ponto_final:
                            # Seleciona um ponto para definir o raio e adiciona à lista
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
                            linhas_bres = transladar_linhas(linhas_bres, dx, dy)
                            linhas_DDA = transladar_linhas(linhas_DDA, dx, dy)
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
                    # Reseta a função selecionada e pontos intermediários
                    funcao_selecionada = None
                    ponto_inicial = None
                    ponto_final = None
                    aguardando_ponto_final = False

        # Aplicar transformações se alguma foi selecionada
        if funcao_selecionada in ['Rotacionar', 'Escalar', 'Reflexão X', 'Reflexão Y', 'Reflexão XY']:
            if funcao_selecionada == 'Rotacionar':
                angulo = 45  # Ângulo em graus para rotacionar
                pontos = rotacionar_pontos(pontos, angulo)
                linhas_bres = rotacionar_linhas(linhas_bres, angulo)
                linhas_DDA = rotacionar_linhas(linhas_DDA, angulo)
                circunferencias = rotacionar_circunferencias(circunferencias, angulo)
                funcao_selecionada = None
            elif funcao_selecionada == 'Escalar':
                sx, sy = 1.5, 1.5  # Fatores de escala em x e y
                pontos = escalar_pontos(pontos, sx, sy)
                linhas_bres = escalar_linhas(linhas_bres, sx, sy)
                linhas_DDA = escalar_linhas(linhas_DDA, sx, sy)
                circunferencias = escalar_circunferencias(circunferencias, sx, sy)
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão X':
                pontos = refletir_pontos(pontos, 'x')
                linhas_bres = refletir_linhas(linhas_bres, 'x')
                linhas_DDA = refletir_linhas(linhas_DDA, 'x')
                circunferencias = refletir_circunferencias(circunferencias, 'x')
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão Y':
                pontos = refletir_pontos(pontos, 'y')
                linhas_bres = refletir_linhas(linhas_bres, 'y')
                linhas_DDA = refletir_linhas(linhas_DDA, 'y')
                circunferencias = refletir_circunferencias(circunferencias, 'y')
                funcao_selecionada = None
            elif funcao_selecionada == 'Reflexão XY':
                pontos = refletir_pontos(pontos, 'xy')
                linhas_bres = refletir_linhas(linhas_bres, 'xy')
                linhas_DDA = refletir_linhas(linhas_DDA, 'xy')
                circunferencias = refletir_circunferencias(circunferencias, 'xy')
                funcao_selecionada = None

        # Atualiza a tela do Pygame
        pygame.display.flip()

    # Encerra o Pygame ao sair do loop principal
    pygame.quit()

# Chama a função principal para iniciar o programa
if __name__ == '__main__':
    main()
