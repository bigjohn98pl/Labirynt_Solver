import pygame
from snake import Snake
from apple import Apple
from config import WINDOW_SIZE

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True

game_state = {"position_and_direction": {}, "surroundings": {}}
snake = Snake(20, 20)
apple = Apple(20,20)
snake.where_is_apple(apple)
walls = [
    pygame.Rect(0, 0, 500, 20),
    pygame.Rect(0, 480, 500, 20),
    pygame.Rect(0, 0, 20, 500),
    pygame.Rect(480, 0, 20, 500)
]

while running:
    DT = clock.tick(60) / 1000 # limits FPS to 60
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if snake.direction == "right":
                    running = False
                snake.direction = "left"
            if event.key == pygame.K_RIGHT:
                if snake.direction == "left":
                    running = False
                snake.direction = "right"
            if event.key == pygame.K_UP:
                if snake.direction == "down":
                    running = False
                snake.direction = "up"
            if event.key == pygame.K_DOWN:
                if snake.direction == "up":
                    running = False
                snake.direction = "down"
        if event.type == pygame.QUIT:
            running = False

    game_state["position_and_direction"] = snake.where_is_apple(apple)        
    snake.look()
    snake.move(DT)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    if snake.collidelist(walls) > -1:
        running = False

    if apple.colliderect(snake):
        apple.move_random()
        snake.grow()
    elif apple.collidelist(snake.body) > -1:
        apple.move_random()

    body_collide = snake.collidelistall(snake.body)
    if len(body_collide) > 0 and len(snake.body) > 1:
        running = False

    # RENDER GAME HERE
    for wall in walls:
        pygame.draw.rect(screen, "orange", wall)
    pygame.draw.rect(screen, "red",apple)
    pygame.draw.rect(screen, "white",snake)
    if snake.body != None:
        for i,element in enumerate(snake.body):
            if i == 0:
                pygame.draw.rect(screen, "yellow", element)
            elif i == len(snake.body) - 1:
                pygame.draw.rect(screen, "orange", element)
            else:
                pygame.draw.rect(screen, "white",element)

    for direction, rect in snake.what_i_see.items():
            if rect.collidelist(walls) > -1:
                pygame.draw.rect(screen, "red", rect)
                game_state["surroundings"][direction] = "wall"
            elif rect.collidelist(snake.body) > -1:
                pygame.draw.rect(screen, "blue", rect)
                game_state["surroundings"][direction] = "body"
            elif rect.colliderect(apple):
                pygame.draw.rect(screen, "yellow", rect)
                game_state["surroundings"][direction] = "apple"
            else:
                pygame.draw.rect(screen, "green", rect)
                game_state["surroundings"][direction] = "    "
            

    text = str(f"Score: {snake.score}")
    text_font = pygame.font.SysFont("Arial", 30)
    text_surface = text_font.render(text, True, "white")
    screen.blit(text_surface, (15, 15))

    pygame.display.flip()

    print(game_state["position_and_direction"])

pygame.quit()