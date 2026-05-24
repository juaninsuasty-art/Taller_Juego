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

BRICK_COLORS = [
    (90, 220, 220),
    (80, 180, 230),
    (100, 140, 230),
    (150, 120, 230),
    (170, 110, 200),
    (60, 130, 150),
]

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

# Ladrillos
BRICK_COLS = 13
BRICK_ROWS = 6
BRICK_W = 36
BRICK_H = 14
BRICK_GAP = 2
BRICK_OFF_X = (W - BRICK_COLS * (BRICK_W + BRICK_GAP) + BRICK_GAP) // 2
BRICK_OFF_Y = 55


# TJ-23 crear ladrillos
def crear_ladrillos():
    ladrillos = []

    for fila in range(BRICK_ROWS):
        for columna in range(BRICK_COLS):
            rect = pygame.Rect(
                BRICK_OFF_X + columna * (BRICK_W + BRICK_GAP),
                BRICK_OFF_Y + fila * (BRICK_H + BRICK_GAP),
                BRICK_W,
                BRICK_H
            )

            ladrillos.append({
                "rect": rect,
                "color": BRICK_COLORS[fila],
                "activo": True
            })

    return ladrillos


def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy

    ball_x = float(W // 2)
    ball_y = float(PAD_Y - BALL_R - 2)
    ball_dx = 4.0
    ball_dy = -4.0


ladrillos = crear_ladrillos()

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
    if ball_x - BALL_R <= 0:
        ball_x = BALL_R
        ball_dx = abs(ball_dx)

    if ball_x + BALL_R >= W:
        ball_x = W - BALL_R
        ball_dx = -abs(ball_dx)

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

    # Deteccion de colision pelota-ladrillo - TJ-23
    for ladrillo in ladrillos:
        if not ladrillo["activo"]:
            continue

        if ladrillo["rect"].collidepoint(ball_x, ball_y):
            ladrillo["activo"] = False
            ball_dy = -ball_dy
            break

    # Limite inferior: si la pelota cae, se reinicia
    if ball_y - BALL_R > H:
        reset_ball()

    # Dibujo
    screen.fill(BG)

    # Dibujar ladrillos
    for ladrillo in ladrillos:
        if ladrillo["activo"]:
            pygame.draw.rect(
                screen,
                ladrillo["color"],
                ladrillo["rect"],
                border_radius=2
            )

    # Dibujar paleta
    pygame.draw.rect(
        screen,
        PAD_COL,
        (pad_x - PAD_W // 2, PAD_Y, PAD_W, PAD_H)
    )

    # Dibujar pelota
    pygame.draw.circle(
        screen,
        BALL_COL,
        (int(ball_x), int(ball_y)),
        BALL_R
    )

    pygame.display.flip()