import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

points = []
blinking_active = False
freeze = False


def draw_points(x, y):
    glPointSize(5)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def update_points():
    global points
    for point in points:
        dx = point["dx"]
        dy = point["dy"]
        speed = point["speed"]
        new_x = point["x"] + dx * speed
        new_y = point["y"] + dy * speed

        if new_x < 0:
            overshoot = -new_x
            new_x = 0 + overshoot
            dx *= -1
        elif new_x > 500:
            overshoot = new_x - 500
            new_x = 500 - overshoot
            dx *= -1

        if new_y < 0:
            overshoot = -new_y
            new_y = 0 + overshoot
            dy *= -1
        elif new_y > 500:
            overshoot = new_y - 500
            new_y = 500 - overshoot
            dy *= -1

        point["x"] = new_x
        point["y"] = new_y
        point["dx"] = dx
        point["dy"] = dy


def show_screen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    if not freeze:
        update_points()
    current_time = glutGet(GLUT_ELAPSED_TIME)
    for point in points:
        if blinking_active:
            if (current_time // 500) % 2 == 0:
                glColor3f(point["r"], point["g"], point["b"])
            else:
                glColor3f(0, 0, 0)
        else:
            glColor3f(point["r"], point["g"], point["b"])
        draw_points(point["x"], point["y"])
    glutSwapBuffers()


def handle_special_keys(key, x, y):
    global points, freeze
    if freeze:
        return
    if key == GLUT_KEY_UP:
        for point in points:
            point["speed"] *= 1.1
    elif key == GLUT_KEY_DOWN:
        for point in points:
            point["speed"] *= 0.9
    glutPostRedisplay()


def handle_normal_keys(key, x, y):
    global freeze
    if key == b" ":
        freeze = not freeze
    glutPostRedisplay()


def mouse_click(button, state, x, y):
    global points, freeze, blinking_active
    if freeze:
        return
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        x_ortho = x
        y_ortho = 500 - y
        r = random.random()
        g = random.random()
        b = random.random()
        dx = random.choice([-1, 1])
        dy = random.choice([-1, 1])
        speed = 0.1
        points.append(
            {
                "x": x_ortho,
                "y": y_ortho,
                "dx": dx,
                "dy": dy,
                "r": r,
                "g": g,
                "b": b,
                "speed": speed,
            }
        )
    elif button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        blinking_active = not blinking_active
    glutPostRedisplay()


def animate():
    if not freeze:
        glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(show_screen)
glutIdleFunc(animate)
glutSpecialFunc(handle_special_keys)
glutKeyboardFunc(handle_normal_keys)
glutMouseFunc(mouse_click)
glutMainLoop()
