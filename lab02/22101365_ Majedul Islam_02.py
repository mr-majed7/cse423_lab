import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# catcher
x1, x2, x3, x4 = 20, 50, 135, 165
y1, y2 = 10, 30
catcher_width = x4 - x1
catcher_height = y2 - y1
catcher_speed = 10

# catcher color set
white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
catcher_color = white
# Diamond
diamond_colors = [
    (1.0, 0.0, 0.0),  # Red
    (0.0, 1.0, 0.0),  # Green
    (0.0, 0.0, 1.0),  # Blue
    (1.0, 1.0, 0.0),  # Yellow
    (1.0, 0.0, 1.0),  # Purple
]

diamond_arr = []
falling_diamonds = None
diamond_speed = 2
# score
score = 0
# window size
window_width = 600
window_height = 900
# Status Flags
pause_flag = False  # pause flag
gameover_flag = False  # game over flag
restarted_flag = False  # restart flag


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()


def find_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    zone = -1
    if abs(dx) > abs(dy):
        if dx > 0:
            if dy > 0:
                zone = 0
            else:
                zone = 7
        else:
            if dy > 0:
                zone = 3
            else:
                zone = 4
    else:
        if dy > 0:
            if dx > 0:
                zone = 1
            else:
                zone = 2
        else:
            if dx > 0:
                zone = 6
            else:
                zone = 5
    return zone


def convert(original_zone, x, y):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return -y, x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return -y, x
    elif original_zone == 7:
        return x, -y


def convert_original(original_zone, x, y):
    if original_zone == 0:
        return x, y
    elif original_zone == 1:
        return y, x
    elif original_zone == 2:
        return -y, -x
    elif original_zone == 3:
        return -x, y
    elif original_zone == 4:
        return -x, -y
    elif original_zone == 5:
        return -y, -x
    elif original_zone == 6:
        return y, -x
    elif original_zone == 7:
        return x, -y


