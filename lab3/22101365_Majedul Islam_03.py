import math
import random

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Game state variables
player_pos = [0, 0, 0]
gun_yaw = 0
bullets = []
enemies = []
camera_mode = "third"
cheat_mode = False
auto_follow = False
life = 5
score = 0
bullets_missed = 0
game_over = False
enemy_speed = 0.5
bullet_speed = 5

# Camera settings
camera_pos = (0, 500, 500)
camera_angle = 0
fovY = 120
GRID_LENGTH = 600
enemy_pulse = 0.0


def reset_game():
    global player_pos, gun_yaw, bullets, enemies, life, score, bullets_missed, game_over
    player_pos = [0, 0, 0]
    gun_yaw = 0
    bullets = []
    enemies = [
        [random.randint(-400, 400), random.randint(-400, 400), 0] for _ in range(5)
    ]
    life = 5
    score = 0
    bullets_missed = 0
    game_over = False


def draw_player():
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])

    # Body (cuboid)
    glColor3f(0.2, 0.5, 1.0)
    glPushMatrix()
    glTranslatef(0, 0, 30)
    glScalef(30, 30, 60)
    glutSolidCube(1)
    glPopMatrix()

    # Head (sphere)
    glColor3f(1, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 0, 75)
    glutSolidSphere(20, 20, 20)
    glPopMatrix()

    # Gun (rotates around Z-axis)
    glPushMatrix()
    glRotatef(gun_yaw, 0, 0, 1)  # Rotate around Z-axis
    glTranslatef(40, 0, 30)  # Move to gun position
    glColor3f(0.3, 0.3, 0.3)
    glRotatef(90, 0, 1, 0)  # Orient gun horizontally
    gluCylinder(gluNewQuadric(), 5, 5, 80, 10, 10)
    glPopMatrix()

    glPopMatrix()


def draw_enemy(x, y, z, scale):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(scale, scale, scale)

    # Red base sphere
    glColor3f(1, 0, 0)
    glutSolidSphere(20, 20, 20)

    # Black top sphere
    glColor3f(0, 0, 0)
    glTranslatef(0, 0, 30)
    glutSolidSphere(15, 20, 20)

    glPopMatrix()


def draw_bullet(x, y, z):
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(1, 1, 0)
    glutSolidCube(10)
    glPopMatrix()


def draw_boundaries():
    glColor3f(0.5, 0.5, 0.5)
    height = 50
    # Left boundary
    glPushMatrix()
    glTranslatef(-GRID_LENGTH, 0, height / 2)
    glScalef(10, GRID_LENGTH * 2, height)
    glutSolidCube(1)
    glPopMatrix()
    # Right boundary
    glPushMatrix()
    glTranslatef(GRID_LENGTH, 0, height / 2)
    glScalef(10, GRID_LENGTH * 2, height)
    glutSolidCube(1)
    glPopMatrix()
    # Front boundary
    glPushMatrix()
    glTranslatef(0, GRID_LENGTH, height / 2)
    glScalef(GRID_LENGTH * 2, 10, height)
    glutSolidCube(1)
    glPopMatrix()
    # Back boundary
    glPushMatrix()
    glTranslatef(0, -GRID_LENGTH, height / 2)
    glScalef(GRID_LENGTH * 2, 10, height)
    glutSolidCube(1)
    glPopMatrix()


def keyboardListener(key, x, y):
    global gun_yaw, cheat_mode, auto_follow, game_over, player_pos
    key = key.decode("utf-8").lower()

    if game_over and key == "r":
        reset_game()
        return

    if key == "a":
        gun_yaw += 5
    elif key == "d":
        gun_yaw -= 5
    elif key == "w":
        rad = math.radians(gun_yaw)
        player_pos[0] += 10 * math.sin(rad)
        player_pos[1] += 10 * math.cos(rad)
    elif key == "s":
        rad = math.radians(gun_yaw)
        player_pos[0] -= 10 * math.sin(rad)
        player_pos[1] -= 10 * math.cos(rad)
    elif key == "c":
        cheat_mode = not cheat_mode
    elif key == "v" and cheat_mode:
        auto_follow = not auto_follow


