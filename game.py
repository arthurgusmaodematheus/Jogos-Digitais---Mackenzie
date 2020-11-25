import sys
import pygame
import random
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Game Project")

# --------------------------------------------------------
#                       Variables
# --------------------------------------------------------

# Screen
size = (800, 600)
screen = pygame.display.set_mode(size)

# Colors
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREY = (120, 120, 120)
BROWN = (145, 82, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 132, 0)

# Background Menu
background_menu = pygame.image.load('images/background_menu.png')

# Background Game
background = pygame.image.load('images/background_game.jpeg')

# Background GameOver
background_gameover = pygame.image.load('images/background_gameover.jpg')

# Background Success
background_success = pygame.image.load('images/background_success.jpg')

# Menu
start_button = pygame.image.load('images/button_start.png').convert_alpha()
start_button_pos = (size[0]/2.0 - start_button.get_width()/2.0, size[1]*0.7 - start_button.get_height()/2.0)

sound_button = [
    pygame.image.load('images/sound_on.png').convert_alpha(),
    pygame.image.load('images/sound_on.png').convert_alpha()
    ]
sound_button_pos = (715, -20)
sound_button_index = 1

# Sound
sound = "sounds/game_song.ogg"
pygame.mixer.init(44000, -16, 1, 1024)
pygame.mixer.music.load(sound)
pygame.mixer.music.play(-1)

gameover_sound = "sounds/game_over.wav"

# good_sound = "sounds/good_collision.wav"

success_game_sound = "sounds/success_game.wav"

# Player
player = [
    pygame.image.load('images/player_back1.png').convert_alpha(),
    pygame.image.load('images/player_back2.png').convert_alpha(),
    pygame.image.load('images/player_transparent.png').convert_alpha(),
    pygame.image.load('images/player_left1.png').convert_alpha(),
    pygame.image.load('images/player_right1.png').convert_alpha()
    ]

player_width, player_height = player[0].get_rect()[2], player[0].get_rect()[3]

player_pos = (size[0]/2.0 - player_width/2.0, size[1]*0.9 - player_height/2.0)

player_hitbox = [(player_pos[0] + player_width*0.15, player_pos[1] + player_height*0.2), player_width*0.7, player_height*0.6]

player_index = 0
player_mov = 0
player_speed = 4

player_curving = False

# Sidewalk
sidewalk = []

sidewalk_index = 0
sidewalk_width = background.get_rect()[2]
sidewalk_height = size[1]*2/3.0
sidewalk_left_edge = (size[0] - sidewalk_width)/2.0
sidewalk_right_edge = sidewalk_left_edge + sidewalk_width
sidewalk_pos = sidewalk_left_edge, size[1]-sidewalk_height
sidewalk_color = GREY

# Enemies
enemyImg = pygame.image.load('images/npc.png')
enemyX = 0
enemyY = 0
enemy_speed = 3.5

# Mask
maskImg = pygame.image.load('images/mask.png')
maskX = 0
maskY = 0
mask_speed = 3.5

# Hand Sanitizer
hand_sanitizerImg = pygame.image.load('images/hand_sanitizer.png')
hand_sanitizerX = 0
hand_sanitizerY = 0
hand_sanitizer_speed = 3.5

# Score
score_value = 0
scoreX = 10
scoreY = 50

# Lives
lives_value = 3
livesX = 10
livesY = 10

# Font
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)

# Variável para contagem de tempo, utilizado para controlar a velocidade de quadros (de atualizações da tela)
clock = pygame.time.Clock()

#criando objeto Clock
CLOCKTICK = pygame.USEREVENT+1
pygame.time.set_timer(CLOCKTICK, 1000) # configurado o timer do Pygame para execução a cada 1 segundo
temporizador = 120


# --------------------------------------------------------
#                       Functions
# --------------------------------------------------------

def validate_click(mouse_pos, target_surface, target_pos):
    return (mouse_pos[0] >= target_pos[0] and mouse_pos[0] <= target_pos[0] + target_surface.get_rect()[2] and \
            mouse_pos[1] >= target_pos[1] and mouse_pos[1] <= target_pos[1] + target_surface.get_rect()[3])


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, YELLOW)
    screen.blit(score, (x, y))


def show_lives(x, y):
    lives = font.render("Lives : " + str(lives_value), True, YELLOW)
    screen.blit(lives, (x, y))


def game_over():
    over_text = over_font.render("GAME OVER", True, WHITE)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(gameover_sound)
    pygame.mixer.music.play(-1, 0)
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_gameover, (0, 0))
        screen.blit(over_text, (200, 270))
        pygame.display.update()


