import arcade


class Bar:
    def __init__(self, x, y, speed):
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.width = 600
    
    def update(self, delta_time, pos):
        if self.width >= 0:
            self.width -= delta_time * 50
            #self.center_x -= delta_time * 50
        self.center_x, self.center_y = pos
        self.center_y -= 350
    
    def draw(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(self.center_x, self.center_y, self.width, 50), arcade.color.WHITE)
    
    def stretch(self):
        self.width += 100