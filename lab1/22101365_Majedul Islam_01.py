import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# TASK 01

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
glutCreateWindow(b"House In a Rainfall")
init()


glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keys)
glutTimerFunc(0, animate, 0)
glutMainLoop()


# TASK 02

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
wind = glutCreateWindow(b"Amazing Box")
glutDisplayFunc(show_screen)
glutIdleFunc(animate)
glutSpecialFunc(handle_special_keys)
glutKeyboardFunc(handle_normal_keys)
glutMouseFunc(mouse_click)
glutMainLoop()
