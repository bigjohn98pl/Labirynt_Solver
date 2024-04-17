import random
from pygame import Rect
from config import WINDOW_SIZE
class Apple:
    def __init__(self,size_x,size_y):
        self.size = (size_x,size_y)
        # apple_pos = random.randrange(0, 1280,self.size[0]), random.randrange(0, 720,self.size[1])
        apple_pos = (40,40)
        self.body = Rect(apple_pos[0], apple_pos[1], self.size[0], self.size[0])

    def move_random(self):
        self.body.x = random.randrange(20, WINDOW_SIZE[0]-self.size[0],20)
        self.body.y = random.randrange(20, WINDOW_SIZE[1]-self.size[1],20)
