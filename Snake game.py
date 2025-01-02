import pygame
import random

# Initialize Pygame
pygame.init()

# Colors
color_1 = (255, 255, 255)  # White
color_2 = (255, 255, 102)  # Yellow
color_6 = (50, 153, 213)   # Blue
color_4 = (213, 50, 80)    # Red
color_5 = (0, 255, 0)      # Green
color_3 = (0, 0, 0)        # Black


# Screen dimensions
box_len = 900
box_height = 600

# Initialize the display
add_caption = pygame.display.set_mode((box_len, box_height))
pygame.display.set_caption("SNAKE GAME")
timer = pygame.time.Clock()

snake_block = 10
snake_speed = 10  # Default speed

# Fonts
display_style = pygame.font.SysFont("arial", 30, "bold")
score_font = pygame.font.SysFont("arial", 35, "bold")


def final_score(score, speed):
    """Display the score and current speed."""
    value = score_font.render(f"Score: {score} | Speed: {speed}", True, color_2)
    add_caption.blit(value, [0, 0])


def make_snake(snake_block, list_snake):
    """Draw the snake."""
    for x in list_snake:
        pygame.draw.rect(add_caption, color_1, [x[0], x[1], snake_block, snake_block])


def display_msg(msg, color):
    """Display a message on the screen."""
    mssg = display_style.render(msg, True, color)
    add_caption.blit(mssg, [box_len / 4, box_height / 2])


def welcome_screen():
    """Display the welcome screen with difficulty options."""
    add_caption.fill(color_3)  # Fill the screen with black (color_3)

    # Display the welcome message
    welcome_msg = display_style.render("Welcome to the Snake Game!", True, color_2)
    add_caption.blit(welcome_msg, [box_len / 4, box_height / 4])  # Centered vertically in the top half

    # Display difficulty options below the welcome message
    level_msg = display_style.render("Press 1 for Easy, 2 for Medium, 3 for Hard", True, color_4)
    add_caption.blit(level_msg, [box_len / 6, box_height / 2])  # Centered vertically in the middle

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 10  # Easy speed
                elif event.key == pygame.K_2:
                    return 20  # Medium speed
                elif event.key == pygame.K_3:
                    return 30  # Hard speed



def game_start():
    """Main game logic."""
    global snake_speed
    snake_speed = welcome_screen()  # Get difficulty level
    game_over = False
    game_close = False

    values_x1 = box_len / 2
    values_y1 = box_height / 2

    new_x1 = 0
    new_y1 = 0

    list_snake = []
    snake_len = 1

    foodx_pos = round(random.randrange(0, box_len - snake_block) / 10.0) * 10.0
    foody_pos = round(random.randrange(0, box_height - snake_block) / 10.0) * 10.0

    obstacles = [[random.randrange(0, box_len, snake_block), random.randrange(0, box_height, snake_block)] for _ in range(5)]

    while not game_over:
        while game_close:
            add_caption.fill(color_3)
            display_msg("You lost! Press C to Play Again or Q to Quit", color_4)
            final_score(snake_len - 1, snake_speed)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_start()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and new_x1 == 0:
                    new_x1 = -snake_block
                    new_y1 = 0
                elif event.key == pygame.K_RIGHT and new_x1 == 0:
                    new_x1 = snake_block
                    new_y1 = 0
                elif event.key == pygame.K_UP and new_y1 == 0:
                    new_y1 = -snake_block
                    new_x1 = 0
                elif event.key == pygame.K_DOWN and new_y1 == 0:
                    new_y1 = snake_block
                    new_x1 = 0

        if values_x1 >= box_len or values_x1 < 0 or values_y1 >= box_height or values_y1 < 0:
            game_close = True

        values_x1 += new_x1
        values_y1 += new_y1
        add_caption.fill(color_6)

        # Draw food
        pygame.draw.rect(add_caption, color_5, [foodx_pos, foody_pos, snake_block, snake_block])

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(add_caption, color_4, [obstacle[0], obstacle[1], snake_block, snake_block])

        # Check collision with obstacles
        for obstacle in obstacles:
            if values_x1 == obstacle[0] and values_y1 == obstacle[1]:
                game_close = True

        # Snake logic
        snake_head = [values_x1, values_y1]
        list_snake.append(snake_head)

        if len(list_snake) > snake_len:
            del list_snake[0]

        for x in list_snake[:-1]:
            if x == snake_head:
                game_close = True

        make_snake(snake_block, list_snake)
        final_score(snake_len - 1, snake_speed)

        pygame.display.update()

        # Check if food is eaten
        if values_x1 == foodx_pos and values_y1 == foody_pos:
            foodx_pos = round(random.randrange(0, box_len - snake_block) / 10.0) * 10.0
            foody_pos = round(random.randrange(0, box_height - snake_block) / 10.0) * 10.0
            snake_len += 1

            # Increase speed
            if snake_speed < 50:
                snake_speed += 1

        timer.tick(snake_speed)

    pygame.quit()
    quit()


game_start()
