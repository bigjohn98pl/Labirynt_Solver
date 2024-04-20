import pygame
from snake import Snake
from apple import Apple
from config import WINDOW_SIZE

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True

snake = Snake(20, 20)
apple = Apple(20,20)
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
                # if snake.direction == "right":
                #     running = False
                snake.direction = "left"
            if event.key == pygame.K_RIGHT:
                # if snake.direction == "left":
                #     running = False
                snake.direction = "right"
            if event.key == pygame.K_UP:
                # if snake.direction == "down":
                #     running = False
                snake.direction = "up"
            if event.key == pygame.K_DOWN:
                # if snake.direction == "up":
                #     running = False
                snake.direction = "down"
        if event.type == pygame.QUIT:
            running = False
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
    print(snake.center, apple.center,snake.x-apple.x, snake.y-apple.y)
    rect_list = snake.collidelistall(snake.body)
    if len(rect_list) > 0:
        if(rect_list[0] == 1):
            if snake.length <= 2:
                print("You eat apple")
            else:
                print("You died, reverse direction")
        elif(rect_list[-1] == snake.length - 2):
            print("You eat apple")
        else:
            print("You died",rect_list,snake.length, len(snake.body))

    
    # RENDER YOUR GAME HERE
    for wall in walls:
        pygame.draw.rect(screen, "orange", wall)
    pygame.draw.rect(screen, "red",apple)
    pygame.draw.rect(screen, "white",snake)
    if snake.body != None:
        for element in snake.body:
            pygame.draw.rect(screen, "white",element)

    for direction, rect in snake.what_i_see.items():
            if rect.collidelist(walls) > -1:
                pygame.draw.rect(screen, "red", rect)
            elif rect.collidelist(snake.body) > -1:
                pygame.draw.rect(screen, "blue", rect)
            elif rect.colliderect(apple):
                pygame.draw.rect(screen, "yellow", rect)
            else:
                pygame.draw.rect(screen, "green", rect)
            

    text = str(f"Score: {snake.score}")
    text_font = pygame.font.SysFont("Arial", 30)
    text_surface = text_font.render(text, True, "white")
    screen.blit(text_surface, (15, 15))

    # flip() the display to put your work on screen
    pygame.display.flip()
    # pygame.display.update()

pygame.quit()