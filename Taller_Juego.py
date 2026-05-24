import pygame
import sys

pygame.init()

W, H = 520, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

# Colores
BG = (10, 10, 20)
PAD_COL = (180, 180, 255)
BALL_COL = (255, 255, 255)

# Paleta
PAD_W, PAD_H = 80, 10
PAD_Y = H - 40
pad_x = W // 2

# Pelota
BALL_R = 7
ball_x = float(W // 2)
ball_y = float(PAD_Y - BALL_R - 2)
ball_dx = 4.0
ball_dy = -4.0


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy

    ball_x = float(W // 2)
    ball_y = float(PAD_Y - BALL_R - 2)
    ball_dx = 4.0
    ball_dy = -4.0


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento paleta con teclado
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pad_x -= 5

    if keys[pygame.K_RIGHT] or keys[pygame.K_b]:
        pad_x += 5

    # Limites de pantalla para la paleta
    pad_x = max(PAD_W // 2, min(W - PAD_W // 2, pad_x))

    # Mover pelota
    ball_x += ball_dx
    ball_y += ball_dy

    # Perimetro de colision en paredes - TJ-22

    # Pared izquierda
    if ball_x - BALL_R <= 0:
        ball_x = BALL_R
        ball_dx = abs(ball_dx)

    # Pared derecha
    if ball_x + BALL_R >= W:
        ball_x = W - BALL_R
        ball_dx = -abs(ball_dx)

    # Techo
    if ball_y - BALL_R <= 0:
        ball_y = BALL_R
        ball_dy = abs(ball_dy)

    # Rebote con control en plataforma - TJ-21
    if (
        PAD_Y <= ball_y + BALL_R <= PAD_Y + PAD_H
        and pad_x - PAD_W // 2 <= ball_x <= pad_x + PAD_W // 2
        and ball_dy > 0
    ):
        rel = (ball_x - pad_x) / (PAD_W / 2)
        ball_dx = rel * 5
        ball_dy = -abs(ball_dy)
        ball_y = PAD_Y - BALL_R - 1

    # Limite inferior: si la pelota cae, se reinicia
    if ball_y - BALL_R > H:
        reset_ball()

    # Dibujo
    screen.fill(BG)

    pygame.draw.rect(
        screen,
        PAD_COL,
        (pad_x - PAD_W // 2, PAD_Y, PAD_W, PAD_H)
    )

    pygame.draw.circle(
        screen,
        BALL_COL,
        (int(ball_x), int(ball_y)),
        BALL_R
    )

    pygame.display.flip()