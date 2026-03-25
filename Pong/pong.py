import pygame
import sys
from entities import (
    Player, Ball, BallFactory, MultiplicationManager,
    KeyboardController, CpuController, PhysicsManager, ScoreManager,
    WIDTH, HEIGHT, BLACK, WHITE, RACKET_WIDTH, RACKET_HEIGHT, BALL_SIZE
)

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

class Game:
    def __init__(self, screen, player1, player2, ball, ctrl_player1, ctrl_player2, ctrl_physics, ctrl_score):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.player1 = player1
        self.player2 = player2
        self.balls: list[Ball] = [ball] 
        self.ctrl_player1 = ctrl_player1
        self.ctrl_player2 = ctrl_player2
        self.physics = ctrl_physics
        self.score = ctrl_score
        self.font_score = pygame.font.SysFont(None, 36)

    def _real_ball(self):
        for b in self.balls:
            if b.is_real:
                return b
        return self.balls[0] if self.balls else None

    def handle_events(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def update(self):
        for ball in self.balls:
            ball.move()

        self.ctrl_player1.update(self.player1)
        real = self._real_ball()
        if real:
            self.ctrl_player2.update(self.player2, real)

        new_decoys: list[Ball] = []

        for ball in self.balls:
            decoys = self.physics.handle_collisions(ball, self.player1, self.player2)

            if decoys:
                new_decoys.extend(decoys)

        self.balls.extend(new_decoys)

        self.balls = self.score.check_scoring(self.balls, self.player1, self.player2)

        if self.player1.score >= 10 or self.player2.score >= 10:
            self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.player1.draw(self.screen, WHITE)
        self.player2.draw(self.screen, WHITE)

        for ball in self.balls:
            ball.draw(self.screen)

        score_text = self.font_score.render(
            f"{self.player1.score} - {self.player2.score}", True, WHITE
        )
        self.screen.blit(score_text, score_text.get_rect(center=(WIDTH//2, 30)))
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    while True:
        menu = Menu(screen)
        menu.run()

        player1 = Player(15, HEIGHT//2 - RACKET_HEIGHT//2, RACKET_WIDTH, RACKET_HEIGHT)
        player2 = Player(WIDTH - 15 - RACKET_WIDTH, HEIGHT//2 - RACKET_HEIGHT//2, RACKET_WIDTH, RACKET_HEIGHT)
        ball = Ball(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, is_real=True, color=WHITE)

        ctrl_player1 = KeyboardController()
        ctrl_player2 = CpuController()
        mult_manager = MultiplicationManager()
        ctrl_physics = PhysicsManager(mult_manager)
        ctrl_score   = ScoreManager()

        game = Game(screen, player1, player2, ball, ctrl_player1, ctrl_player2, ctrl_physics, ctrl_score)
        game.run()

if __name__ == "__main__":
    main()