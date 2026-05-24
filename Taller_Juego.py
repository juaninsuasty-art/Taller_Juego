import pygame
import sys
import math
import array
import random

pygame.init()

# =========================
# Sonido - TJ-31
# =========================
try:
    pygame.mixer.init(frequency=44100, size=-16, channels=1)
    SOUND_ENABLED = True
except pygame.error:
    SOUND_ENABLED = False


def crear_sonido(frecuencia, duracion, volumen=0.35):
    sample_rate = 44100
    muestras = array.array("h")
    total_muestras = int(sample_rate * duracion)

    for i in range(total_muestras):
        t = i / sample_rate
        fade = 1 - (i / total_muestras)
        valor = int(
            volumen
            * 32767
            * fade
            * math.sin(2 * math.pi * frecuencia * t)
        )
        muestras.append(valor)

    return pygame.mixer.Sound(buffer=muestras.tobytes())


def reproducir_sonido(sonido):
    if SOUND_ENABLED and sonido is not None:
        sonido.play()


if SOUND_ENABLED:
    SND_MENU = crear_sonido(520, 0.08, 0.25)
    SND_PALETA = crear_sonido(720, 0.07, 0.30)
    SND_LADRILLO = crear_sonido(420, 0.09, 0.35)
    SND_VIDA = crear_sonido(180, 0.20, 0.35)
    SND_GAME_OVER = crear_sonido(120, 0.35, 0.35)
    SND_WIN = crear_sonido(880, 0.25, 0.30)
    SND_POWER = crear_sonido(980, 0.15, 0.35)
else:
    SND_MENU = None
    SND_PALETA = None
    SND_LADRILLO = None
    SND_VIDA = None
    SND_GAME_OVER = None
    SND_WIN = None
    SND_POWER = None


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

HEART_COL = (255, 90, 120)
WARNING_COL = (255, 210, 120)
WIN_COL = (120, 255, 220)

POWER_WIDE_COL = (120, 255, 180)
POWER_BIG_COL = (255, 220, 120)
POWER_MULTI_COL = (190, 140, 255)

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
PAD_W_NORMAL = 80
PAD_W_BIG = 120
PAD_W = PAD_W_NORMAL
PAD_H = 10
PAD_Y = H - 40
pad_x = W // 2

# =========================
# Pelotas
# =========================
BALL_R_NORMAL = 7
BALL_R_BIG = 11
BALL_R = BALL_R_NORMAL
pelotas = []

# =========================
# Power-ups - TJ-37
# =========================
powerups = []
powerup_speed = 2.2
powerup_timer = 0
active_powerup = None
POWERUP_DURATION = 600

# =========================
# Estado del juego
# =========================
estado = "menu"

# =========================
# Estado de partida
# =========================
vidas = 3
score = 0
nivel = 1

