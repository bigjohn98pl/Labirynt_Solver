import pygame
from snake import Snake
from apple import Apple
from config import *
import q_learning as q
from numpy import mean

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(WINDOW_SIZE)
running = True

apple_directions_to_num = {'upleft': 0, 'up': 1, 'upright': 2, 'left': 3, 'right': 4, 'downleft': 5, 'down': 6, 'downright': 7}
snake_directions_to_num = {'left': 0, 'right': 1, 'up': 2, 'down': 3}
snake_directions_to_str = {0: 'left', 1: 'right', 2: 'up', 3: 'down'}
object_to_num = {'empty': 0, 'apple': 1, 'snake_body': 2, 'walls': 3}
game_state = []
surrounding_states = []
snake = Snake()
snake.move_random()
apple = Apple()
apple.move_random()
snake.where_is_apple(apple)
walls = [
    pygame.Rect(0, 0, WINDOW_SIZE[0], PIXEL_SIZE),
    pygame.Rect(0, WINDOW_SIZE[1]-PIXEL_SIZE, WINDOW_SIZE[0], PIXEL_SIZE),
    pygame.Rect(0, 0, PIXEL_SIZE, WINDOW_SIZE[1]),
    pygame.Rect(WINDOW_SIZE[0]-PIXEL_SIZE, 0, PIXEL_SIZE, WINDOW_SIZE[1])
]
text_score = str(f"Score: {snake.score}")
text_episodes = str(f"Episode: {EPISODE}/{TOTAL_EPISODES}")
text_max_score = str(f"Max Score: {MAX_SCORE}")
text_font = pygame.font.SysFont("Arial", 20)

def re_run():
    snake.reset()
    apple.move_random()
    snake.where_is_apple(apple)

def set_game_state(state):
    snake.reset()
    snake.direction = snake_directions_to_num.get(state[1])

def run():
    running = True
    while running:
        DT = clock.tick(60) / 1000 # limits FPS to 60
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if snake.direction == "right":
                        re_run()
                    snake.direction = "left"
                if event.key == pygame.K_RIGHT:
                    if snake.direction == "left":
                        re_run()
                    snake.direction = "right"
                if event.key == pygame.K_UP:
                    if snake.direction == "down":
                        re_run()
                    snake.direction = "up"
                if event.key == pygame.K_DOWN:
                    if snake.direction == "up":
                        re_run()
                    snake.direction = "down"
            if event.type == pygame.QUIT:
                running = False

        game_state.append(apple_directions_to_num[snake.where_is_apple(apple)])  
        game_state.append(snake_directions_to_num[snake.direction])      
        snake.look()
        snake.move(DT)

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")
        if snake.collidelist(walls) > -1:
            re_run()

        if apple.colliderect(snake):
            apple.move_random()
            snake.grow()
        elif apple.collidelist(snake.body) > -1:
            apple.move_random()

        body_collide = snake.collidelistall(snake.body)
        if len(body_collide) > 0 and len(snake.body) > 1:
            re_run()

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
                    surrounding_states.append(3)
                elif rect.collidelist(snake.body) > -1:
                    pygame.draw.rect(screen, "red", rect)
                    surrounding_states.append(2)
                elif rect.colliderect(apple):
                    pygame.draw.rect(screen, "blue", rect)
                    surrounding_states.append(1)
                else:
                    pygame.draw.rect(screen, "green", rect)
                    surrounding_states.append(0)
                

        text = str(f"Score: {snake.score}")
        text_font = pygame.font.SysFont("Arial", 30)
        text_surface = text_font.render(text, True, "white")
        screen.blit(text_surface, (15, 15))

        pygame.display.flip()

        game_state.append(tuple(surrounding_states))
        print(tuple(game_state))
        surrounding_states.clear()
        game_state.clear()
    pygame.quit()

def initial_game_state():
    snake.reset()
    apple.move_random()
    while apple.colliderect(snake):
        apple.move_random()
    
    apple_direction = snake.where_is_apple(apple)
    surrounding_states = []
    surroundings = snake.look()
    for direction, rect in surroundings.items():
        if rect.collidelist(walls) > -1:
            surrounding_states.append(3)
        elif rect.collidelist(snake.body) > -1:
            surrounding_states.append(2)
        elif rect.colliderect(apple) > -1:
            surrounding_states.append(1)
        else:
            surrounding_states.append(0)
    try:
        return tuple([apple_directions_to_num[apple_direction],snake_directions_to_num[snake.direction],surrounding_states])
    except KeyError as e:
        print(e)