def specialKeyListener(key, x, y):
    global camera_pos, camera_angle
    dx, dy, dz = camera_pos

    if key == GLUT_KEY_UP:
        dz += 10
    elif key == GLUT_KEY_DOWN:
        dz -= 10
    elif key == GLUT_KEY_LEFT:
        camera_angle += 2
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 2

    # Update camera position based on angle
    radius = math.hypot(camera_pos[0], camera_pos[1])
    rad = math.radians(camera_angle)
    new_x = radius * math.sin(rad)
    new_y = radius * math.cos(rad)
    camera_pos = (new_x, new_y, dz)


def mouseListener(button, state, x, y):
    global camera_mode
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN and not game_over:
        rad = math.radians(gun_yaw)
        print("Player Bullet fired!")  # Add this line
        # Calculate bullet start position at gun tip
        bullet_x = player_pos[0] + (80 + 40) * math.cos(
            rad
        )  # 80 (barrel) + 40 (offset)
        bullet_y = player_pos[1] + (80 + 40) * math.sin(rad)
        bullets.append(
            {
                "x": bullet_x,
                "y": bullet_y,
                "z": 50,
                "dir": math.cos(rad),  # Correct direction
                "dir_y": math.sin(rad),
            }
        )
    elif button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        camera_mode = "first" if camera_mode == "third" else "third"


def update_enemies():
    global enemies, life, game_over
    for i in range(len(enemies)):
        ex, ey, ez = enemies[i]
        dx = player_pos[0] - ex
        dy = player_pos[1] - ey
        dist = math.hypot(dx, dy)
        if dist == 0:
            continue
        ex += dx / dist * enemy_speed
        ey += dy / dist * enemy_speed
        enemies[i] = [ex, ey, ez]

        # Check collision with player
        if math.hypot(player_pos[0] - ex, player_pos[1] - ey) < 50 and not game_over:
            life -= 1
            print(f"Remaining player life: {life}")  # Add this line
            if life <= 0:
                print(
                    f"GAME OVER! Final Score: {score}, Bullets Missed: {bullets_missed}"
                )
                game_over = True
            enemies[i] = [random.randint(-400, 400), random.randint(-400, 400), 0]


def update_bullets():
    global bullets, bullets_missed, score
    new_bullets = []
    for b in bullets:
        # Move bullet in facing direction
        b["x"] += b["dir"] * bullet_speed
        b["y"] += b["dir_y"] * bullet_speed
        b["z"] += 1  # Slight upward arc

        # Check boundaries
        if abs(b["x"]) > 600 or abs(b["y"]) > 600:
            bullets_missed += 1
            continue
        # Check enemy hits
        hit = False
        for i in range(len(enemies)):
            ex, ey, ez = enemies[i]
            if math.hypot(b["x"] - ex, b["y"] - ey) < 30:
                score += 10
                enemies[i] = [random.randint(-400, 400), random.randint(-400, 400), 0]
                hit = True
                break
        if not hit:
            new_bullets.append(b)
        else:
            bullets_missed = max(0, bullets_missed - 1)  # Compensate for hit
    bullets = new_bullets


def setupCamera():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == "first":
        # First-person view follows gun direction
        rad = math.radians(gun_yaw)
        cam_x = player_pos[0] - 100 * math.sin(rad)
        cam_y = player_pos[1] - 100 * math.cos(rad)
        cam_z = player_pos[2] + 50
        look_x = player_pos[0] + 200 * math.sin(rad)
        look_y = player_pos[1] + 200 * math.cos(rad)
        gluLookAt(cam_x, cam_y, cam_z, look_x, look_y, 50, 0, 0, 1)
    else:
        # Third-person view remains unchanged
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 0, 1)


