import numpy as np
import itertools
import matplotlib.pyplot as plt
from config import *
#define all states
apple_directions = {'upleft': 0, 'up': 1, 'upright': 2, 'left': 3, 'right': 4, 'downleft': 5, 'down': 6, 'downright': 7}
# all_apple_positions = [(x, y) for x in range(PIXEL_SIZE, WINDOW_SIZE[0] - PIXEL_SIZE, PIXEL_SIZE) for y in range(PIXEL_SIZE, WINDOW_SIZE[1] - PIXEL_SIZE, PIXEL_SIZE)]
# all_snake_positions = [(x, y) for x in range(PIXEL_SIZE, WINDOW_SIZE[0] - PIXEL_SIZE, PIXEL_SIZE) for y in range(PIXEL_SIZE, WINDOW_SIZE[1] - PIXEL_SIZE, PIXEL_SIZE)]

snake_directions = {'left': 0, 'right': 1, 'up': 2, 'down': 3}
states = [0, 1, 2, 3]  # empty, apple, snake_body, walls

surrounding_states = list(itertools.product(states, repeat=8)) # repeat = 8 because there snake head sees 8 surrounding tiles
all_possible_states = [(apple_directions[apple], snake_directions[snake], list(surround))
                       for apple, snake, surround in itertools.product(apple_directions, snake_directions, surrounding_states)]


print("All states: ", len(all_possible_states))
print("Example state: ", all_possible_states[0])

def state_to_index(state):
    apple_pos, snake_pos, surroundings = state
    
    surroundings_index = 0
    base = 4  
    for i, val in enumerate(surroundings):
        surroundings_index += val * (base ** i)

    total_base = base ** 8
    index = surroundings_index + total_base * (snake_pos + 4 * apple_pos)
    return index

def choose_action(state_index, epsilon=0.1):
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(Q[state_index])

def update_Q(state_index: int, action_index: int, reward, next_state_index: int, alpha=0.1, gamma=0.99):
    # Q[s,a] = Q[s,a] + alpha*(reward + gamma*max(Q[s',a']) - Q[s,a])
    best_next_action = np.argmax(Q[next_state_index])
    td_target = reward + gamma * Q[next_state_index][best_next_action]
    td_error = td_target - Q[state_index][action_index]
    td_errors.append(abs(td_error))
    Q[state_index][action_index] += alpha * td_error

def plot_Q_values(mean_q_values):

    plt.plot(mean_q_values, marker='o')
    plt.title('Average Q-value Evolution Over Time')
    plt.xlabel('Episode')
    plt.ylabel('Average Q-value')
    plt.grid(True)
    plt.show()

def plot_td_errors(td_errors):
    plt.plot(td_errors)
    plt.title("TD-Errors")
    plt.xlabel("Step")
    plt.ylabel("TD-Error")
    plt.show()

def plot_total_rewards(total_rewards):
    plt.plot(total_rewards)
    plt.title("Total Rewards per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Total Reward")
    plt.show()

def plot_actions_per_episode(total_actions: list[dict[str, int]]):
    data = {action: [] for action in ACTION_COUNT.keys()}
    for actions_per_episode in total_actions:
        for action_type, count in actions_per_episode.items():
            data[action_type].append(count)

    fig, axs = plt.subplots(len(ACTION_COUNT.keys()), 1, figsize=(10, 20))  # Ustawienie wielkości figury dla czytelności
    fig.suptitle('Actions Count per Episode')

    for i, action_type in enumerate(ACTION_COUNT.keys()):
        axs[i].plot(data[action_type], label=action_type, marker='o')
        axs[i].set_title(action_type)
        axs[i].set_xlabel("Episode")
        axs[i].set_ylabel("Count")
        axs[i].legend()
    plt.show()

num_states = len(all_possible_states)
num_actions = 4

Q = np.zeros((num_states, num_actions))

td_errors = []
epsilone_change = [100,200,300,400,500,600,700,800,900,1000]
epsilon = 0.1  # Stopień eksploracji
alpha = 0.4    # Współczynnik uczenia
gamma = 0.9    # Współczynnik dyskontujący
