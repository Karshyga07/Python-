import pygame
pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Circle")
clock = pygame.time.Clock()
running = True
ball_radius = 25
ball_color = (255, 0, 0)
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
step = 20
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, ball_color, (ball_x,ball_y), ball_radius)
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x - step - ball_radius >= 0:
        ball_x -= step
    if keys[pygame.K_RIGHT] and ball_x + step + ball_radius <= WIDTH:
        ball_x += step
    if keys[pygame.K_UP] and ball_y - step - ball_radius >= 0:
        ball_y -= step
    if keys[pygame.K_DOWN] and ball_y + step + ball_radius <= HEIGHT:
        ball_y += step
        
        
pygame.quit()