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

    snake.move(DT)

    if snake.head.x > WINDOW_SIZE[0] - 20 or snake.head.x < 0 or snake.head.y > WINDOW_SIZE[1] - 20 or snake.head.y < 0:
        running = False
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    if snake.head.collidelist(walls) > -1:
        running = False

    if apple.body.colliderect(snake.head):
        apple.move_random()
        snake.grow()

    rect_list = snake.head.collidelistall(snake.body)
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

    text = str(f"Score: {snake.score}")
    text_font = pygame.font.SysFont("Arial", 30)
    text_surface = text_font.render(text, True, "white")
    screen.blit(text_surface, (15, 15))


    pygame.draw.rect(screen, "red",apple.body)
    pygame.draw.rect(screen, "white",snake.head)
    if snake.body != None:
        for element in snake.body:
            pygame.draw.rect(screen, "white",element)
    # flip() the display to put your work on screen
    pygame.display.flip()
    # pygame.display.update()
    # snake.draw()

pygame.quit()