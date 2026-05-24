import pygame
import sys

pygame.init()

W, H = 520, 480
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Arkanoid")
clock = pygame.time.Clock()

# =========================
# Colores
# =========================
BG = (6, 10, 28)
CYAN_DARK = (18, 55, 72)
CYAN_SOFT = (45, 150, 180)
CYAN_BRIGHT = (90, 220, 235)

PANEL_COL = (12, 18, 42)
PANEL_BORDER = (70, 170, 210)

PAD_COL = (180, 180, 255)
BALL_COL = (255, 255, 255)

TEXT_COL = (225, 235, 255)
SUBTEXT_COL = (170, 190, 220)

BUTTON_COL = (55, 145, 195)
BUTTON_HOVER = (80, 185, 225)
BUTTON_BORDER = (210, 245, 255)
BUTTON_TEXT = (245, 250, 255)

TITLE_MAIN = (255, 255, 255)
TITLE_GLOW = (70, 220, 235)
TITLE_OUTLINE = (20, 90, 130)

BRICK_COLORS = [
    (90, 220, 220),
    (80, 180, 230),
    (100, 140, 230),
    (150, 120, 230),
    (170, 110, 200),
    (60, 130, 150),
]

# =========================
# Fuentes
# =========================
font_title = pygame.font.SysFont("Arial Black", 42)
font_subtitle = pygame.font.SysFont("Consolas", 16, bold=True)
font_menu = pygame.font.SysFont("Arial", 21, bold=True)
font_med = pygame.font.SysFont("Arial", 18, bold=True)
font_small = pygame.font.SysFont("Consolas", 15)

# =========================
# Paleta
# =========================
PAD_W, PAD_H = 80, 10
PAD_Y = H - 40
pad_x = W // 2

