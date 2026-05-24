# Arkanoid - Metodología de Desarrollo de Software

## 1. Descripción del proyecto

Este proyecto consiste en el desarrollo de un videojuego tipo **Arkanoid** usando **Python** y **pygame-ce**.

El jugador controla una plataforma ubicada en la parte inferior de la pantalla. El objetivo principal es evitar que la pelota caiga mientras se destruyen los ladrillos ubicados en la parte superior del escenario.

El proyecto fue desarrollado aplicando conceptos de metodología de desarrollo de software, control de versiones con Git, trabajo por ramas, commits asociados a historias de usuario y versionamiento mediante tags.

---

## 2. Objetivo del juego

El objetivo del juego es destruir todos los ladrillos del nivel usando una pelota que rebota en la plataforma, paredes y ladrillos.

El jugador pierde una vida cuando todas las pelotas caen por debajo de la pantalla. Si el contador de vidas llega a cero, la partida termina y se muestra la pantalla de **Game Over**.

---

## 3. Tecnologías utilizadas

- Python
- pygame-ce
- Visual Studio Code
- Git
- GitHub

---

## 4. Instalación

Para instalar las dependencias necesarias, ejecutar en la terminal:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` contiene la librería necesaria para ejecutar el juego:

```txt
pygame-ce
```

---

## 5. Ejecución del juego

Para ejecutar el juego desde la terminal:

```bash
py -3.14 Taller_Juego.py
```

También puede ejecutarse con:

```bash
python Taller_Juego.py
```

dependiendo de la configuración de Python instalada en el equipo.

---

## 6. Controles

| Acción | Control |
|---|---|
| Mover plataforma a la izquierda | Flecha izquierda o tecla A |
| Mover plataforma a la derecha | Flecha derecha o tecla B |
| Lanzar pelota | Barra espaciadora |
| Continuar después de perder vida | Enter |
| Navegar por menús | Click izquierdo |

---

## 7. Funcionalidades implementadas

### Jugabilidad principal

- Movimiento horizontal de la plataforma.
- Movimiento continuo de la pelota.
- Rebote en paredes laterales y techo.
- Rebote con control de ángulo sobre la plataforma.
- Colisión entre pelota y ladrillos.
- Sistema de ladrillos con diferente durabilidad.
- Sistema de múltiples pelotas.
- Pérdida de vida al caer todas las pelotas.

### Interfaz de usuario

- Menú principal.
- Pantalla de controles.
- Pantalla de configuración.
- Activación y desactivación de sonido.
- Pantalla de Game Over.
- Pantalla de Felicitaciones al completar nivel.
- Indicador de vidas mediante corazones.
- Contador de puntos y nivel.

### Progresión

- Nivel 1 con división central en la distribución de ladrillos.
- Múltiples niveles.
- Aumento de dificultad por nivel.
- Aumento progresivo de la velocidad de la pelota.
- Mayor cantidad de ladrillos resistentes en niveles superiores.

### Power-ups

- `WIDE`: aumenta el tamaño de la plataforma.
- `BIG`: aumenta el tamaño de la pelota.
- `MULTI`: genera múltiples pelotas.

---

## 8. Versiones del proyecto

### Release 1 - Tag `v1.0`

La primera versión corresponde al producto mínimo funcional del juego.

Incluye:

- Movimiento de plataforma.
- Movimiento de pelota.
- Rebote básico.
- Colisión con ladrillos.
- Menú inicial.
- Sistema de vidas.
- Contador de puntos.
- Nivel estático.
- Ladrillos con diferente durabilidad.

### Release 2 - Tag `v2.0`

La segunda versión agrega mejoras sobre el producto base.

Incluye:

- Sistema de colisiones avanzado.
- Efectos de sonido.
- Pantalla de Game Over mejorada.
- Pantalla de Felicitaciones.
- Detección de nivel completado.
- Múltiples niveles.
- Power-ups.
- Configuración para activar o silenciar sonido.
- Distribución visual mejorada del nivel 1.
- Sistema de múltiples pelotas.

---

## 9. Organización con Git y GitHub

El proyecto fue organizado siguiendo la estructura del Story Mapping.

La lógica usada fue:

```text
Rama = tarea del Story Mapping
Commit = historia de usuario implementada
Tag = versión o release del proyecto
```

Ejemplo:

```text
v1.0 = Release 1
v2.0 = Release 2
```

---

## 10. Ramas principales utilizadas

Algunas ramas usadas durante el desarrollo fueron:

```text
Jugabilidad_Mecanicas/controlar_paleta
Jugabilidad_Mecanicas/gestionar_pelota
Jugabilidad_Mecanicas/procesar_colisiones
Interfaz_Usuario/navegar_menus
Interfaz_Usuario/monitorear_estado
Progresion_Niveles/superar_niveles
Progresion_Niveles/obtener_mejoras
Jugabilidad_Mecanicas/procesar_colisiones_v2
Interfaz_Usuario/navegar_menus_v2
Progresion_Niveles/superar_niveles_v2
Progresion_Niveles/obtener_mejoras_v2
```

---

## 11. Historias implementadas

### Release 1

```text
TJ-19 Movimiento de paleta
TJ-20 Rebote de pelota en paredes
TJ-21 Rebote de pelota con control
TJ-22 Perímetro de colisión en paredes
TJ-23 Detección de colisión pelota-ladrillo
TJ-25 Menú de inicio
TJ-26 Detección de fin de partida al quedarse sin vidas
TJ-27 Indicador visual al perder vida
TJ-28 Contador de vidas y puntos
TJ-33 Un solo nivel estático
TJ-34 Ladrillos de diferente durabilidad
```

### Release 2

```text
TJ-24 Sistema de colisiones avanzado
TJ-31 Efectos de sonido
TJ-32 Pantalla de Game Over y Felicitaciones
TJ-35 Completar nivel al destruir todos los ladrillos
TJ-36 Múltiples niveles
TJ-37 Lanzamiento de Power-ups
TJ-37 Agregar power-up de múltiples pelotas
TJ-37 Configuración de sonido y distribución de nivel
```

---

## 12. Archivos principales del repositorio

| Archivo | Descripción |
|---|---|
| `Taller_Juego.py` | Código principal del videojuego |
| `README.md` | Documentación general del proyecto |
| `requirements.txt` | Dependencias necesarias para ejecutar el juego |
| `.gitignore` | Archivos y carpetas que Git debe ignorar |

---

## 13. Estado final del proyecto

El proyecto final cuenta con una versión funcional de Arkanoid, con menú, controles, vidas, puntos, niveles, sonidos, power-ups y versionamiento mediante Git y GitHub.

Este desarrollo corresponde a una entrega académica para la asignatura **Metodología de Desarrollo de Software**.