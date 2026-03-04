import pygame
import sys

pygame.init()

PRETO=(0, 0, 0)
BRANCO=(255, 255, 255)
LARGURA=800
ALTURA=600

tela=pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")

clock=pygame.time.Clock()

RAQUETE_LARGURA=10
RAQUETE_ALTURA=60
TAMANHO_BOLA=10

player1_x=15
player1_y=ALTURA//2 - RAQUETE_ALTURA//2

player2_x=LARGURA - 15 - RAQUETE_LARGURA
player2_y=ALTURA//2 - RAQUETE_ALTURA//2

bola_x=LARGURA//2 - TAMANHO_BOLA//2
bola_y=ALTURA//2 - TAMANHO_BOLA//2

rodando=True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando=False

    tela.fill(PRETO)

    pygame.draw.rect(tela, BRANCO, (player1_x, player1_y, RAQUETE_LARGURA, RAQUETE_ALTURA))
    pygame.draw.rect(tela, BRANCO, (player2_x, player2_y, RAQUETE_LARGURA, RAQUETE_ALTURA))
    pygame.draw.circle(tela, BRANCO, (bola_x, bola_y), TAMANHO_BOLA)

    pygame.display.flip()
    clock.tick(60)
