import random
from pygame import Rect
from config import WINDOW_SIZE
from config import PIXEL_SIZE
class Apple(Rect):
    def __init__(self):
        self.size = (PIXEL_SIZE,PIXEL_SIZE)
        self.x = 40
        self.y = 40

    def move_random(self):
        self.x = random.randrange(PIXEL_SIZE, WINDOW_SIZE[0]-PIXEL_SIZE,PIXEL_SIZE)
        self.y = random.randrange(PIXEL_SIZE, WINDOW_SIZE[1]-PIXEL_SIZE,PIXEL_SIZE)
