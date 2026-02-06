import arcade

class Exit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 100
        self.height = 0
        self.appear = False
    
    def draw(self):
        if self.appear:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.x, self.y, 50, self.height), arcade.color.GHOST_WHITE)
    
    def update(self, delta_time):
        if self.appear:
            if self.height <= 50:
                self.height += self.speed * delta_time