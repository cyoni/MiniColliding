import pygame as game
from random import randrange

import Math
from Brick import Brick


def load(address):
    return game.image.load(address)


gameRunning = True
screen_x = 500
screen_y = 500
score = -1
game.init()
screen = game.display.set_mode((screen_x, screen_y))
playerImage = load("brick.png")
backgroundImage = load("background.jpg")
brickImage = load("brick.png")
player_x = screen_x/2
player_y = screen_y - 100
bricks = []
num_of_elements = 6
difficult = 0.5


def change_level():
    global difficult, score
    if score == 3:
        difficult = difficult + 0.5
    elif score == 10:
        difficult = difficult + 0.5


def change_bricks():
    global bricks, score
    score = score + 1
    bricks = []
    new_element = randrange(1, num_of_elements)
    offset = 0
    for i in range(num_of_elements):
        if i == new_element:
            bricks.append(-1)
        else:
            bricks.append(Brick(offset, 0))
        offset = offset + 80
    change_level()


change_bricks()


def draw_bricks():
    for i in range(num_of_elements):
        current_brick = bricks[i]
        if current_brick != -1:
            screen.blit(brickImage, (current_brick.x, current_brick.y))


def update_bricks():
    global difficult
    for i in range(num_of_elements):
        current_brick = bricks[i]
        if current_brick != -1:
            current_brick.y = current_brick.y + difficult
            if current_brick.y > screen_y:
                change_bricks()
                break


def check_for_collision():
    global gameRunning
    for i in range(num_of_elements):
        current_brick = bricks[i]
        if current_brick != -1:
            distance = Math.distance(player_x, player_y, current_brick.x, current_brick.y)
            if distance < 30:
                gameRunning = False


def show_score():
    global score
    font = game.font.Font('SansBold.ttf', 32)
    text_score = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(text_score, (10, 10))


while gameRunning:
    for event in game.event.get():
        if event.type == game.QUIT:
            gameRunning = False
            break
    keys = game.key.get_pressed()

    x = player_x
    if keys[game.K_LEFT]:
        x = x - 1
    if keys[game.K_RIGHT]:
        x = x + 1

    player_x = x

    screen.blit(backgroundImage, [0, 0])  # this has to be first
    draw_bricks()
    update_bricks()
    check_for_collision()
    show_score()
    screen.blit(playerImage, (player_x, player_y))
    game.display.update()
