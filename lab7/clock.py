import pygame
import os
from datetime import datetime

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Clock")

clock = pygame.time.Clock()
running = True


background_path = os.path.join("clock-elements", "clock.png")
min_path = os.path.join("clock-elements", "min_hand (2).png")
sec_path = os.path.join("clock-elements", "sec_hand.png")


if not (os.path.exists(background_path) and os.path.exists(min_path) and os.path.exists(sec_path)):
    print("Error: One or more image files are missing.")
    pygame.quit()
    exit()

background = pygame.image.load(background_path)
min_hand = pygame.image.load(min_path)
sec_hand = pygame.image.load(sec_path)


background_rect = background.get_rect(center=(WIDTH // 2, HEIGHT // 2))
min_hand_rect = min_hand.get_rect(center=(WIDTH // 2, HEIGHT // 2))
sec_hand_rect = sec_hand.get_rect(center=(WIDTH // 2, HEIGHT // 2))

def rot_center(image, angle):
    orig_rect = image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=orig_rect.center)
    return rot_image, rot_rect

while running:
    screen.fill((255, 255, 255))
    

    now = datetime.now()
    second_angle = now.second  
    minute_angle = now.minute  
   
    screen.blit(background, background_rect)

    
    rotated_min_hand, min_hand_rect = rot_center(min_hand, minute_angle)
    rotated_sec_hand, sec_hand_rect = rot_center(sec_hand, second_angle)
    
    screen.blit(rotated_min_hand, min_hand_rect.topleft)
    screen.blit(rotated_sec_hand, sec_hand_rect.topleft)

    pygame.display.flip()
    clock.tick(1)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()