def midpoint(zone, x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    d = (2 * dy) - dx
    forE = 2 * dy
    forNE = 2 * (dy - dx)
    x = x0
    y = y0
    while x < x1:
        org_x, org_y = convert_original(zone, x, y)
        draw_points(org_x, org_y)
        if d <= 0:
            x += 1
            d += forE
        else:
            x += 1
            y += 1
            d += forNE


def draw_catcher():
    global x1, x2, x3, x4, y1, y2
    glColor3fv(catcher_color)
    eight_way_symmetry(x2, y1, x3, y1)
    eight_way_symmetry(x1, y2, x2, y1)
    eight_way_symmetry(x3, y1, x4, y2)
    eight_way_symmetry(x1, y2, x4, y2)


def eight_way_symmetry(x0, y0, x1, y1):
    zone = find_zone(x0, y0, x1, y1)
    conv_x0, conv_y0 = convert(zone, x0, y0)
    conv_x1, conv_y1 = convert(zone, x1, y1)
    midpoint(zone, conv_x0, conv_y0, conv_x1, conv_y1)


def left_arrow():
    glColor3f(0.0, 1.0, 1.0)
    eight_way_symmetry(20, 850, 100, 850)
    eight_way_symmetry(40, 855, 20, 850)
    eight_way_symmetry(40, 845, 20, 850)


def cross():
    glColor3f(1.0, 0.0, 0.0)
    eight_way_symmetry(500, 840, 575, 880)
    eight_way_symmetry(500, 880, 575, 840)


def play():
    glColor3f(1.0, 1.0, 0.0)
    eight_way_symmetry(297, 870, 297, 820)
    eight_way_symmetry(303, 870, 303, 820)


def pause():
    glColor3f(1.0, 1.0, 0.0)
    eight_way_symmetry(297, 870, 297, 820)
    eight_way_symmetry(297, 870, 310, 845)
    eight_way_symmetry(297, 820, 310, 845)


def animation():
    global pause_flag, gameover_flag
    if pause_flag == False and gameover_flag == False:
        glutPostRedisplay()


def iterate():
    glViewport(0, 0, 600, 900)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 600, 0.0, 900, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def specialKeyListener(key, x, y):
    global x1, x2, x3, x4, catcher_speed, pause_flag
    if pause_flag == False:
        if key == GLUT_KEY_RIGHT:
            if (x1 < 600) and (x2 <= 600) and (x3 < 600) and (x4 < 600):
                x1 += catcher_speed
                x2 += catcher_speed
                x3 += catcher_speed
                x4 += catcher_speed
        if key == GLUT_KEY_LEFT:
            if (x1 > 0) and (x2 > 0) and (x3 > 0) and (x4 > 0):
                x1 -= catcher_speed
                x2 -= catcher_speed
                x3 -= catcher_speed
                x4 -= catcher_speed
    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global pause_flag, x1, x2, x3, x4, score, restarted_flag, gameover_flag
    new_y = window_height - y
    if (button == GLUT_LEFT_BUTTON) and (state == GLUT_DOWN):
        # pause
        if (297 <= x <= 310) and (820 <= new_y <= 870):
            pause_flag = not pause_flag  # Toggle pause state
            if pause_flag:
                print(f"Pause Score: {score}")
        # restart
        if (20 <= x <= 100) and (845 <= new_y <= 855):
            restarted_flag = True
            print("Starting over")
        # terminate
        if (500 <= x <= 575) and (840 <= new_y <= 880):
            print(f"Goodbye! Score: {score}")
            glutLeaveMainLoop()


def create_diamond():
    diamond_y = 800
    diamond_x = random.randint(25, 525)
    diamond_color = random.choice(diamond_colors)
    diamond_arr.append([diamond_x, diamond_y, diamond_color])


def draw_diamond(x, y, color):
    glColor3fv(color)
    eight_way_symmetry(x, y, x + 10, y + 10)
    eight_way_symmetry(x - 10, y + 10, x, y)
    eight_way_symmetry(x, y + 20, x + 10, y + 10)
    eight_way_symmetry(x, y + 20, x - 10, y + 10)


def update(value):
    global score, catcher_color, x1, x2, x3, x4, y1, y2, gameover_flag, restarted_flag, pause_flag, falling_diamonds, diamond_speed, catcher_speed
    bar_x = (x1 + x4) / 2
    if restarted_flag == True:
        score = 0
        catcher_color = white
        x1 = 20
        x2 = 50
        x3 = 135
        x4 = 165
        gameover_flag = False
        diamond_arr.clear()
        diamond_speed = 2
        catcher_speed = 10
        falling_diamonds = None  # Reset the falling diamond
        for i in range(10):
            create_diamond()
            glutDisplayFunc(showScreen)
        restarted_flag = False
    elif not gameover_flag and not pause_flag:
        if not falling_diamonds:
            if diamond_arr:
                falling_diamonds = diamond_arr.pop(0)
        if falling_diamonds:
            diamond_x, diamond_y, diamond_color = falling_diamonds
            diamond_y -= diamond_speed
            falling_diamonds = [diamond_x, diamond_y, diamond_color]
            if (diamond_y <= catcher_height) and (
                abs(diamond_x - bar_x) < catcher_width / 2
            ):
                score += 1
                print(f"Score: {score}")
                falling_diamonds = None
                diamond_speed += 0.1
                catcher_speed += 0.5
                create_diamond()
            elif diamond_y < 0:
                gameover_flag = True
                falling_diamonds = None
                catcher_color = red
                if gameover_flag == True:
                    pause_flag = True
                    catcher_color = red
                    print(f"Game Over! Your final score is {score}")
    glutPostRedisplay()
    glutTimerFunc(10, update, 0)


def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_catcher()
    left_arrow()
    cross()
    if falling_diamonds:
        xi, yi, color = falling_diamonds
        draw_diamond(xi, yi, color)

    if pause_flag == True:
        pause()
    if pause_flag == False:
        play()
    glutSwapBuffers()


for i in range(10):
    create_diamond()
glutInit()


glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(1100, 0)
glutCreateWindow(b"Catch the Diamonds!")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)
glutIdleFunc(animation)
glutTimerFunc(10, update, 0)
glutMainLoop()
