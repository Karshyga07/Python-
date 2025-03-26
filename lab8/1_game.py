# Imports
import pygame, sys
from pygame.locals import *
import random, time
import os

# Initialize
pygame.init()

# Settings
FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 3
SCORE = 0
COINS = 0
c1, c2, c3, c4, c5 = False, False, False, False, False

# Colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fonts
font = pygame.font.SysFont("Verdana", 20)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Background
background = pygame.image.load(os.path.join("1-game-elements", "background.png"))
screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Racer")

# --- CLASSES ---
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "Enemy.png"))
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.reset_position()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "coin.png"))
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 40))

    def move(self):
        global COINS, SPEED, c1, c2, c3, c4, c5
        if self.rect.bottom < SCREEN_HEIGHT // 3:
            COINS += 3
        elif self.rect.bottom < SCREEN_HEIGHT // 1.5:
            COINS += 2
        else:
            COINS += 1

        # Increase speed at thresholds
        if not c1 and COINS >= 10:
            SPEED += 1; c1 = True
        if not c2 and COINS >= 20:
            SPEED += 1; c2 = True
        if not c3 and COINS >= 30:
            SPEED += 1; c3 = True
        if not c4 and COINS >= 40:
            SPEED += 1; c4 = True
        if not c5 and COINS >= 50:
            SPEED += 1; c5 = True

        self.reset_position()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join("1-game-elements", "Player.png"))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed[K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)
        if pressed[K_UP] and self.rect.top > 0:
            self.rect.move_ip(0, -5)
        if pressed[K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
            self.rect.move_ip(0, 5)

# --- Game Over ---
def game_over_screen():
    screen.fill(RED)
    screen.blit(game_over, (150, 250))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit(); sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                elif event.key == K_ESCAPE:
                    return False

# --- RESET GAME STATE ---
def reset_game(player, enemy, coin):
    global SCORE, COINS, SPEED, c1, c2, c3, c4, c5
    SCORE = 0
    COINS = 0
    SPEED = 3
    c1 = c2 = c3 = c4 = c5 = False
    player.rect.center = (160, 520)
    enemy.reset_position()
    coin.reset_position()

# --- INITIAL OBJECTS ---
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins_group = pygame.sprite.Group()
coins_group.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Events
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

background_y = 0

# --- MAIN LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == INC_SPEED:
            SPEED += 0.1

    # Check collisions
    if pygame.sprite.spritecollideany(P1, enemies):
        continue_game = game_over_screen()
        if not continue_game:
            pygame.quit()
            sys.exit()
        else:
            reset_game(P1, E1, C1)

    # Scroll background
    background_y = (background_y + SPEED) % background.get_height()
    screen.blit(background, (0, background_y))
    screen.blit(background, (0, background_y - background.get_height()))

    # Draw score & coins
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coins_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(coins_text, (400, 10))

    # Move & draw all sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        if isinstance(entity, Coin) and pygame.sprite.collide_rect(P1, entity):
            entity.move()
        else:
            entity.move()

    pygame.display.update()
    FramePerSec.tick(FPS)