# =========================
# Botones
# =========================
btn_start = pygame.Rect(W // 2 - 95, 220, 190, 40)
btn_controls = pygame.Rect(W // 2 - 95, 272, 190, 40)
btn_settings = pygame.Rect(W // 2 - 95, 324, 190, 40)
btn_quit = pygame.Rect(W // 2 - 95, 376, 190, 40)

btn_exit_sub = pygame.Rect(W // 2 - 80, 388, 160, 36)
btn_back_menu = pygame.Rect(W // 2 - 105, 330, 210, 40)

btn_next_level = pygame.Rect(W // 2 - 105, 305, 210, 40)
btn_win_menu = pygame.Rect(W // 2 - 105, 355, 210, 40)

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
# Niveles - TJ-33, TJ-34, TJ-36
# =========================
def crear_nivel(nivel_actual):
    ladrillos_nivel = []

    filas_resistentes = min(BRICK_ROWS, 1 + nivel_actual)

    for fila in range(BRICK_ROWS):
        for columna in range(BRICK_COLS):
            rect = pygame.Rect(
                BRICK_OFF_X + columna * (BRICK_W + BRICK_GAP),
                BRICK_OFF_Y + fila * (BRICK_H + BRICK_GAP),
                BRICK_W,
                BRICK_H
            )

            if fila < filas_resistentes:
                vida_ladrillo = 2
            else:
                vida_ladrillo = 1

            if nivel_actual >= 3 and fila == 0:
                vida_ladrillo = 3

            ladrillos_nivel.append({
                "rect": rect,
                "color": BRICK_COLORS[fila],
                "color_original": BRICK_COLORS[fila],
                "activo": True,
                "vida": vida_ladrillo,
                "vida_max": vida_ladrillo,
                "puntos": (BRICK_ROWS - fila) * 10
            })

    return ladrillos_nivel


def velocidad_por_nivel():
    return 4.0 + (nivel - 1) * 0.4


def crear_pelota(x, y, dx, dy):
    return {
        "x": float(x),
        "y": float(y),
        "dx": float(dx),
        "dy": float(dy)
    }


def reset_pelotas():
    global pelotas

    velocidad = velocidad_por_nivel()

    pelotas = [
        crear_pelota(
            pad_x,
            PAD_Y - BALL_R - 2,
            velocidad,
            -velocidad
        )
    ]


def reset_powerups():
    global powerups, active_powerup, powerup_timer, PAD_W, BALL_R

    powerups = []
    active_powerup = None
    powerup_timer = 0
    PAD_W = PAD_W_NORMAL
    BALL_R = BALL_R_NORMAL


def oscurecer_color(color):
    return (
        max(0, color[0] - 45),
        max(0, color[1] - 45),
        max(0, color[2] - 45)
    )


def reiniciar_partida():
    global vidas, score, nivel, ladrillos, estado

    vidas = 3
    score = 0
    nivel = 1
    reset_powerups()
    ladrillos = crear_nivel(nivel)
    reset_pelotas()
    estado = "ready"


def pasar_siguiente_nivel():
    global nivel, ladrillos, estado

    nivel += 1
    reset_powerups()
    ladrillos = crear_nivel(nivel)
    reset_pelotas()
    estado = "ready"


def nivel_completado():
    for ladrillo in ladrillos:
        if ladrillo["activo"]:
            return False
    return True


# =========================
# Power-ups - TJ-37
# =========================
def crear_powerup(x, y):
    tipo = random.choice(["WIDE", "BIG", "MULTI"])

    rect = pygame.Rect(int(x) - 17, int(y) - 8, 34, 16)

    if tipo == "WIDE":
        color = POWER_WIDE_COL
    elif tipo == "BIG":
        color = POWER_BIG_COL
    else:
        color = POWER_MULTI_COL

    powerups.append({
        "rect": rect,
        "tipo": tipo,
        "color": color
    })


def intentar_lanzar_powerup(x, y):
    if random.random() < 0.25:
        crear_powerup(x, y)


def agregar_multiples_pelotas():
    """
    TJ-37:
    Power-up MULTI. Crea dos pelotas adicionales a partir
    de la primera pelota disponible.
    """
    if len(pelotas) == 0:
        return

    base = pelotas[0]
    velocidad = velocidad_por_nivel()

    pelotas.append(
        crear_pelota(
            base["x"],
            base["y"],
            -velocidad,
            -abs(velocidad)
        )
    )

    pelotas.append(
        crear_pelota(
            base["x"],
            base["y"],
            velocidad * 0.6,
            -abs(velocidad)
        )
    )


def aplicar_powerup(tipo):
    global PAD_W, BALL_R, active_powerup, powerup_timer

    reproducir_sonido(SND_POWER)

    if tipo == "MULTI":
        agregar_multiples_pelotas()
        return

    active_powerup = tipo
    powerup_timer = POWERUP_DURATION

    if tipo == "WIDE":
        PAD_W = PAD_W_BIG
        BALL_R = BALL_R_NORMAL

    elif tipo == "BIG":
        BALL_R = BALL_R_BIG
        PAD_W = PAD_W_NORMAL


def actualizar_powerups():
    global powerup_timer, active_powerup, PAD_W, BALL_R

    for powerup in powerups[:]:
        powerup["rect"].y += powerup_speed

        pad_rect = pygame.Rect(
            int(pad_x - PAD_W // 2),
            PAD_Y,
            PAD_W,
            PAD_H
        )

        if powerup["rect"].colliderect(pad_rect):
            aplicar_powerup(powerup["tipo"])
            powerups.remove(powerup)

        elif powerup["rect"].top > H:
            powerups.remove(powerup)

    if active_powerup is not None:
        powerup_timer -= 1

        if powerup_timer <= 0:
            active_powerup = None
            powerup_timer = 0
            PAD_W = PAD_W_NORMAL
            BALL_R = BALL_R_NORMAL


def dibujar_powerups():
    for powerup in powerups:
        pygame.draw.rect(
            screen,
            powerup["color"],
            powerup["rect"],
            border_radius=5
        )

        pygame.draw.rect(
            screen,
            (255, 255, 255),
            powerup["rect"],
            width=1,
            border_radius=5
        )

        label = font_small.render(powerup["tipo"], True, (10, 10, 20))
        screen.blit(
            label,
            (
                powerup["rect"].centerx - label.get_width() // 2,
                powerup["rect"].centery - label.get_height() // 2
            )
        )


# =========================
# Dibujo general
# =========================
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
    offsets = [
        (-2, 0), (2, 0), (0, -2), (0, 2),
        (-2, -2), (2, -2), (-2, 2), (2, 2)
    ]

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
        ("POWER-UPS", "Atrapa las mejoras que caen"),
    ]

    y = 145
    for accion, tecla in items:
        txt1 = font_med.render(accion, True, TEXT_COL)
        txt2 = font_small.render(tecla, True, SUBTEXT_COL)

        screen.blit(txt1, (95, y))
        screen.blit(txt2, (95, y + 22))

        pygame.draw.line(screen, CYAN_DARK, (92, y + 46), (428, y + 46), 1)
        y += 48

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


def dibujar_game_over():
    draw_pattern_background()
    dibujar_panel(70, 70, 380, 330)

    titulo = font_title.render("GAME OVER", True, WARNING_COL)
    screen.blit(titulo, (W // 2 - titulo.get_width() // 2, 115))

    texto = font_med.render(f"Puntuacion final: {score}", True, TEXT_COL)
    screen.blit(texto, (W // 2 - texto.get_width() // 2, 185))

    ayuda = font_small.render("La partida ha terminado.", True, SUBTEXT_COL)
    screen.blit(ayuda, (W // 2 - ayuda.get_width() // 2, 220))

    dibujar_boton(btn_back_menu, "VOLVER AL MENU")


def dibujar_felicitaciones():
    draw_pattern_background()
    dibujar_panel(60, 50, 400, 380)

    titulo = font_title.render("FELICITACIONES", True, WIN_COL)
    screen.blit(titulo, (W // 2 - titulo.get_width() // 2, 90))

    texto1 = font_med.render(f"Completaste el nivel {nivel}", True, TEXT_COL)
    texto2 = font_med.render(f"Puntuacion: {score}", True, TEXT_COL)
    texto3 = font_small.render("Puedes continuar o volver al menu.", True, SUBTEXT_COL)

    screen.blit(texto1, (W // 2 - texto1.get_width() // 2, 165))
    screen.blit(texto2, (W // 2 - texto2.get_width() // 2, 195))
    screen.blit(texto3, (W // 2 - texto3.get_width() // 2, 230))

    dibujar_boton(btn_next_level, "CONTINUAR")
    dibujar_boton(btn_win_menu, "MENU")


def dibujar_vidas():
    corazones = "♥ " * vidas
    texto = font_med.render(corazones, True, HEART_COL)
    screen.blit(texto, (18, 14))


def dibujar_hud():
    hud = font_small.render(
        f"PUNTOS: {score}     NIVEL: {nivel}",
        True,
        TEXT_COL
    )
    screen.blit(hud, (W - hud.get_width() - 18, 16))

    if active_powerup is not None:
        texto = font_small.render(f"POWER: {active_powerup}", True, CYAN_BRIGHT)
        screen.blit(texto, (W // 2 - texto.get_width() // 2, 16))

    if len(pelotas) > 1:
        multi = font_small.render(f"PELOTAS: {len(pelotas)}", True, POWER_MULTI_COL)
        screen.blit(multi, (W // 2 - multi.get_width() // 2, 34))


def dibujar_aviso_vida_perdida():
    caja = pygame.Rect(W // 2 - 150, H // 2 - 45, 300, 90)

    pygame.draw.rect(screen, PANEL_COL, caja, border_radius=12)
    pygame.draw.rect(screen, CYAN_BRIGHT, caja, width=2, border_radius=12)

    aviso = font_med.render("VIDA PERDIDA", True, WARNING_COL)
    ayuda = font_small.render("Presiona ENTER para continuar", True, SUBTEXT_COL)

    screen.blit(aviso, (W // 2 - aviso.get_width() // 2, H // 2 - 25))
    screen.blit(ayuda, (W // 2 - ayuda.get_width() // 2, H // 2 + 8))


def dibujar_mensaje_ready():
    txt = font_med.render("Presiona ESPACIO para lanzar", True, TEXT_COL)
    screen.blit(txt, (W // 2 - txt.get_width() // 2, H // 2 + 105))


# =========================
# Inicialización
# =========================
ladrillos = crear_nivel(nivel)
reset_pelotas()

# =========================
# Bucle principal
# =========================
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if estado == "menu":
                if btn_start.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    reiniciar_partida()

                elif btn_controls.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "controles"

                elif btn_settings.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "configuracion"

                elif btn_quit.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    pygame.quit()
                    sys.exit()

            elif estado == "controles":
                if btn_exit_sub.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "menu"

            elif estado == "configuracion":
                if btn_exit_sub.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "menu"

            elif estado == "game_over":
                if btn_back_menu.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "menu"

            elif estado == "felicitaciones":
                if btn_next_level.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    pasar_siguiente_nivel()

                elif btn_win_menu.collidepoint(event.pos):
                    reproducir_sonido(SND_MENU)
                    estado = "menu"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and estado == "ready":
                reproducir_sonido(SND_MENU)
                estado = "playing"

            elif event.key == pygame.K_RETURN and estado == "life_lost":
                reproducir_sonido(SND_MENU)
                reset_pelotas()
                estado = "ready"

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

    if estado == "felicitaciones":
        dibujar_felicitaciones()
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        pad_x -= 5

    if keys[pygame.K_RIGHT] or keys[pygame.K_b]:
        pad_x += 5

    pad_x = max(PAD_W // 2, min(W - PAD_W // 2, pad_x))

    if estado == "ready":
        pelotas[0]["x"] = float(pad_x)
        pelotas[0]["y"] = float(PAD_Y - BALL_R - 2)

    if estado == "playing":
        actualizar_powerups()

        for pelota in pelotas[:]:
            prev_ball_x = pelota["x"]
            prev_ball_y = pelota["y"]

            pelota["x"] += pelota["dx"]
            pelota["y"] += pelota["dy"]

            if pelota["x"] - BALL_R <= 0:
                pelota["x"] = BALL_R
                pelota["dx"] = abs(pelota["dx"])

            if pelota["x"] + BALL_R >= W:
                pelota["x"] = W - BALL_R
                pelota["dx"] = -abs(pelota["dx"])

            if pelota["y"] - BALL_R <= 0:
                pelota["y"] = BALL_R
                pelota["dy"] = abs(pelota["dy"])

            if (
                PAD_Y <= pelota["y"] + BALL_R <= PAD_Y + PAD_H
                and pad_x - PAD_W // 2 <= pelota["x"] <= pad_x + PAD_W // 2
                and pelota["dy"] > 0
            ):
                reproducir_sonido(SND_PALETA)
                rel = (pelota["x"] - pad_x) / (PAD_W / 2)
                pelota["dx"] = rel * 5
                pelota["dy"] = -abs(pelota["dy"])
                pelota["y"] = PAD_Y - BALL_R - 1

            ball_rect = pygame.Rect(
                int(pelota["x"] - BALL_R),
                int(pelota["y"] - BALL_R),
                BALL_R * 2,
                BALL_R * 2
            )

            for ladrillo in ladrillos:
                if not ladrillo["activo"]:
                    continue

                if ball_rect.colliderect(ladrillo["rect"]):
                    reproducir_sonido(SND_LADRILLO)

                    ladrillo["vida"] -= 1

                    if ladrillo["vida"] <= 0:
                        ladrillo["activo"] = False
                        score += ladrillo["puntos"]

                        intentar_lanzar_powerup(
                            ladrillo["rect"].centerx,
                            ladrillo["rect"].centery
                        )
                    else:
                        ladrillo["color"] = oscurecer_color(ladrillo["color"])

                    pelota["x"] = prev_ball_x
                    pelota["y"] = prev_ball_y

                    if (
                        prev_ball_y + BALL_R <= ladrillo["rect"].top
                        or prev_ball_y - BALL_R >= ladrillo["rect"].bottom
                    ):
                        pelota["dy"] = -pelota["dy"]
                    else:
                        pelota["dx"] = -pelota["dx"]

                    break

            if pelota["y"] - BALL_R > H:
                pelotas.remove(pelota)

        if nivel_completado():
            reproducir_sonido(SND_WIN)
            estado = "felicitaciones"

        if len(pelotas) == 0:
            vidas -= 1

            if vidas <= 0:
                reproducir_sonido(SND_GAME_OVER)
                estado = "game_over"
            else:
                reproducir_sonido(SND_VIDA)
                estado = "life_lost"

    draw_pattern_background()

    for ladrillo in ladrillos:
        if ladrillo["activo"]:
            pygame.draw.rect(
                screen,
                ladrillo["color"],
                ladrillo["rect"],
                border_radius=2
            )

            if ladrillo["vida_max"] > 1:
                pygame.draw.rect(
                    screen,
                    (230, 245, 255),
                    ladrillo["rect"],
                    width=1,
                    border_radius=2
                )

    dibujar_powerups()

    pygame.draw.rect(
        screen,
        PAD_COL,
        (pad_x - PAD_W // 2, PAD_Y, PAD_W, PAD_H),
        border_radius=5
    )

    for pelota in pelotas:
        pygame.draw.circle(
            screen,
            BALL_COL,
            (int(pelota["x"]), int(pelota["y"])),
            BALL_R
        )

    dibujar_vidas()
    dibujar_hud()

    if estado == "ready":
        dibujar_mensaje_ready()

    if estado == "life_lost":
        dibujar_aviso_vida_perdida()

    pygame.display.flip()