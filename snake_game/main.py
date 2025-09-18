import pygame
import random

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SNAKE_SEGMENT_SIZE = 20
BACKGROUND_COLOR = (34, 34, 34)
SNAKE_COLOR = (109, 237, 138)
FOOD_COLOR = (255, 95, 133)
TEXT_COLOR = (240, 241, 78)
FPS = 10

# --- Functions ---

def move_snake(direction, snake_segments):
    """Moves the snake by adding a new head in the given direction."""
    if direction == "RIGHT":
        new_head = pygame.Rect(snake_segments[0].x + SNAKE_SEGMENT_SIZE, snake_segments[0].y, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE)
    elif direction == "LEFT":
        new_head = pygame.Rect(snake_segments[0].x - SNAKE_SEGMENT_SIZE, snake_segments[0].y, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE)
    elif direction == "UP":
        new_head = pygame.Rect(snake_segments[0].x, snake_segments[0].y - SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE)
    elif direction == "DOWN":
        new_head = pygame.Rect(snake_segments[0].x, snake_segments[0].y + SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE)
    snake_segments.insert(0, new_head)

def check_food_collision(snake_segments, food_position):
    """Checks for collision with food. If eaten, moves food and returns True."""
    if snake_segments[0].colliderect(food_position):
        food_position.x = random.randrange(0, SCREEN_WIDTH // SNAKE_SEGMENT_SIZE) * SNAKE_SEGMENT_SIZE
        food_position.y = random.randrange(0, SCREEN_HEIGHT // SNAKE_SEGMENT_SIZE) * SNAKE_SEGMENT_SIZE
        return True
    return False

def check_game_over(snake_segments):
    """Checks for game over conditions (wall or self-collision)."""
    head = snake_segments[0]
    # Wall collision
    if (head.left < 0 or head.right > SCREEN_WIDTH or
            head.top < 0 or head.bottom > SCREEN_HEIGHT):
        return True
    # Self collision
    for segment in snake_segments[1:]:
        if head.colliderect(segment):
            return True
    return False

def draw_elements(screen, snake_segments, food_position, score):
    """Draws all game elements on the screen."""
    screen.fill(BACKGROUND_COLOR)
    for segment in snake_segments:
        pygame.draw.rect(screen, SNAKE_COLOR, segment)
    pygame.draw.rect(screen, FOOD_COLOR, food_position)

    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(text, (10, 10))

    pygame.display.flip()

def draw_game_over(screen, score):
    """Displays the game over screen."""
    screen.fill(BACKGROUND_COLOR)
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 36)
    text = font.render(f"Final Score: {score}", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
    screen.blit(text, text_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                waiting = False

def main():
    """Main function to run the snake game."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    # Initial game state
    snake_segments = [
        pygame.Rect(100, 100, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE),
        pygame.Rect(80, 100, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE),
        pygame.Rect(60, 100, SNAKE_SEGMENT_SIZE, SNAKE_SEGMENT_SIZE),
    ]
    food_position = pygame.Rect(
        random.randrange(0, SCREEN_WIDTH // SNAKE_SEGMENT_SIZE) * SNAKE_SEGMENT_SIZE,
        random.randrange(0, SCREEN_HEIGHT // SNAKE_SEGMENT_SIZE) * SNAKE_SEGMENT_SIZE,
        SNAKE_SEGMENT_SIZE,
        SNAKE_SEGMENT_SIZE,
    )
    direction = "RIGHT"
    score = 0

    running = True
    while running:
        # Event handling
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

        # Game logic
        move_snake(direction, snake_segments)

        if check_food_collision(snake_segments, food_position):
            score += 1
        else:
            snake_segments.pop()

        if check_game_over(snake_segments):
            running = False

        # Drawing
        if running:
            draw_elements(screen, snake_segments, food_position, score)
            clock.tick(FPS)

    draw_game_over(screen, score)
    pygame.quit()

if __name__ == "__main__":
    main()
