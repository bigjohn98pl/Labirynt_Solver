from pygame import draw
from pygame import display
from pygame import Rect
from config import PIXEL_SIZE
class Snake(Rect):
    def __init__(self,x_size,y_size):
        self.size = (x_size,y_size)
        self.x = 100
        self.y = 100
        self.body: list[Rect] = []
        self.direction = "right"
        self.what_i_see = {}
        self.apple_direction = "none"
        self.length = 1
        self.score = 0
        self.time_since_last_update = 0
        self.state = {}
        
    
    def move(self, DT: float):
        speed = 300
        movement_distance = speed * DT
        
        self.time_since_last_update += DT
        
        if self.time_since_last_update > 0.1:
            self.time_since_last_update = 0

            last_position = (self.center)
            if self.direction == "left":
                self.move_ip(-PIXEL_SIZE, 0)
            if self.direction == "right":
                self.move_ip(PIXEL_SIZE, 0)
            if self.direction == "up":
                self.move_ip(0,-PIXEL_SIZE)
            if self.direction == "down":
                self.move_ip(0,PIXEL_SIZE)

            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].center = self.body[i - 1].center
        
            if self.body:
                self.body[0].center = last_position
                    
    def look(self):
        self.what_i_see = {
            "left": Rect(self.centerx - PIXEL_SIZE, self.centery,5,5),
            "right": Rect(self.centerx + PIXEL_SIZE, self.centery,5,5),
            "up": Rect(self.centerx, self.centery - PIXEL_SIZE,5,5),
            "down": Rect(self.centerx, self.centery + PIXEL_SIZE,5,5),
            "upper_left": Rect(self.centerx - PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
            "lower_left": Rect(self.centerx - PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
            "upper_right": Rect(self.centerx + PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
            "lower_right": Rect(self.centerx + PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
        }
        

    def grow(self):
        self.length += 1
        self.score += 10
        if len(self.body) == 0:
            body_part = Rect(self.x, self.y, 17, 17)
        elif len(self.body) == 1:
            body_part = Rect(self.body[0].x, self.body[0].y, 17, 17)
        else:
            body_part = Rect(self.body[-1].x, self.body[-1].y, 17, 17)
        self.body.append(body_part)
    
    def where_is_apple(self, apple):
        x_diff = apple.x-self.x
        y_diff = apple.y-self.y
        direction: str = ""

        if y_diff == 0:
            direction += " "
        elif y_diff < 0:
            direction += "up"
        else:
            direction += "down"

        if x_diff == 0:
            direction += " "
        elif x_diff < 0:
            direction += " left"
        else:
            direction += " right"
        
        print(direction, x_diff, y_diff)
