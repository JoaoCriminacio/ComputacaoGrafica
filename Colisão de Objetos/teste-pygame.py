import pygame
import sys
import random

pygame.init()

PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
LARGURA = 800
ALTURA = 600
TAMANHO_FONTE = 50
FPS = 512

TEXTO_STR = 'GEROMEL'
TEXTO2_STR = 'KANNEMMAN'

def gerar_velocidade():
    while True:
        vx = random.randint(-1, 1)
        vy = random.randint(-1, 1)
        if vx != 0 or vy != 0:
            return vx, vy
        
def cor_aleatoria():
    return (
        random.randint(1, 255),
        random.randint(1, 255),
        random.randint(1, 255),
    )

def criar_texto(fonte, texto_str, cor, posicao):
    texto = fonte.render(texto_str, True, cor)
    rect = texto.get_rect(center=posicao)
    return texto, rect

def atualizar_colisao_borda(rect, vx, vy, fonte, texto_str):
    mudou = False

    if rect.right >= LARGURA:
        vx = random.randint(-1, 0)
        vy = random.randint(-1, 1)
        mudou = True

    if rect.left <= 0:
        vx = random.randint(0, 1)
        vy = random.randint(-1, 1)
        mudou = True

    if rect.bottom >= ALTURA:
        vx = random.randint(-1, 1)
        vy = random.randint(-1, 0)
        mudou = True

    if rect.top <= 0:
        vx = random.randint(-1, 1)
        vy = random.randint(0, 1)
        mudou = True

    if mudou:
        texto = fonte.render(texto_str, True, cor_aleatoria())
        return vx, vy, texto

    return vx, vy, None

def main():
    pygame.init()

    tela = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Janela")

    clock = pygame.time.Clock()
    fonte = pygame.font.SysFont(None, TAMANHO_FONTE)

    texto1, rect1 = criar_texto(fonte, TEXTO_STR, BRANCO, (200, 300))
    vx1, vy1 = gerar_velocidade()

    texto2, rect2 = criar_texto(fonte, TEXTO2_STR, BRANCO, (600, 300))
    vx2, vy2 = gerar_velocidade()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        tela.fill(PRETO)

        rect1.x += vx1
        rect1.y += vy1
        rect2.x += vx2
        rect2.y += vy2

        vx1, vy1, novo_texto1 = atualizar_colisao_borda(rect1, vx1, vy1, fonte, TEXTO_STR)
        vx2, vy2, novo_texto2 = atualizar_colisao_borda(rect2, vx2, vy2, fonte, TEXTO2_STR)

        if novo_texto1:
            texto1 = novo_texto1
        if novo_texto2:
            texto2 = novo_texto2

        if rect1.colliderect(rect2):
            vx1, vx2 = vx2, vx1
            vy1, vy2 = vy2, vy1

            texto1 = fonte.render(TEXTO_STR, True, cor_aleatoria())
            texto2 = fonte.render(TEXTO2_STR, True, cor_aleatoria())

        tela.blit(texto1, rect1)
        tela.blit(texto2, rect2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

main()