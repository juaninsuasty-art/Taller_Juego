# Arkanoid - Metodologías de Desarrollo de Software
# Universidad del Valle

import pygame
import sys

pygame.init()

W, H = 520, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

# Paleta
PAD_W, PAD_H = 80, 10
PAD_Y = H - 40
pad_x = W // 2

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Movimiento con teclado
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pad_x -= 5

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        pad_x += 5

    # Límites de pantalla
    pad_x = max(PAD_W // 2, min(W - PAD_W // 2, pad_x))

    screen.fill((10, 10, 20))

    pygame.draw.rect(
        screen,
        (180, 180, 255),
        (pad_x - PAD_W // 2, PAD_Y, PAD_W, PAD_H),
        border_radius=5
    )

    pygame.display.flip()