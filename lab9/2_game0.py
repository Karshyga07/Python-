# imports
import pygame
import os
import random
import sys
from pygame.locals import *

# init
pygame.init()

# FPS
FPS = 60
FramePerSec = pygame.time.Clock()

CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)

# окно
WIDTH, HEIGHT = 320, 640
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")
icon = pygame.image.load(os.path.join("2-game-elements", "snake.png"))
pygame.display.set_icon(icon)

# фон
background = pygame.image.load(os.path.join("2-game-elements", "background.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# загрузка изображений
food_image = pygame.image.load(os.path.join("2-game-elements", "food.png"))
food_image = pygame.transform.scale(food_image, (CELL_SIZE, CELL_SIZE))

snake_image = pygame.image.load(os.path.join("2-game-elements", "snake.png"))
snake_image = pygame.transform.scale(snake_image, (CELL_SIZE, CELL_SIZE))

# параметры змейки
snake_body = [(WIDTH // 2, HEIGHT - CELL_SIZE)]
snake_dir = (0, 0)

# функция генерации еды по сетке
def random_food():
    x = random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    y = random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE
    return (x, y)

food = random_food()
speed = 10

run = True
while run:
    FramePerSec.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        # Управление
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake_dir != (0, CELL_SIZE):
                snake_dir = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN and snake_dir != (0, -CELL_SIZE):
                snake_dir = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT and snake_dir != (CELL_SIZE, 0):
                snake_dir = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT and snake_dir != (-CELL_SIZE, 0):
                snake_dir = (CELL_SIZE, 0)

    if snake_dir != (0, 0):
        # движение змейки
        head_x = snake_body[0][0] + snake_dir[0]
        head_y = snake_body[0][1] + snake_dir[1]
        new_head = (head_x, head_y)
        snake_body.insert(0, new_head)  # добавляем новую голову

        # отладка
        print("Змейка:", new_head, "Еда:", food)

        # проверка еды
        if new_head == food:
            food = random_food()
            speed += 1  # ускорение

        # проверка на стены и саму себя
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake_body[1:]):
            run = False

    # отрисовка
    screen.blit(background, (0, 0))
    screen.blit(food_image, food)

    for part in snake_body:
        screen.blit(snake_image, part)

    pygame.display.update()

pygame.quit()
