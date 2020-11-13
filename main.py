import sys
import math
import random
import pygame

pygame.init()

# --------------------------------------------------------
#                       Variables
# --------------------------------------------------------

# Screen
size = (800, 600)
screen = pygame.display.set_mode(size)

# Background Menu
background_menu = pygame.image.load('images/background_menu.png')

# Background Game
background = pygame.image.load('images/background_game.png')

# Menu
start_button = pygame.image.load('images/button_start.png').convert_alpha()
start_button_pos = (size[0]/4.0 - start_button.get_width()/2.0, size[1]*0.5 - start_button.get_height()/2.0)

sound_button = [
    pygame.image.load('images/sound_on.png').convert_alpha(),
    pygame.image.load('images/sound_on.png').convert_alpha()
    ]
sound_button_pos = (715, 0)
sound_button_index = 1

# Sound
sound = "sound/game_song.ogg"
pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load(sound)
pygame.mixer.music.play(-1)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 625
playerY = 40
playerX_change = 0
playerY_change = 0

# Enemies
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

# Score
score_value = 100
textX = 10
testY = 10

# Font
font = pygame.font.Font('freesansbold.ttf', 32)


# --------------------------------------------------------
#                       Methods
# --------------------------------------------------------

def validate_click(mouse_pos, target_surface, target_pos):
    return mouse_pos[0] >= target_pos[0] and mouse_pos[0] <= target_pos[0] + target_surface.get_rect()[2] and \
           mouse_pos[1] >= target_pos[1] and mouse_pos[1] <= target_pos[1] + target_surface.get_rect()[3]


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def show_player(x, y):
    screen.blit(playerImg, (x, y))


def show_enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    if distance < 27:
        return True
    else:
        return False


def create_enemies():
    for enemy in range(num_of_enemies):
        enemyImg.append(pygame.image.load('images/ghost.png'))
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_change.append(4)
        enemyY_change.append(40)


# --------------------------------------------------------
#                       Menu
# --------------------------------------------------------
show_menu = True
local_sound_flag = True
while show_menu:

    # Background
    screen.fill((0, 0, 0))
    screen.blit(background_menu, (0, 0))

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Click Position Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Validate Click in Start Button
            if validate_click(mouse_pos, start_button, start_button_pos):
                show_menu = False

            # Validate Click in Sound Button
            if validate_click(mouse_pos, sound_button[sound_button_index], sound_button_pos):
                sound_button_index = (sound_button_index + 1) % 2
                local_sound_flag = not local_sound_flag
                if not local_sound_flag:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.load(sound)
                    pygame.mixer.music.play(-1, 0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(start_button, start_button_pos)
    screen.blit(sound_button[sound_button_index], sound_button_pos)

    pygame.display.update()


# --------------------------------------------------------
#                       Game Loop
# --------------------------------------------------------
create_enemies()
running = True
while running:

    # Background Image with black ground
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Click Position Mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Validate Click in Sound Button
            if validate_click(mouse_pos, sound_button[sound_button_index], sound_button_pos):
                sound_button_index = (sound_button_index + 1) % 2
                local_sound_flag = not local_sound_flag
                if not local_sound_flag:
                    pygame.mixer.music.stop()
                else:
                    pygame.mixer.music.load(sound)
                    pygame.mixer.music.play(-1, 0)

        # if keystroke is pressed check whether its right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_UP:
                playerY_change = -5
            if event.key == pygame.K_DOWN:
                playerY_change = 5

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    playerY += playerY_change
    if playerY <= 0:
        playerY = 0
    elif playerY >= 736:
        playerY = 736

    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        show_enemy(enemyX[i], enemyY[i], i)

        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            score_value -= 1

    screen.blit(sound_button[sound_button_index], sound_button_pos)
    show_player(playerX, playerY)
    show_score(textX, testY)

    pygame.display.update()
