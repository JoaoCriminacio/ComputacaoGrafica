# 🏓 Pong Game 
Este projeto é uma implementação clássica do jogo Pong feita em Python utilizando a biblioteca Pygame. O jogo coloca um jogador humano contra uma inteligência artificial simples (CPU) em uma disputa de 10 pontos.

O jogo apresenta:
- Menu inicial interativo.
- Movimentação fluida das raquetes.
- Sistema de pontuação em tempo real.
- Uma CPU que segue a trajetória da bola.

---

## 📦 Tecnologias utilizadas
- Python 3
- Pygame

---

## 🖥️ O que o programa faz
O programa abre uma janela de 800x600 pixels e inicia em uma tela de menu. Após pressionar a tecla de espaço, o jogo começa.

As principais mecânicas são:
- Jogador: Controlado pelas setas (Cima/Baixo).
- CPU: Segue automaticamente a posição vertical da bola.
- Colisão: A bola rebate nas raquetes e nas bordas superiores/inferiores.
- Pontuação: Quando a bola sai pelas laterais, o ponto é computado e a bola retorna ao centro.
- Condição de Vitória: O jogo encerra e volta ao menu quando alguém atinge 10 pontos.

---

## 🧠 Estrutura do código
O código foi organizado utilizando Orientação a Objetos, dividindo as responsabilidades em classes específicas.

### Classe `Player`:
Representa as raquetes. Define as dimensões, velocidade e os métodos de movimentação e desenho.

```Python
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
```

### Classe `Ball`
Controla a física da bola, sua direção aleatória inicial e o método de reset após um ponto.

```Python
class Ball:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = random.choice([-5, 5])
        self.speed_y = random.choice([-5, -4, -3, -2, -1, 1, 2, 3, 4, 5])

    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
```

### Classe `InputController`
Contém a lógica da movimentação do jogador, caso clique na seta para cima a raquete sobe, caso contrário, desce.

```Python
class InputController:
    def handle(self, player):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            player.move_up()
        if keys[pygame.K_DOWN]:
            player.move_down()
```

### Classe `CpuController`
Contém a lógica da Inteligência Artificial, que ajusta a posição do Player 2 com base na posição central da bola.

```Python
class CpuController:
    def update(self, player, ball):
        if player.rect.centery < ball.rect.centery:
            player.move_down()
        elif player.rect.centery > ball.rect.centery:
            player.move_up()
```

### Classe `CollisionManager`
Responsável por gerenciar todas as colisões físicas e a lógica de pontuação do jogo.

```Python
class CollisionManager:
    def handle_ball_collision(self, ball, player1, player2):
        if ball.rect.colliderect(player1.rect) or ball.rect.colliderect(player2.rect):
            ball.speed_x *= -1

        if ball.rect.y <= 0 or ball.rect.y >= HEIGHT - ball.size:
            ball.speed_y *= -1
```

### Função `main()`
Orquestra o fluxo principal, alternando entre a instância do Menu e a instância do Game.

```Python
def main():
    while True:
        menu = Menu(screen)
        if not menu.run():
            break

        game = Game()
        game.run()

    pygame.quit()
    sys.exit()
```