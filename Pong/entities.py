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
    def __init__(self, x, y, size, is_real=True, color=WHITE):
        self.size = size
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = 0
        self.speed_y = 0
        self.is_real = is_real
        self.color = color
        self.reset()

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def reset(self):
        self.rect.x = WIDTH//2 - self.size//2
        self.rect.y = HEIGHT//2 - self.size//2
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

    def draw(self, screen, color=None):
        draw_color = color if color is not None else self.color
        pygame.draw.circle(screen, draw_color, self.rect.center, self.size)

class BallFactory:
    def random_color():
        while True:
            r = random.randint(80, 255)
            g = random.randint(80, 255)
            b = random.randint(80, 255)
            return (r, g, b)

    def create_decoys(origin: Ball, count: int = 3):
        decoys = []
        for _ in range(count):
            color = BallFactory.random_color()
            decoy = Ball(
                origin.rect.x,
                origin.rect.y,
                origin.size,
                is_real=False,
                color=color,
            )
            decoy.speed_x = random.choice([-1, 1]) * random.randint(3, 8)
            decoy.speed_y = random.choice([-1, 1]) * random.randint(2, 7)
            decoys.append(decoy)
        return decoys
    
class MultiplicationTimer:
    INTERVAL_MS = 5_000

    def __init__(self):
        self._last_trigger = pygame.time.get_ticks()

    def is_ready(self):
        return pygame.time.get_ticks() - self._last_trigger >= self.INTERVAL_MS

    def reset(self):
        self._last_trigger = pygame.time.get_ticks()

class MultiplicationManager:
    DECOY_COUNT = 3

    def __init__(self):
        self._timer = MultiplicationTimer()

    def notify_paddle_hit(self, ball: Ball):
        if not self._timer.is_ready():
            return None
        if not ball.is_real:
            return None

        self._timer.reset()
        return BallFactory.create_decoys(ball, count=self.DECOY_COUNT)

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
    def __init__(self, multiplication_manager = None):
        self.MAX_SPEED = 20
        self.SPEED_MULTIPLIER = 1.05
        self._mult = multiplication_manager

    def handle_collisions(self, ball: Ball, player1: Player, player2: Player):
        fragments = None

        if ball.rect.colliderect(player1.rect):
            ball.rect.left = player1.rect.right
            ball.speed_x = abs(ball.speed_x) * self.SPEED_MULTIPLIER
            ball.speed_y *= self.SPEED_MULTIPLIER
            if self._mult:
                fragments = self._mult.notify_paddle_hit(ball)

        elif ball.rect.colliderect(player2.rect):
            ball.rect.right = player2.rect.left
            ball.speed_x = -abs(ball.speed_x) * self.SPEED_MULTIPLIER
            ball.speed_y *= self.SPEED_MULTIPLIER
            if self._mult:
                fragments = self._mult.notify_paddle_hit(ball)

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.size:
            ball.speed_y *= -1

        ball.speed_x = max(-self.MAX_SPEED, min(self.MAX_SPEED, ball.speed_x))
        ball.speed_y = max(-self.MAX_SPEED, min(self.MAX_SPEED, ball.speed_y))
 
        return fragments
    
class ScoreManager:
    def check_scoring(self, balls: list, player1: Player, player2: Player):
        real_scored = False

        for ball in balls:
            if not ball.is_real:
                continue
            if ball.rect.x <= 0:
                player2.score += 1
                ball.reset()
                real_scored = True
            elif ball.rect.x >= WIDTH - ball.size:
                player1.score += 1
                ball.reset()
                real_scored = True

        if real_scored:
            return [b for b in balls if b.is_real]

        surviving = []
        for ball in balls:
            if ball.is_real:
                surviving.append(ball)
            elif 0 <= ball.rect.x <= WIDTH - ball.size:
                surviving.append(ball)

        return surviving