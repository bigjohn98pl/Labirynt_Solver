from pygame import draw
from pygame import display
from pygame import Rect

class Snake:
    def __init__(self,x_size,y_size):
        self.head = Rect(100, 100, x_size, y_size)
        self.body = []
        self.direction = "right"
        self.length = 1
        self.score = 0
        self.time_since_last_update = 0
        
    
    def move(self, DT: float):
        speed = 300
        movement_distance = speed * DT
        
        self.time_since_last_update += DT
        
        if self.time_since_last_update > 0.1:
            self.time_since_last_update = 0
            # print(self.time_since_last_update)

            last_position = (self.head.x, self.head.y)
            if self.direction == "left":
                self.head.x -= 20
            if self.direction == "right":
                self.head.x += 20
            if self.direction == "up":
                self.head.y -= 20
            if self.direction == "down":
                self.head.y += 20
            # print(abs(self.head.x - last_position[0]), abs(self.head.y - last_position[1]))
            for i in range(len(self.body) - 1, 0, -1):
                self.body[i].x = self.body[i - 1].x
                self.body[i].y = self.body[i - 1].y
        
            if self.body:
                    self.body[0].x, self.body[0].y = last_position
    
    def grow(self):
        self.length += 1
        self.score += 10
        self.body.append(Rect(self.head.x, self.head.y, 18, 18))
    # def draw(self):
    #     for element in self.body:
    #         display.dr(element)