# =========================
# Pelota
# =========================
BALL_R = 7
ball_x = float(W // 2)
ball_y = float(PAD_Y - BALL_R - 2)
ball_dx = 4.0
ball_dy = -4.0

# =========================
# Estado del juego
# =========================
estado = "menu"   # menu | controles | configuracion | ready | playing | game_over

# TJ-26 vidas iniciales
vidas = 3

# =========================
# Botones
# =========================
btn_start = pygame.Rect(W // 2 - 95, 220, 190, 40)
btn_controls = pygame.Rect(W // 2 - 95, 272, 190, 40)
btn_settings = pygame.Rect(W // 2 - 95, 324, 190, 40)
btn_quit = pygame.Rect(W // 2 - 95, 376, 190, 40)

btn_exit_sub = pygame.Rect(W // 2 - 80, 388, 160, 36)
btn_back_menu = pygame.Rect(W // 2 - 105, 330, 210, 40)

# =========================
# Ladrillos
# =========================
BRICK_COLS = 13
BRICK_ROWS = 6
BRICK_W = 36
BRICK_H = 14
BRICK_GAP = 2
BRICK_OFF_X = (W - BRICK_COLS * (BRICK_W + BRICK_GAP) + BRICK_GAP) // 2
BRICK_OFF_Y = 55


# =========================
# Funciones base
# =========================
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

    ball_x = float(pad_x)
    ball_y = float(PAD_Y - BALL_R - 2)
    ball_dx = 4.0
    ball_dy = -4.0


# TJ-26 reiniciar partida completa
def reiniciar_partida():
    global vidas, ladrillos, estado

    vidas = 3
    ladrillos = crear_ladrillos()
    reset_ball()
    estado = "ready"


def draw_pattern_background():
    screen.fill(BG)

    for y in range(0, H, 22):
        for x in range(0, W, 26):
            px = x + ((y // 22) % 2) * 10
            py = y + 8

            if 0 <= px < W and 0 <= py < H:
                pygame.draw.circle(screen, CYAN_DARK, (px, py), 1)
                pygame.draw.line(
                    screen,
                    (20, 85, 110),
                    (px - 3, py + 4),
                    (px + 3, py - 2),
                    1
                )


def draw_text_outline(texto, fuente, color_texto, color_borde, x, y):
    offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]

    for dx, dy in offsets:
        borde = fuente.render(texto, True, color_borde)
        screen.blit(borde, (x + dx, y + dy))

    texto_main = fuente.render(texto, True, color_texto)
    screen.blit(texto_main, (x, y))


def dibujar_logo():
    texto = "ARKANOID"
    glow = font_title.render(texto, True, TITLE_GLOW)
    gx = W // 2 - glow.get_width() // 2
    gy = 76

    screen.blit(glow, (gx - 2, gy))
    screen.blit(glow, (gx + 2, gy))
    screen.blit(glow, (gx, gy - 2))
    screen.blit(glow, (gx, gy + 2))

    draw_text_outline(texto, font_title, TITLE_MAIN, TITLE_OUTLINE, gx, gy)

    pygame.draw.line(screen, CYAN_BRIGHT, (145, 125), (375, 125), 2)
    pygame.draw.line(screen, CYAN_SOFT, (165, 132), (355, 132), 1)

    subt = font_subtitle.render("METODOLOGIAS DE DESARROLLO DE SOFTWARE", True, SUBTEXT_COL)
    screen.blit(subt, (W // 2 - subt.get_width() // 2, 142))


def dibujar_boton(rect, texto):
    mouse_pos = pygame.mouse.get_pos()
    hover = rect.collidepoint(mouse_pos)

    color = BUTTON_HOVER if hover else BUTTON_COL

    pygame.draw.rect(screen, color, rect, border_radius=10)
    pygame.draw.rect(screen, BUTTON_BORDER, rect, width=2, border_radius=10)

    pygame.draw.line(
        screen,
        (220, 250, 255),
        (rect.left + 8, rect.top + 6),
        (rect.right - 8, rect.top + 6),
        1
    )

    label = font_menu.render(texto, True, BUTTON_TEXT)
    screen.blit(
        label,
        (
            rect.centerx - label.get_width() // 2,
            rect.centery - label.get_height() // 2
        )
    )


def dibujar_panel(x, y, w, h):
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, PANEL_COL, rect, border_radius=16)
    pygame.draw.rect(screen, PANEL_BORDER, rect, width=2, border_radius=16)
    return rect


# =========================
# Pantallas de interfaz
# =========================
def dibujar_menu():
    draw_pattern_background()
    dibujar_panel(75, 45, 370, 390)
    dibujar_logo()

    ayuda = font_small.render("Selecciona una opcion con click izquierdo", True, SUBTEXT_COL)
    screen.blit(ayuda, (W // 2 - ayuda.get_width() // 2, 180))

    dibujar_boton(btn_start, "INICIAR")
    dibujar_boton(btn_controls, "CONTROLES")
    dibujar_boton(btn_settings, "CONFIGURACION")
    dibujar_boton(btn_quit, "SALIR")


def dibujar_controles():
    draw_pattern_background()
    dibujar_panel(60, 40, 400, 400)

    titulo = font_title.render("CONTROLES", True, TITLE_MAIN)
    screen.blit(titulo, (W // 2 - titulo.get_width() // 2, 72))

    pygame.draw.line(screen, CYAN_BRIGHT, (145, 122), (375, 122), 2)

    items = [
        ("MOVER IZQUIERDA", "Flecha izquierda o A"),
        ("MOVER DERECHA", "Flecha derecha o B"),
        ("LANZAR PELOTA", "Barra espaciadora"),
        ("NAVEGAR MENU", "Click izquierdo"),
    ]

    y = 165
    for accion, tecla in items:
        txt1 = font_med.render(accion, True, TEXT_COL)
        txt2 = font_small.render(tecla, True, SUBTEXT_COL)

        screen.blit(txt1, (95, y))
        screen.blit(txt2, (95, y + 22))

        pygame.draw.line(screen, CYAN_DARK, (92, y + 46), (428, y + 46), 1)
        y += 58

    dibujar_boton(btn_exit_sub, "EXIT")


def dibujar_configuracion():
    draw_pattern_background()
    dibujar_panel(60, 40, 400, 400)

    titulo = font_title.render("CONFIGURACION", True, TITLE_MAIN)
    screen.blit(titulo, (W // 2 - titulo.get_width() // 2, 80))

    pygame.draw.line(screen, CYAN_BRIGHT, (120, 130), (400, 130), 2)

    t1 = font_med.render("Seccion reservada para Version 2", True, TEXT_COL)
    t2 = font_small.render("Aqui iran sonido y ajustes del juego.", True, SUBTEXT_COL)

    screen.blit(t1, (W // 2 - t1.get_width() // 2, 205))
    screen.blit(t2, (W // 2 - t2.get_width() // 2, 235))

    dibujar_boton(btn_exit_sub, "EXIT")


# TJ-26 pantalla de Game Over
def dibujar_game_over():
    draw_pattern_background()
    dibujar_panel(70, 70, 380, 330)

    titulo = font_title.render("GAME OVER", True, TITLE_MAIN)
    screen.blit(titulo, (W // 2 - titulo.get_width() // 2, 120))

    texto = font_med.render("Te quedaste sin vidas", True, TEXT_COL)
    screen.blit(texto, (W // 2 - texto.get_width() // 2, 190))

    ayuda = font_small.render("Puedes volver al menu principal.", True, SUBTEXT_COL)
    screen.blit(ayuda, (W // 2 - ayuda.get_width() // 2, 225))

    dibujar_boton(btn_back_menu, "VOLVER AL MENU")


def dibujar_mensaje_ready():
    txt = font_med.render("Presiona ESPACIO para lanzar", True, TEXT_COL)
    screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 + 105))


# =========================
# Inicialización
# =========================
ladrillos = crear_ladrillos()

# =========================
# Bucle principal
# =========================
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # =========================
        # Navegación de menús
        # =========================
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if estado == "menu":
                if btn_start.collidepoint(event.pos):
                    reiniciar_partida()

                elif btn_controls.collidepoint(event.pos):
                    estado = "controles"

                elif btn_settings.collidepoint(event.pos):
                    estado = "configuracion"

                elif btn_quit.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

            elif estado == "controles":
                if btn_exit_sub.collidepoint(event.pos):
                    estado = "menu"

            elif estado == "configuracion":
                if btn_exit_sub.collidepoint(event.pos):
                    estado = "menu"

            elif estado == "game_over":
                if btn_back_menu.collidepoint(event.pos):
                    estado = "menu"

        # =========================
        # Lanzar pelota
        # =========================
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and estado == "ready":
                estado = "playing"

    # =========================
    # Pantallas de menú
    # =========================
    if estado == "menu":
        dibujar_menu()
        pygame.display.flip()
        continue

    if estado == "controles":
        dibujar_controles()
        pygame.display.flip()
        continue

    if estado == "configuracion":
        dibujar_configuracion()
        pygame.display.flip()
        continue

    if estado == "game_over":
        dibujar_game_over()
        pygame.display.flip()
        continue

    # =========================
    # Movimiento paleta - TJ-19
    # =========================
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pad_x -= 5

    if keys[pygame.K_RIGHT] or keys[pygame.K_b]:
        pad_x += 5

    pad_x = max(PAD_W // 2, min(W - PAD_W // 2, pad_x))

    # =========================
    # Estado READY
    # =========================
    if estado == "ready":
        ball_x = float(pad_x)
        ball_y = float(PAD_Y - BALL_R - 2)

    # =========================
    # Estado PLAYING
    # =========================
    if estado == "playing":
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

        # TJ-26: si cae la pelota, se resta una vida
        if ball_y - BALL_R > H:
            vidas -= 1

            if vidas <= 0:
                estado = "game_over"
            else:
                reset_ball()
                estado = "ready"

    # =========================
    # Dibujo del juego
    # =========================
    draw_pattern_background()

    for ladrillo in ladrillos:
        if ladrillo["activo"]:
            pygame.draw.rect(
                screen,
                ladrillo["color"],
                ladrillo["rect"],
                border_radius=2
            )

    pygame.draw.rect(
        screen,
        PAD_COL,
        (pad_x - PAD_W // 2, PAD_Y, PAD_W, PAD_H),
        border_radius=5
    )

    pygame.draw.circle(
        screen,
        BALL_COL,
        (int(ball_x), int(ball_y)),
        BALL_R
    )

    if estado == "ready":
        dibujar_mensaje_ready()

    pygame.display.flip()