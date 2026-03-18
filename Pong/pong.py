import random
import pygame
import sys

pygame.init()

BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
WIDTH=800
HEIGHT=600
RACKET_WIDTH=10
RACKET_HEIGHT=60
BALL_SIZE=7

screen=pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = 5
        self.score = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move_up(self):
        if self.rect.y > 0:
            self.rect.y -= self.speed

    def move_down(self):
        if self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed

    def drawRect(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

class Ball:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.x = WIDTH//2 - self.size//2
        self.rect.y = HEIGHT//2 - self.size//2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

    def drawCircle(self, screen, color):
        pygame.draw.circle(screen, color, self.rect.center, self.size)

class InputController:
    def handle(self, player):
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

class CollisionManager:
    def handle_ball_collision(self, ball, player1, player2):
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.speed_x *= -1

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.size:
            ball.speed_y *= -1

    def handle_score(self, ball, player1, player2):
        if ball.rect.x <= 0:
            player2.score += 1
            ball.reset()

        if ball.rect.x >= WIDTH - ball.size:
            player1.score += 1
            ball.reset()

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True

        self.title_font = pygame.font.SysFont(None, 50)
        self.option_font = pygame.font.SysFont(None, 26)

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.running = False

    def draw(self):
        self.screen.fill(BLACK)

        texto = self.title_font.render("Pong", True, WHITE)
        rect = texto.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(texto, rect)

        tempo = pygame.time.get_ticks()
        if tempo % 2000 < 1000:
            texto_blynk = self.option_font.render("Pressione ESPAÇO para jogar", True, WHITE)
            rect_blynk = texto_blynk.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            self.screen.blit(texto_blynk, rect_blynk)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()

        return True

class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.running = True

        self.player1 = Player(15, HEIGHT//2 - RACKET_HEIGHT//2, RACKET_WIDTH, RACKET_HEIGHT)
        self.player2 = Player(WIDTH - 15 - RACKET_WIDTH, HEIGHT//2 - RACKET_HEIGHT//2, RACKET_WIDTH, RACKET_HEIGHT)
        self.ball = Ball(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE)

        self.input_controller = InputController()
        self.cpu_controller = CpuController()
        self.collision_manager = CollisionManager()

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False

    def update(self):
        self.ball.move()

        self.input_controller.handle(self.player1)
        self.cpu_controller.update(self.player2, self.ball)

        self.collision_manager.handle_ball_collision(
            self.ball, self.player1, self.player2
        )

        self.collision_manager.handle_score(
            self.ball, self.player1, self.player2
        )

    def draw(self, screen):
        screen.fill(BLACK)

        self.player1.drawRect(screen, WHITE)
        self.player2.drawRect(screen, WHITE)
        self.ball.drawCircle(screen, WHITE)

        font_score = pygame.font.SysFont(None, 36)
        score_text = font_score.render(
            f"{self.player1.score} - {self.player2.score}", True, WHITE
        )
        screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, 30)))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw(screen)
            self.clock.tick(60)

            if self.player1.score >= 10 or self.player2.score >= 10:
                self.running = False

def main():
    while True:
        menu = Menu(screen)
        if not menu.run():
            break

        game = Game()
        game.run()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()