WINDOW_SIZE = (500,500)
PIXEL_SIZE = 20

TOTAL_EPISODES = 5000
EPISODE = 0

PENALTESS = {
    "body_collision": -1.0,
    "wall_collision": -1.0,
    "going_from_apple": -0.01,
    "forbidden_direction": -1.0
}

REWARDS = {
    "explore": 0.0,
    "going_to_apple": 0.01,
    "get_apple": 1.0,
}

ACTION_COUNT = {
    "body_collision": 0,
    "wall_collision": 0,
    "explore": 0,
    "going_to_apple": 0,
    "going_from_apple": 0,
    "get_apple": 0,
    "forbidden_direction": 0
}

Q_TABLE_MEANS = []
MAX_SCORE = 0.0
MAX_EPISODE = 0