def showScreen():
    global enemy_pulse
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)

    setupCamera()

    cell_size = 100  # Size of each grid cell
    color1 = (0.7, 0.7, 0.7)  # Light gray
    color2 = (0.4, 0.4, 0.4)  # Dark gray

    glBegin(GL_QUADS)
    for i in range(-GRID_LENGTH, GRID_LENGTH, cell_size):
        for j in range(-GRID_LENGTH, GRID_LENGTH, cell_size):
            # Alternate colors based on grid position
            if ((i + j) // cell_size) % 2 == 0:
                glColor3f(*color1)
            else:
                glColor3f(*color2)

            # Draw grid cell
            glVertex3f(i, j, 0)
            glVertex3f(i + cell_size, j, 0)
            glVertex3f(i + cell_size, j + cell_size, 0)
            glVertex3f(i, j + cell_size, 0)
    glEnd()

    draw_boundaries()

    # Draw player
    if not game_over:
        draw_player()
    else:
        # Game Over display
        glColor3f(1, 0, 0)
        draw_text(400, 400, "GAME OVER", GLUT_BITMAP_TIMES_ROMAN_24)
        draw_text(380, 370, f"Your score is: {score}", GLUT_BITMAP_HELVETICA_18)
        draw_text(350, 340, "Press R to restart", GLUT_BITMAP_HELVETICA_18)

    # Draw enemies with pulsation
    enemy_pulse = (enemy_pulse + 0.05) % (2 * math.pi)
    scale = 1 + 0.2 * math.sin(enemy_pulse)
    for e in enemies:
        draw_enemy(e[0], e[1], e[2], scale)

    # Draw bullets
    for b in bullets:
        draw_bullet(b["x"], b["y"], b["z"])

    # HUD
    draw_text(10, 770, f"Life: {life}  Score: {score}  Missed: {bullets_missed}")
    if cheat_mode:
        draw_text(10, 740, "CHEAT MODE ACTIVE")

    glutSwapBuffers()


def find_nearest_enemy():
    nearest = None
    min_dist = float("inf")
    for enemy in enemies:
        dx = enemy[0] - player_pos[0]
        dy = enemy[1] - player_pos[1]
        dist = math.hypot(dx, dy)
        if dist < min_dist:
            min_dist = dist
            nearest = enemy
    return nearest


cheat_shot_cooldown = 0
COOLDOWN_FRAMES = 30  # Half second at 60 FPS
TARGET_ANGLE_THRESHOLD = 5  # Degrees


def idle():
    global game_over, cheat_shot_cooldown
    if game_over:
        return

    # Improved cheat mode with precision shooting
    if cheat_mode:
        global gun_yaw
        nearest_enemy = find_nearest_enemy()

        if nearest_enemy:
            # Calculate direction to enemy
            dx = nearest_enemy[0] - player_pos[0]
            dy = nearest_enemy[1] - player_pos[1]
            target_angle = math.degrees(math.atan2(dy, dx))

            # Calculate angle difference with wrapping
            angle_diff = (target_angle - gun_yaw + 180) % 360 - 180

            # Smooth rotation towards target
            gun_yaw += angle_diff * 0.3  # Faster rotation

            # Handle cooldown and shooting
            if cheat_shot_cooldown > 0:
                cheat_shot_cooldown -= 1
            elif abs(angle_diff) < TARGET_ANGLE_THRESHOLD:
                # Fire precise shot
                rad = math.radians(gun_yaw)
                bullets.append(
                    {
                        "x": player_pos[0] + 120 * math.cos(rad),
                        "y": player_pos[1] + 120 * math.sin(rad),
                        "z": 50,
                        "dir": math.cos(rad),
                        "dir_y": math.sin(rad),
                    }
                )
                cheat_shot_cooldown = COOLDOWN_FRAMES
                print("Precision cheat shot fired!")

    update_enemies()
    update_bullets()

    if bullets_missed >= 10:
        print(f"GAME OVER! Final Score: {score}, Bullets Missed: {bullets_missed}")
        game_over = True

    glutPostRedisplay()


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glColor3f(1, 1, 1)
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutCreateWindow(b"Bullet Frenzy")
    glEnable(GL_DEPTH_TEST)
    reset_game()

    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)

    glutMainLoop()


if __name__ == "__main__":
    main()
