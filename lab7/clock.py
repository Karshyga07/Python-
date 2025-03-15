import pygame
import os
import datetime
pygame.init
WIGTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIGTH, HEIGHT))
pygame.display.set_caption("Clock")
clock = pygame.time.Clock()
running = True
image = pygame.image.load(os.path.join("clock-elements", "clock.png"))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(image, (0, 0))
    
    