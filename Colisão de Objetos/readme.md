# 🎮 DVD Bounce com Pygame

Este projeto é uma pequena simulação feita em **Python** utilizando a biblioteca **Pygame**, onde dois textos se movimentam pela tela, quicam nas bordas da janela e colidem entre si trocando de direção.

Quando eles batem:

* Mudam de direção.
* Trocam suas velocidades.
* Mudam de cor aleatoriamente.

---

## 📦 Tecnologias utilizadas

* Python 3
* Pygame

---

## 🖥️ O que o programa faz

O programa abre uma janela de **800x600 pixels** onde dois textos ficam se movendo continuamente.

Eles possuem:

* Velocidade aleatória inicial
* Detecção de colisão com bordas
* Detecção de colisão entre si
* Mudança de cor dinâmica

---

## 🧠 Estrutura do código

O código foi organizado em funções para facilitar a leitura e manutenção.

### Função `gerar_velocidade()`

Gera uma velocidade aleatória para o texto.

Ela garante que a velocidade **não seja (0,0)** para que o objeto não fique parado.

```python
vx, vy = gerar_velocidade()
```

---

### Função `cor_aleatoria()`

Gera uma cor RGB aleatória.

```python
(123, 45, 200)
```

Usada quando ocorre colisão.

---

### Função `criar_texto()`

Responsável por:

* Renderizar o texto na tela
* Criar o retângulo de colisão (`rect`)
* Definir a posição inicial

```python
texto, rect = criar_texto(fonte, texto_str, BRANCO, posicao)
```

---

### Função `atualizar_colisao_borda()`

Verifica se o texto bateu nas bordas da tela:

* Direita
* Esquerda
* Topo
* Base

Quando isso acontece:

* A direção muda
* A cor do texto muda

---

## 💥 Colisão entre os textos

A colisão é detectada usando:

```python
rect1.colliderect(rect2)
```

Quando os textos se encostam:

* As velocidades são trocadas
* A cor dos dois muda

Isso cria um efeito de **troca de movimento**, simulando um impacto simples.
