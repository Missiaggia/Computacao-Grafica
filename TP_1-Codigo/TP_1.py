import pygame
import math

# Inicialização do Pygame
pygame.init()

# Dimensões da janela
LARGURA, ALTURA = 1200, 800
MEIO_X, MEIO_Y = LARGURA // 2, ALTURA // 2

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
ROXO = (128, 0, 128)
CINZA = (200, 200, 200)
AZUL_CLARO = (173, 216, 230)
VERMELHO = (255, 0, 0)

# Configuração da janela
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption('Transformações Geométricas 2D')

# Lista para armazenar pontos desenhados
pontos = []

# Variável para armazenar a transformação selecionada
transformacao_selecionada = None

# Variáveis para seleção de ponto na translação
ponto_selecionado = None
aguardando_novo_ponto = False

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

# Função para desenhar os pontos armazenados
def desenhar_pontos():
    for ponto in pontos:
        cor = BRANCO
        if ponto == ponto_selecionado:
            cor = VERMELHO  # Destaca o ponto selecionado
        plotar_pixel(ponto[0], ponto[1], cor)

# Função para desenhar os botões de transformação
def desenhar_botoes():
    botoes = []
    opcoes = [
        'Transladar',
        'Rotacionar',
        'Escalar',
        'Reflexão X',
        'Reflexão Y',
        'Reflexão XY'
    ]
    x, y = 10, 10
    largura_botao, altura_botao = 100, 30

    for opcao in opcoes:
        retangulo = pygame.Rect(x, y, largura_botao, altura_botao)
        pygame.draw.rect(tela, CINZA, retangulo)
        texto = fonte.render(opcao, True, PRETO)
        tela.blit(texto, (x + 5, y + 5))
        botoes.append((retangulo, opcao))
        y += altura_botao + 5

    return botoes

# Funções de transformação sem NumPy
def transladar(pontos, dx, dy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x + dx
        y_novo = y + dy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def rotacionar(pontos, angulo):
    rad = math.radians(angulo)
    cos_ang = math.cos(rad)
    sin_ang = math.sin(rad)
    novos_pontos = []
    for x, y in pontos:
        x_novo = x * cos_ang - y * sin_ang
        y_novo = x * sin_ang + y * cos_ang
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def escalar(pontos, sx, sy):
    novos_pontos = []
    for x, y in pontos:
        x_novo = x * sx
        y_novo = y * sy
        novos_pontos.append((x_novo, y_novo))
    return novos_pontos

def refletir(pontos, eixo):
    novos_pontos = []
    for x, y in pontos:
        if eixo == 'x':
            novos_pontos.append((x, -y))
        elif eixo == 'y':
            novos_pontos.append((-x, y))
        elif eixo == 'xy':
            novos_pontos.append((-x, -y))
    return novos_pontos

# Função principal
def main():
    global pontos, transformacao_selecionada, ponto_selecionado, aguardando_novo_ponto
    executando = True
    botoes = []

    while executando:
        desenhar_eixos()
        botoes = desenhar_botoes()
        desenhar_pontos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                posicao_mouse = pygame.mouse.get_pos()
                # Verifica se o clique foi em algum botão
                clicou_em_botao = False
                for retangulo, opcao in botoes:
                    if retangulo.collidepoint(posicao_mouse):
                        transformacao_selecionada = opcao
                        ponto_selecionado = None
                        aguardando_novo_ponto = False
                        clicou_em_botao = True
                        break
                if not clicou_em_botao:
                    x_c, y_c = tela_para_cartesiano(*posicao_mouse)
                    if transformacao_selecionada == 'Transladar':
                        if not ponto_selecionado:
                            # Seleciona o ponto mais próximo ao clique
                            ponto_selecionado = selecionar_ponto_proximo((x_c, y_c))
                            if ponto_selecionado:
                                aguardando_novo_ponto = True
                        elif aguardando_novo_ponto:
                            # Calcula o vetor de translação
                            dx = x_c - ponto_selecionado[0]
                            dy = y_c - ponto_selecionado[1]
                            pontos = transladar(pontos, dx, dy)
                            ponto_selecionado = None
                            aguardando_novo_ponto = False
                            transformacao_selecionada = None
                    else:
                        # Se não estiver em modo de transformação, adiciona o ponto
                        pontos.append((x_c, y_c))
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    transformacao_selecionada = None
                    ponto_selecionado = None
                    aguardando_novo_ponto = False

        # Aplicar outras transformações se selecionada
        if transformacao_selecionada and transformacao_selecionada != 'Transladar':
            if transformacao_selecionada == 'Rotacionar':
                # Exemplo de rotação com ângulo fixo
                angulo = 30  # graus
                pontos = rotacionar(pontos, angulo)
                transformacao_selecionada = None
            elif transformacao_selecionada == 'Escalar':
                # Exemplo de escala com fator fixo
                sx, sy = 1.5, 1.5
                pontos = escalar(pontos, sx, sy)
                transformacao_selecionada = None
            elif transformacao_selecionada == 'Reflexão X':
                pontos = refletir(pontos, 'x')
                transformacao_selecionada = None
            elif transformacao_selecionada == 'Reflexão Y':
                pontos = refletir(pontos, 'y')
                transformacao_selecionada = None
            elif transformacao_selecionada == 'Reflexão XY':
                pontos = refletir(pontos, 'xy')
                transformacao_selecionada = None

        pygame.display.flip()

    pygame.quit()

# Função para selecionar o ponto mais próximo ao clique
def selecionar_ponto_proximo(posicao, raio=5):
    x_click, y_click = posicao
    for ponto in pontos:
        distancia = math.hypot(ponto[0] - x_click, ponto[1] - y_click)
        if distancia <= raio:
            return ponto
    return None

if __name__ == '__main__':
    main()
