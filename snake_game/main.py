import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Create the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Snake properties
snake_segment_size = 20
snake_color = (0, 255, 0)  # Green
snake_segments = [
    pygame.Rect(100, 100, snake_segment_size, snake_segment_size),
    pygame.Rect(80, 100, snake_segment_size, snake_segment_size),
    pygame.Rect(60, 100, snake_segment_size, snake_segment_size),
]

# Food properties
food_color = (255, 0, 0)  # Red
food_position = pygame.Rect(
    random.randrange(0, screen_width // snake_segment_size) * snake_segment_size,
    random.randrange(0, screen_height // snake_segment_size) * snake_segment_size,
    snake_segment_size,
    snake_segment_size,
)

# Initial direction
direction = "RIGHT"

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Move the snake
    if direction == "RIGHT":
        new_head = pygame.Rect(snake_segments[0].x + snake_segment_size, snake_segments[0].y, snake_segment_size, snake_segment_size)
    elif direction == "LEFT":
        new_head = pygame.Rect(snake_segments[0].x - snake_segment_size, snake_segments[0].y, snake_segment_size, snake_segment_size)
    elif direction == "UP":
        new_head = pygame.Rect(snake_segments[0].x, snake_segments[0].y - snake_segment_size, snake_segment_size, snake_segment_size)
    elif direction == "DOWN":
        new_head = pygame.Rect(snake_segments[0].x, snake_segments[0].y + snake_segment_size, snake_segment_size, snake_segment_size)

    snake_segments.insert(0, new_head)

    # Check for food consumption
    if snake_segments[0].colliderect(food_position):
        food_position.x = random.randrange(0, screen_width // snake_segment_size) * snake_segment_size
        food_position.y = random.randrange(0, screen_height // snake_segment_size) * snake_segment_size
    else:
        snake_segments.pop()

    # Check for collisions
    # Wall collision
    if (
        snake_segments[0].left < 0
        or snake_segments[0].right > screen_width
        or snake_segments[0].top < 0
        or snake_segments[0].bottom > screen_height
    ):
        running = False

    # Self collision
    for segment in snake_segments[1:]:
        if snake_segments[0].colliderect(segment):
            running = False

    # Fill the background
    screen.fill((0, 0, 0))  # Black

    # Draw the snake
    for segment in snake_segments:
        pygame.draw.rect(screen, snake_color, segment)

    # Draw the food
    pygame.draw.rect(screen, food_color, food_position)

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(10)

# Quit Pygame
pygame.quit()
