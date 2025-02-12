import pygame
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
GRID_SIZE = 20  # Size of each grid cell
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 50)

# Game variables
snake = [(100, 100), (80, 100), (60, 100)]
direction = (GRID_SIZE, 0)
food = (random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE, random.randint(2, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE)
score = 0
highest_score = 0
hearts = 0
food_counter = 0
running = True
game_over = False

# Game loop
while running:
    screen.fill(BLACK)
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != (0, GRID_SIZE):
                direction = (0, -GRID_SIZE)
            elif event.key == pygame.K_DOWN and direction != (0, -GRID_SIZE):
                direction = (0, GRID_SIZE)
            elif event.key == pygame.K_LEFT and direction != (GRID_SIZE, 0):
                direction = (-GRID_SIZE, 0)
            elif event.key == pygame.K_RIGHT and direction != (-GRID_SIZE, 0):
                direction = (GRID_SIZE, 0)
            elif game_over and event.key == pygame.K_RETURN:
                snake = [(100, 100), (80, 100), (60, 100)]
                direction = (GRID_SIZE, 0)
                score = 0
                food_counter = 0
                hearts = 0
                game_over = False

    if not game_over:
        # Move the snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        
        # Wrap around screen (like old Nokia Snake)
        new_head = (new_head[0] % WIDTH, new_head[1] % HEIGHT)
        
        # Check collision with itself
        if new_head in snake:
            if hearts > 0:
                hearts -= 1
                snake = [(100, 100), (80, 100), (60, 100)]
                direction = (GRID_SIZE, 0)
            else:
                game_over = True
                if score > highest_score:
                    highest_score = score
                continue
        
        snake.insert(0, new_head)

        # Check if the snake eats food
        if new_head == food:
            score += 10
            food_counter += 1
            if food_counter == 10:
                hearts += 1
                food_counter = 0
            food = (random.randint(0, (WIDTH//GRID_SIZE)-1) * GRID_SIZE, random.randint(2, (HEIGHT//GRID_SIZE)-1) * GRID_SIZE)
        else:
            snake.pop()

        # Draw food
        pygame.draw.rect(screen, RED, (food[0], food[1], GRID_SIZE, GRID_SIZE))

        # Draw snake
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], GRID_SIZE, GRID_SIZE))

        # Display score and hearts
        text = font.render(f"Score: {score}  High Score: {highest_score}  Hearts: {hearts}", True, WHITE)
        screen.blit(text, (10, 5))
    else:
        # Game Over screen
        screen.fill(BLACK)
        game_over_text = large_font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//3))
        play_again_text = font.render("Press ENTER to Play Again", True, WHITE)
        screen.blit(play_again_text, (WIDTH//2 - 110, HEIGHT//2))
        high_score_text = font.render(f"Highest Score: {highest_score}", True, BLUE)
        screen.blit(high_score_text, (WIDTH//2 - 90, HEIGHT//2 + 40))
    
    pygame.display.update()

pygame.quit()
