import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_WIDTH = 75
BLOCK_HEIGHT = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BALL_SIZE = 20
POWER_UP_SIZE = 15

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Screen Setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Breakout Game")

# Fonts
font = pygame.font.Font(None, 36)

# Sound Effects
hit_sound = pygame.mixer.Sound('hit.wav')
power_up_sound = pygame.mixer.Sound('powerup.wav')
level_up_sound = pygame.mixer.Sound('levelup.wav')

# Game Variables
player_name = "Mahmoud"
score = 0
best_score = 0
level = 1
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 30
ball_x = SCREEN_WIDTH // 2
ball_y = SCREEN_HEIGHT // 2
ball_dx = 3 * random.choice([1, -1])
ball_dy = 3 * random.choice([1, -1])
paddle_speed = 5

# Power-Up Variables
power_ups = []


# Function to Create Blocks
def create_blocks(level):
    blocks = []
    for i in range(5):
        for j in range(10):
            block_rect = pygame.Rect(j * (BLOCK_WIDTH + 5) + 35, i * (BLOCK_HEIGHT + 5) + 50, BLOCK_WIDTH, BLOCK_HEIGHT)
            blocks.append(block_rect)
    return blocks


# Initialize Blocks
blocks = create_blocks(level)

# Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle_x > 0:
        paddle_x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle_x < SCREEN_WIDTH - PADDLE_WIDTH:
        paddle_x += paddle_speed

    # Ball Movement
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball Collision with Walls
    if ball_x <= 0 or ball_x >= SCREEN_WIDTH - BALL_SIZE:
        ball_dx *= -1
        hit_sound.play()
    if ball_y <= 0:
        ball_dy *= -1
        hit_sound.play()

    # Ball Collision with Paddle
    paddle_rect = pygame.Rect(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
    if ball_rect.colliderect(paddle_rect):
        ball_dy *= -1
        hit_sound.play()

    # Ball Collision with Blocks
    for block in blocks[:]:
        if ball_rect.colliderect(block):
            ball_dy *= -1
            blocks.remove(block)
            score += 10
            hit_sound.play()
            if random.randint(1, 10) == 1:  # 10% chance to drop a power-up
                power_up_rect = pygame.Rect(block.x, block.y, POWER_UP_SIZE, POWER_UP_SIZE)
                power_ups.append(power_up_rect)

    # Ball Missed the Paddle
    if ball_y > SCREEN_HEIGHT:
        if score > best_score:
            best_score = score
        score = 0
        ball_x, ball_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        ball_dx, ball_dy = 3 * random.choice([1, -1]), 3 * random.choice([1, -1])

    # Power-Up Movement and Collision with Paddle
    for power_up in power_ups[:]:
        power_up.y += 3  # Power-ups fall down
        if power_up.colliderect(paddle_rect):
            power_ups.remove(power_up)
            power_up_sound.play()
            paddle_speed = 8  # Example power-up effect

    # Remove off-screen power-ups
    power_ups = [p for p in power_ups if p.y < SCREEN_HEIGHT]

    # Draw Blocks
    for block in blocks:
        pygame.draw.rect(screen, GREEN, block)

    # Draw Paddle
    pygame.draw.rect(screen, ORANGE, paddle_rect)

    # Draw Ball
    pygame.draw.ellipse(screen, WHITE, ball_rect)

    # Draw Power-Ups
    for power_up in power_ups:
        pygame.draw.rect(screen, RED, power_up)

    # Draw Scores and Player Name
    score_text = font.render(f"Score: {score}", True, WHITE)
    best_score_text = font.render(f"Best: {best_score}", True, WHITE)
    player_name_text = font.render(player_name, True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (20, 10))
    screen.blit(best_score_text, (20, 40))
    screen.blit(player_name_text, (SCREEN_WIDTH - 200, 10))
    screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))

    # Check if level is complete
    if not blocks:
        level += 1
        level_up_sound.play()
        blocks = create_blocks(level)
        ball_dx *= 1.2  # Increase ball speed
        ball_dy *= 1.2

    # Update Display
    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
