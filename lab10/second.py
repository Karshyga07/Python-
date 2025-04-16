import pygame
import psycopg2
import random
import sys

WEIGHT = 600
HEIGHT = 400

def connect():
    return psycopg2.connect(
        dbname="postgres",
        user="omega",
        password="",  
        host="localhost",
        port="5432"
    )

def init_db():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "user" (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL
        );
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_score (
            user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE,
            level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0,
            player_x INTEGER,
            player_y INTEGER,
            saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def get_or_create_user(username):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT id FROM \"user\" WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        user_id = row[0]
    else:
        cur.execute("INSERT INTO \"user\" (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
    cur.close()
    conn.close()
    return user_id

def load_user_score(user_id):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT level, score, player_x, player_y FROM user_score WHERE user_id = %s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row

def save_user_score(user_id, level, score, x, y):
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_score (user_id, level, score, player_x, player_y)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (user_id) DO UPDATE SET
            level = EXCLUDED.level,
            score = EXCLUDED.score,
            player_x = EXCLUDED.player_x,
            player_y = EXCLUDED.player_y;
    """, (user_id, level, score, x, y))
    conn.commit()
    cur.close()
    conn.close()


LEVELS = {
    1: {"speed": 5, "walls": []},
    2: {"speed": 7, "walls": [(100, 100, 400, 10)]},
    3: {"speed": 9, "walls": [(50, 200, 540, 10), (300, 50, 10, 380)]}
}

def get_level_settings(level):
    return LEVELS.get(level, LEVELS[1])

def get_random_food(snake_body):
    while True:
        pos = [random.randrange(0, WEIGHT, 20), random.randrange(0, HEIGHT, 20)]
        if pos not in snake_body:
            return pos


pygame.init()
screen = pygame.display.set_mode((WEIGHT, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

init_db()


username = input("Enter your username: ").strip()
user_id = get_or_create_user(username)
data = load_user_score(user_id)
if data:
    level, score, player_x, player_y = data
else:
    level, score, player_x, player_y = 1, 0, 100, 100
settings = get_level_settings(level)

snake = [[player_x, player_y]]
direction = 'RIGHT'
apple_pos = get_random_food(snake)
paused = False


running = True
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_user_score(user_id, level, score, snake[0][0], snake[0][1])
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                if paused:
                    save_user_score(user_id, level, score, snake[0][0], snake[0][1])
            if event.key == pygame.K_LEFT and direction != 'RIGHT': direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT': direction = 'RIGHT'
            if event.key == pygame.K_UP and direction != 'DOWN': direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP': direction = 'DOWN'

    if paused:
        pause_text = font.render("PAUSED", True, (255, 255, 0))
        screen.blit(pause_text, (250, 200))
        pygame.display.flip()
        clock.tick(5)
        continue

    
    head_x, head_y = snake[0]
    if direction == 'UP': head_y -= 20
    elif direction == 'DOWN': head_y += 20
    elif direction == 'LEFT': head_x -= 20
    elif direction == 'RIGHT': head_x += 20

    snake.insert(0, [head_x, head_y])


    if snake[0] == apple_pos:
        score += 10
        apple_pos = get_random_food(snake)
    else:
        snake.pop()

    
    for block in snake:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(block[0], block[1], 20, 20))

    
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(apple_pos[0], apple_pos[1], 20, 20))

    
    for wall in settings["walls"]:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(wall))

    pygame.display.flip()
    clock.tick(settings["speed"])

pygame.quit()
sys.exit()
