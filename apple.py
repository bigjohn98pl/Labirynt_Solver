import random
from pygame import Rect
from config import WINDOW_SIZE
from config import PIXEL_SIZE
class Apple(Rect):
    def __init__(self,size_x,size_y):
        self.size = (size_x,size_y)
        self.x = 40
        self.y = 40

    def move_random(self):
        self.x = random.randrange(PIXEL_SIZE, WINDOW_SIZE[0]-self.size[0],PIXEL_SIZE)
        self.y = random.randrange(PIXEL_SIZE, WINDOW_SIZE[1]-self.size[1],PIXEL_SIZE)
