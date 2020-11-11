import random
import math
import pygame
from pygame import mixer

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('images/background_game.png')

# Sound
pygame.mixer.init(44000, -16, 1, 1024)
mixer.music.load("song.ogg")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 625
playerY = 40
playerX_change = 0
playerY_change = 0

# Score
score_value = 100
textX = 10
testY = 10

# Font
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, playerX, playerY):
    distance = math.sqrt(math.pow(enemyX - playerX, 2) + (math.pow(enemyY - playerY, 2)))
    if distance < 30:
        return True
    else:
        return False


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 8

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/ghost.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)


# Game Loop
running = True
while running:

    # Background Image with black ground
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
    #
    #     # Game Over
    #     if enemyY[i] > 440:
    #         for j in range(num_of_enemies):
    #             enemyY[j] = 2000
    #         game_over_text()
    #         break
    #
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        enemy(enemyX[i], enemyY[i], i)

    collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
    if collision:
        score_value -= 1

    player(playerX, playerY)
    show_score(textX, testY)
    pygame.display.update()
