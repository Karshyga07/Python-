import pygame
import os
import random
import sys
import time
from pygame.locals import *

pygame.init()

# Настройки
FPS = 60
WIDTH, HEIGHT = 800, 600
speed = 3
score = 0
coins = 0

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Шрифт и экран
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load(os.path.join("1-game-elements", "background.jpg"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("1-Game")

# Флаги ускорения
c1 = c2 = c3 = c4 = c5 = False

# Игровые классы
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "capybara.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        global score
        self.rect.move_ip(0, speed)
        if self.rect.top > HEIGHT:
            score += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "coin.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))

    def move(self):
        global coins, speed, c1, c2, c3, c4, c5
        if self.rect.bottom < HEIGHT // 3:
            coins += 3
        elif self.rect.bottom < HEIGHT // 1.5:
            coins += 2
        else:
            coins += 1

        if not c1 and coins >= 10:
            speed += 1
            c1 = True
        if not c2 and coins >= 20:
            speed += 1
            c2 = True
        if not c3 and coins >= 30:
            speed += 1
            c3 = True
        if not c4 and coins >= 40:
            speed += 1
            c4 = True
        if not c5 and coins >= 50:
            speed += 1
            c5 = True

        self.rect.center = (random.randint(40, WIDTH - 40), random.randint(40, HEIGHT - 40))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "cat.jpg"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if self.rect.top > 0 and pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if self.rect.bottom < HEIGHT and pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

# Функция Game Over
def game_over_screen():
    screen.fill(WHITE)
    screen.blit(game_over, (300, 250))
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    sys.exit()

# Объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы
enemys = pygame.sprite.Group()
enemys.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Событие увеличения скорости
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Фон
FramePerSec = pygame.time.Clock()
background_y = 0

# --- Игровой цикл ---
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            speed += 0.1
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemys):
        game_over_screen()

    # Двигаем фон
    background_y = (background_y + speed) % background.get_rect().height
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_rect().height))

    # Тексты
    score_text = font_small.render("Score: " + str(score), True, BLACK)
    coins_text = font_small.render("Coins: " + str(coins), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (700, 10))

    # Отрисовка и движение спрайтов
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if isinstance(entity, Coin) and pygame.sprite.collide_rect(P1, entity):
            entity.move()
        else:
            entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