def success_game():
    score = font.render("Score : " + str(score_value), True, BLACK)
    pygame.mixer.music.stop()
    pygame.mixer.music.load(success_game_sound)
    pygame.mixer.music.play(-1, 0)
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(background_success, (0, 0))
        screen.blit(score, (300, 500))
        pygame.display.update()


# --------------------------------------------------------
#                       Menu
# --------------------------------------------------------
show_menu = True
local_sound_flag = True
while show_menu:

    # Background
    screen.fill(BLACK)
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

    # Show in Screen
    screen.blit(start_button, start_button_pos)
    screen.blit(sound_button[sound_button_index], sound_button_pos)

    pygame.display.update()

# --------------------------------------------------------
#                       Game Loop
# --------------------------------------------------------
create_enemy = True
create_mask = True
create_hand_sanitizer = True
running = True
while running:

    # Background Image with black ground
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # capturando evendo de relogio a cada 1 segundo e atualizando a variável contadora
        if event.type == CLOCKTICK:
            temporizador = temporizador - 1

        # Click Keys Keyboard
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_index = 3
                player_mov -= player_speed
                player_curving = True
            if event.key == K_RIGHT:
                player_index = 4
                player_mov += player_speed
                player_curving = True
        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                player_index = 0
                player_mov = 0
                player_curving = False

        # Click Mouse
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

    # finalizando o jogo
    if temporizador == 0:
        success_game()

    # Update Player Position
    player_pos = (player_pos[0] + player_mov, player_pos[1])

    if player_pos[0] < sidewalk_left_edge + player_width / 2.0:
        player_pos = ((sidewalk_left_edge + player_width / 2.0), player_pos[1])
    if player_pos[0] + player_width > sidewalk_right_edge - player_width / 2.0:
        player_pos = ((sidewalk_right_edge - player_width / 2.0) - player_width, player_pos[1])

    player_hitbox[0] = (player_pos[0] + player_width * 0.15, player_pos[1] + player_height * 0.2)

    # Set Initial Position Enemy
    if create_enemy:
        enemyX = random.randint(166, 622)
        enemyY = 20
        create_enemy = False

    # Speed Enemy
    enemyY += enemy_speed

    # Show the Enemy
    screen.blit(enemyImg, (enemyX, enemyY))

    # Create New Enemy
    if enemyY > 600:
        create_enemy = True

    # Enemy Collision
    if (player_pos[1] + 20 >= enemyY - 10 and player_pos[1] - 20 <= enemyY + 10) and \
            (player_pos[0] + 20 >= enemyX - 10 and player_pos[0] - 20 <= enemyX + 20):
        create_enemy = True
        lives_value -= 1

    # Set Initial Position Mask
    if create_mask:
        maskX = random.randint(166, 622)
        maskY = 20
        create_mask = False

    # Speed Mask
    maskY += mask_speed

    # Show the Mask
    screen.blit(maskImg, (maskX, maskY))

    # Create New Mask
    if maskY > 600:
        create_mask = True

    # Mask Collision
    if (player_pos[1] + 20 >= maskY - 10 and player_pos[1] - 20 <= maskY + 10) and \
            (player_pos[0] + 20 >= maskX - 10 and player_pos[0] - 20 <= maskX + 20):
        create_mask = True
        score_value += 1


    # Set Initial Position Hand Sanitizer
    if create_hand_sanitizer:
        hand_sanitizerX = random.randint(166, 622)
        hand_sanitizerY = 20
        create_hand_sanitizer = False

    # Speed Hand Sanitizer
    hand_sanitizerY += hand_sanitizer_speed

    # Show the Hand Sanitizer
    screen.blit(hand_sanitizerImg, (hand_sanitizerX, hand_sanitizerY))

    # Create New Hand Sanitizer
    if hand_sanitizerY > 600:
        create_hand_sanitizer = True

    # Hand Sanitizer Collision
    if (player_pos[1] + 20 >= hand_sanitizerY - 10 and player_pos[1] - 20 <= hand_sanitizerY + 10) and \
            (player_pos[0] + 20 >= hand_sanitizerX - 10 and player_pos[0] - 20 <= hand_sanitizerX + 20):
        create_hand_sanitizer = True
        score_value += 1

    if not lives_value:
        game_over()

    # rendrizando as fontes do cronometro na tela do usuario
    timer1 = font.render('Tempo ' + str(temporizador), True, (YELLOW))
    screen.blit(timer1, (330, 10))

    # Show in Screen
    screen.blit(sound_button[sound_button_index], sound_button_pos)
    screen.blit(player[player_index], player_pos)
    show_score(scoreX, scoreY)
    show_lives(livesX, livesY)

    # Limita a taxa de quadros (framerate) a 60 quadros por segundo (60fps)
    clock.tick(60)

    pygame.display.update()
