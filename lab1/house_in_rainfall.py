import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Global variables
rain_direction = 0.0
house_color = [0.3, 0.2, 0.1]
bg_color = [0.0392, 0.0392, 0.0392]
target_house_color = house_color.copy()
target_bg_color = bg_color.copy()
raindrops = []


def init():
    glClearColor(*bg_color, 1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 500, 0, 500)
    glMatrixMode(GL_MODELVIEW)

    for _ in range(200):
        raindrops.append({"x": random.uniform(0, 500), "y": random.uniform(0, 500)})


def draw_house():
    glColor3f(*house_color)
    glBegin(GL_LINES)
    glVertex2f(200, 200)
    glVertex2f(300, 200)
    glVertex2f(300, 200)
    glVertex2f(300, 300)
    glVertex2f(300, 300)
    glVertex2f(200, 300)
    glVertex2f(200, 300)
    glVertex2f(200, 200)
    glEnd()

    door_width = 40
    door_height = 80
    door_x = 250 - door_width / 2
    door_top = 200 + door_height

    glColor3f(0.4, 0.2, 0.0)
    glBegin(GL_LINES)
    glVertex2f(door_x, 200)
    glVertex2f(door_x, door_top)
    glVertex2f(door_x + door_width, 200)
    glVertex2f(door_x + door_width, door_top)
    glVertex2f(door_x, door_top)
    glVertex2f(door_x + door_width, door_top)
    glVertex2f(door_x + door_width - 10, 200 + door_height / 2)
    glVertex2f(door_x + door_width - 5, 200 + door_height / 2)
    glEnd()

    glColor3f(*house_color)
    glBegin(GL_TRIANGLES)
    glVertex2f(180, 300)
    glVertex2f(320, 300)
    glVertex2f(250, 350)
    glEnd()


def draw_rain():
    glColor3f(0.8, 0.9, 1.0)
    glBegin(GL_LINES)
    for drop in raindrops:
        glVertex2f(drop["x"], drop["y"])
        glVertex2f(drop["x"] + rain_direction, drop["y"] - 10)
    glEnd()


def update_rain():
    for drop in raindrops:
        drop["x"] += rain_direction * 0.1
        drop["y"] -= 5

        if drop["y"] < 0:
            drop["y"] = 500
            drop["x"] = random.uniform(0, 500)


def interpolate_colors():
    global house_color, bg_color
    speed = 0.02
    for i in range(3):
        house_color[i] += (target_house_color[i] - house_color[i]) * speed
        bg_color[i] += (target_bg_color[i] - bg_color[i]) * speed
    glClearColor(*bg_color, 1.0)


def keyboard(key, x, y):
    global target_house_color, target_bg_color
    if key == b"d":
        target_house_color = [0.9, 0.8, 0.7]
        target_bg_color = [0.53, 0.81, 0.98]
    elif key == b"n":
        target_house_color = [0.3, 0.2, 0.1]
        target_bg_color = [0.0392, 0.0392, 0.0392]
    glutPostRedisplay()


def special_keys(key, x, y):
    global rain_direction
    if key == GLUT_KEY_LEFT:
        rain_direction -= 0.5
    elif key == GLUT_KEY_RIGHT:
        rain_direction += 0.5
    rain_direction = max(-20, min(20, rain_direction))


def animate(value):
    update_rain()
    interpolate_colors()
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_house()
    draw_rain()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutCreateWindow(b"Rainy House")
init()

# Register callbacks
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(0, animate, 0)
glutMainLoop()
