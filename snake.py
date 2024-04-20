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
        self.length = 1
        self.score = 0
        self.time_since_last_update = 0
        
    
    def move(self, DT: float):
        speed = 300
        movement_distance = speed * DT
        
        self.time_since_last_update += DT
        
        if self.time_since_last_update > 0.3:
            self.time_since_last_update = 0
            # print(self.time_since_last_update)

            last_position = (self.center)
            if self.direction == "left":
                self.move_ip(-PIXEL_SIZE, 0)
            if self.direction == "right":
                self.move_ip(PIXEL_SIZE, 0)
            if self.direction == "up":
                self.move_ip(0,-PIXEL_SIZE)
            if self.direction == "down":
                self.move_ip(0,PIXEL_SIZE)
            # print(abs(self.head.x - last_position[0]), abs(self.head.y - last_position[1]))
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].center = self.body[i - 1].center
                # self.body[i].y = self.body[i - 1].y
        
            if self.body:
                    # self.body[0].x, self.body[0].y = last_position
                    self.body[0].center = last_position
    
    def look(self):
        if self.direction == "left":
            self.what_i_see = {
                "left": Rect(self.centerx - PIXEL_SIZE, self.centery,5,5),
                "up": Rect(self.centerx, self.centery - PIXEL_SIZE,5,5),
                "down": Rect(self.centerx, self.centery + PIXEL_SIZE,5,5),
                "upper_left": Rect(self.centerx - PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
                "lower_left": Rect(self.centerx - PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
            }
        if self.direction == "right":
            self.what_i_see = {
                "right": Rect(self.centerx + PIXEL_SIZE, self.centery,5,5),
                "up": Rect(self.centerx, self.centery - PIXEL_SIZE,5,5),
                "down": Rect(self.centerx, self.centery + PIXEL_SIZE,5,5),
                "upper_right": Rect(self.centerx + PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
                "lower_right": Rect(self.centerx + PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
            }
        if self.direction == "up":
            self.what_i_see = {
                "up": Rect(self.centerx, self.centery - PIXEL_SIZE,5,5),
                "left": Rect(self.centerx - PIXEL_SIZE, self.centery,5,5),
                "right": Rect(self.centerx + PIXEL_SIZE, self.centery,5,5),
                "upper_left": Rect(self.centerx - PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
                "upper_right": Rect(self.centerx + PIXEL_SIZE, self.centery - PIXEL_SIZE,5,5),
            }
        if self.direction == "down":
            self.what_i_see = {
                "down": Rect(self.centerx, self.centery + PIXEL_SIZE,5,5),
                "left": Rect(self.centerx - PIXEL_SIZE, self.centery,5,5),
                "right": Rect(self.centerx + PIXEL_SIZE, self.centery,5,5),
                "lower_left": Rect(self.centerx - PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
                "lower_right": Rect(self.centerx + PIXEL_SIZE, self.centery + PIXEL_SIZE,5,5),
            }

    def grow(self):
        self.length += 1
        self.score += 10
        body_part = Rect(self.x, self.y, 17, 17)
        # body_part.center = (self.x, self.y)
        self.body.append(body_part)
