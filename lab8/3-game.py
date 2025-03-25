import pygame

# Константы
WIDTH, HEIGHT = 640, 640
FPS = 80
radius = 2
color = 'pink'
mode = 'pen'
draw = False

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

screen.fill((255, 255, 255))


# --- ФУНКЦИИ РИСОВАНИЯ ---

def DrawLine(screen, start, end, width, color): 
    x1, y1 = start
    x2, y2 = end
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    A = y2 - y1
    B = x1 - x2
    C = x2 * y1 - x1 * y2

    if dx > dy:
        if x1 > x2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for x in range(x1, x2):
            y = int((-C - A * x) / B)
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)
    else:
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        for y in range(y1, y2):
            x = int((-C - B * y) / A)
            pygame.draw.circle(screen, pygame.Color(color), (x, y), width)

def DrawCircle(screen, start, end, width, color):
    x1, y1 = start
    x2, y2 = end
    x = (x1 + x2) // 2
    y = (y1 + y2) // 2
    radius_calc = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
    pygame.draw.circle(screen, pygame.Color(color), (x, y), radius_calc, width)

def DrawRectangle(screen, start, end, thickness, color):
    x1, y1 = start
    x2, y2 = end
    top_left_x = min(x1, x2)
    top_left_y = min(y1, y2)
    rect_width = abs(x1 - x2)
    rect_height = abs(y1 - y2)
    pygame.draw.rect(screen, pygame.Color(color), (top_left_x, top_left_y, rect_width, rect_height), thickness)

def DrawSquare(screen, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    size = min(abs(x2 - x1), abs(y2 - y1))
    top_left_x = min(x1, x2)
    top_left_y = min(y1, y2)
    pygame.draw.rect(screen, pygame.Color(color), (top_left_x, top_left_y, size, size), thickness)

def DrawRightTriangle(screen, color, start, end, thickness):
    x1, y1 = start
    x2, y2 = end
    points = [(x1, y1), (x2, y2), (x1, y2)] if x1 <= x2 else [(x1, y1), (x2, y2), (x2, y1)]
    pygame.draw.polygon(screen, pygame.Color(color), points, thickness)


# --- ОСНОВНОЙ ЦИКЛ ---

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Клавиши
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r: 
                mode = "rectangle"
            elif event.key == pygame.K_c: 
                mode = "circle"
            elif event.key == pygame.K_s: 
                mode = "square"
            elif event.key == pygame.K_t: 
                mode = "right_tri"
            elif event.key == pygame.K_e: 
                mode = "erase"
            elif event.key == pygame.K_p: 
                mode = "pen"
            elif event.key == pygame.K_q: screen.fill((255, 255, 255))

            # Цвета
            elif event.key == pygame.K_1: 
                color = "black"
            elif event.key == pygame.K_2: 
                color = "green"
            elif event.key == pygame.K_3: 
                color = "red"
            elif event.key == pygame.K_4: 
                color = "blue"
            elif event.key == pygame.K_5: 
                color = "yellow"

            # Толщина
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                radius = min(50, radius + 1)
            elif event.key == pygame.K_MINUS:
                radius = max(1, radius - 1)

        # Мышь нажата
        if event.type == pygame.MOUSEBUTTONDOWN:
            draw = True
            prevPos = event.pos
            if mode == "pen":
                pygame.draw.circle(screen, pygame.Color(color), event.pos, radius)
        
        # Мышь отпущена
        if event.type == pygame.MOUSEBUTTONUP:
            draw = False
            if mode == "rectangle":
                DrawRectangle(screen, prevPos, event.pos, radius, color)
            elif mode == "square":
                DrawSquare(screen, color, prevPos, event.pos, radius)
            elif mode == "right_tri":
                DrawRightTriangle(screen, color, prevPos, event.pos, radius)
            elif mode == "circle":
                DrawCircle(screen, prevPos, event.pos, radius, color)

        # Движение мыши
        if event.type == pygame.MOUSEMOTION:
            if draw:
                if mode == "pen":
                    DrawLine(screen, lastPos, event.pos, radius, color)
                elif mode == "erase":
                    DrawLine(screen, lastPos, event.pos, radius, "white")
            lastPos = event.pos

    # --- UI отображение: текущий радиус, цвет и режим ---
    pygame.draw.rect(screen, pygame.Color("white"), (0, 0, 300, 30))
    renderRadius = font.render(str(radius), True, pygame.Color(color))  # Render the text showing the current radius
    screen.blit(renderRadius, (5, 5)) 

    pygame.display.flip()
    clock.tick(FPS)
