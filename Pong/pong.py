import random
import pygame
import sys

pygame.init()

PRETO=(0, 0, 0)
BRANCO=(255, 255, 255)
LARGURA=800
ALTURA=600

tela=pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")

rodando=False
def menu_principal():
    global rodando
    while not rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    rodando = True
                    return

        tela.fill(PRETO)
        fonte = pygame.font.SysFont(None, 50)
        texto = fonte.render("Pong", True, BRANCO)
        rect = texto.get_rect(center=(LARGURA//2, ALTURA//2))
        tela.blit(texto, rect)

        font_blynk = pygame.font.SysFont(None, 26)
        tempo = pygame.time.get_ticks()
        if tempo % 2000 < 1000:
            texto_blynk = font_blynk.render("Pressione ESPACO para jogar", True, BRANCO)
            rect_blynk = texto_blynk.get_rect(center=(LARGURA//2, ALTURA//2 + 50))
            tela.blit(texto_blynk, rect_blynk)

        pygame.display.flip()

clock=pygame.time.Clock()

RAQUETE_LARGURA=10
RAQUETE_ALTURA=60
TAMANHO_BOLA=7

player1_x=15
player1_y=ALTURA//2 - RAQUETE_ALTURA//2

player2_x=LARGURA - 15 - RAQUETE_LARGURA
player2_y=ALTURA//2 - RAQUETE_ALTURA//2

bola_x=LARGURA//2 - TAMANHO_BOLA//2
bola_y=ALTURA//2 - TAMANHO_BOLA//2

velocidade_bola_x= random.choices([-5, 5])[0]
velocidade_bola_y= random.choices([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])[0]

score_player1 = 0
score_player2 = 0

menu_principal()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando=False

    tela.fill(PRETO)

    bola_x += velocidade_bola_x
    bola_y += velocidade_bola_y

    bola_rect = pygame.Rect(bola_x, bola_y, TAMANHO_BOLA, TAMANHO_BOLA)
    player1_rect = pygame.Rect(player1_x, player1_y, RAQUETE_LARGURA, RAQUETE_ALTURA)
    player2_rect = pygame.Rect(player2_x, player2_y, RAQUETE_LARGURA, RAQUETE_ALTURA)

    if bola_rect.colliderect(player1_rect) or bola_rect.colliderect(player2_rect):
        velocidade_bola_x = -velocidade_bola_x

    if bola_y <= 0 or bola_y >= ALTURA - TAMANHO_BOLA:
        velocidade_bola_y = -velocidade_bola_y

    if bola_x <= 0:
        score_player2 += 1
        bola_x = LARGURA//2 - TAMANHO_BOLA//2
        bola_y = ALTURA//2 - TAMANHO_BOLA//2
        velocidade_bola_x = -velocidade_bola_x
        velocidade_bola_y = random.choices([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])[0]
    
    if bola_x >= LARGURA - TAMANHO_BOLA:
        score_player1 += 1
        bola_x = LARGURA//2 - TAMANHO_BOLA//2
        bola_y = ALTURA//2 - TAMANHO_BOLA//2
        velocidade_bola_x = -velocidade_bola_x
        velocidade_bola_y = random.choices([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])[0]

    if player2_y + RAQUETE_ALTURA//2 < bola_y:
        player2_y += 5
    elif player2_y + RAQUETE_ALTURA//2 > bola_y:
        player2_y -= 5

    if player2_y < 0:
        player2_y = 0
    elif player2_y > ALTURA - RAQUETE_ALTURA:
        player2_y = ALTURA - RAQUETE_ALTURA

    pygame.draw.rect(tela, BRANCO, (player1_x, player1_y, RAQUETE_LARGURA, RAQUETE_ALTURA))
    pygame.draw.rect(tela, BRANCO, (player2_x, player2_y, RAQUETE_LARGURA, RAQUETE_ALTURA))
    pygame.draw.circle(tela, BRANCO, (bola_x, bola_y), TAMANHO_BOLA)

    font_score = pygame.font.SysFont(None, 36)
    score_text = font_score.render(f"{score_player1} - {score_player2}", True, BRANCO)
    tela.blit(score_text, score_text.get_rect(center=(LARGURA//2, 30)))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player1_y > 0:
        player1_y -= 5
    if keys[pygame.K_DOWN] and player1_y < ALTURA - RAQUETE_ALTURA:
        player1_y += 5

    pygame.display.flip()
    clock.tick(60)
