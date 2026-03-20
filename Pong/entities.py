import random
import pygame

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
WIDTH=800
HEIGHT=600
RACKET_WIDTH=10
RACKET_HEIGHT=60
BALL_SIZE=7

class Player:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 5
        self.score = 0

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

class Ball:
    def __init__(self, x, y, size):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = 0
        self.speed_y = 0
        self.reset()

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.x = WIDTH//2 - self.size//2
        self.rect.y = HEIGHT//2 - self.size//2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

    def draw(self, screen, color):
        pygame.draw.circle(screen, color, self.rect.center, self.size)

class KeyboardController:
    def update(self, player):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()

class CpuController:
    def update(self, player, ball):
        if player.rect.centery < ball.rect.centery:
            player.move_down()
        elif player.rect.centery > ball.rect.centery:
            player.move_up()

class PhysicsManager:
    def handle_collisions(self, ball, player1, player2):
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.speed_x *= -1

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.size:
            ball.speed_y *= -1
    
class ScoreManager:
    def check_scoring(self, ball, player1, player2):
        if ball.rect.x <= 0:
            player2.score += 1
            ball.reset()
        if ball.rect.x >= WIDTH - ball.size:
            player1.score += 1
            ball.reset()