def run_q_learning():
    global ACTION_COUNT
    global EPISODE
    global MAX_SCORE
    global MAX_EPISODE
    MAX_SCORE = 0.0
    total_rewards = []
    total_actions: list[dict[str, int]] = []
    running = True

    for episode in range(TOTAL_EPISODES):
        EPISODE = episode
        total_reward = 0.0
        state = initial_game_state()
        state_index = q.state_to_index(state)
        game_over = False
        ACTION_COUNT = {
            "body_collision": 0,
            "wall_collision": 0,
            "explore": 0,
            "going_to_apple": 0,
            "going_from_apple": 0,
            "get_apple": 0,
            "forbidden_direction": 0
        }
        
        while not game_over:
            DT = clock.tick(200) / 1000 # limits FPS to 60
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            # if EPISODE in q.epsilone_change:
            #     q.epsilon -= 0.01
            action_index = q.choose_action(state_index, q.epsilon)
            next_state, reward, game_over = game_step(DT,state,action_index)
            total_reward += reward
            next_state_index = q.state_to_index(next_state)
            q.update_Q(state_index, action_index, reward, next_state_index, q.alpha, q.gamma)
            state = next_state
            state_index = next_state_index
        total_rewards.append(total_reward)
        if max(total_rewards) > MAX_SCORE:
            MAX_EPISODE = EPISODE
            MAX_SCORE = max(total_rewards)
        total_actions.append(ACTION_COUNT.copy())
        Q_TABLE_MEANS.append(mean(q.Q))

        if not running:
            break
    pygame.quit()

    q.plot_actions_per_episode(total_actions)
    q.plot_total_rewards(total_rewards)
    q.plot_Q_values(Q_TABLE_MEANS)
    q.plot_td_errors(q.td_errors)

def game_step(DT,state,action_index):
    global ACTION_COUNT
    global EPISODE
    game_state = []
    surrounding_states = []
    game_over = False
    direction = snake_directions_to_str.get(action_index)
    snake.move(DT)

    if direction == "left" and snake.direction == "right" or direction == "right" and snake.direction == "left" or direction == "up" and snake.direction == "down" or direction == "down" and snake.direction == "up":
        snake.score += PENALTESS["forbidden_direction"]
        ACTION_COUNT["forbidden_direction"] += 1
        game_over = True
    else:
        snake.direction = direction
        snake.score += REWARDS["explore"]
        ACTION_COUNT["explore"] += 1

    if apple.colliderect(snake):
        apple.move_random()
        snake.grow()
        snake.score += REWARDS["get_apple"]
        ACTION_COUNT["get_apple"] += 1

    while apple.collidelist(snake.body) > -1:
        apple.move_random()

    apple_direction = snake.where_is_apple(apple)
    if direction in apple_direction:
        snake.score += REWARDS["going_to_apple"]
        ACTION_COUNT["going_to_apple"] += 1
    else:
        snake.score += PENALTESS["going_from_apple"]
        ACTION_COUNT["going_from_apple"] += 1
        

    for direction, rect in snake.look().items():
        if rect.collidelist(walls) > -1:
            surrounding_states.append(3)
        elif rect.collidelist(snake.body) > -1:
            surrounding_states.append(2)
        elif rect.colliderect(apple):
            surrounding_states.append(1)
        else:
            surrounding_states.append(0)

    if snake.collidelist(walls) > -1:
        game_over = True
        snake.score += PENALTESS["wall_collision"]
        ACTION_COUNT["wall_collision"] += 1

    body_collide = snake.collidelistall(snake.body)
    if len(body_collide) > 0 and len(snake.body) > 1:
        game_over = True
        snake.score += PENALTESS["body_collision"]
        ACTION_COUNT["body_collision"] += 1

    render_frame(screen)

    game_state.append(apple_directions_to_num[apple_direction])  
    game_state.append(snake_directions_to_num[snake.direction])  
    game_state.append(surrounding_states)

    return tuple(game_state), float(snake.score), game_over

def render_frame(screen: pygame.Surface):
    # RENDER GAME FRAME
    screen.fill("black")
    
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
            surrounding_states.append(3)
        elif rect.collidelist(snake.body) > -1:
            pygame.draw.rect(screen, "red", rect)
            surrounding_states.append(2)
        elif rect.colliderect(apple):
            pygame.draw.rect(screen, "blue", rect)
            surrounding_states.append(1)
        else:
            pygame.draw.rect(screen, "green", rect)
            surrounding_states.append(0)
            

    text_score = str(f"Score: {snake.score}")
    text_episodes = str(f"Episode: {EPISODE}/{TOTAL_EPISODES}")
    text_max_score = str(f"Max Score: {int(MAX_SCORE)} Episode: {MAX_EPISODE}")

    surface_score = text_font.render(text_score, True, "white")
    surface_episodes = text_font.render(text_episodes, True, "white")
    surface_max_score = text_font.render(text_max_score, True, "white")

    screen.blit(surface_score, (20, 20))
    screen.blit(surface_episodes, (20, 480))
    screen.blit(surface_max_score, (200, 480))

    pygame.display.flip()

if __name__ == "__main__":
    # run()
    run_q_learning()