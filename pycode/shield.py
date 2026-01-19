import arcade
import math



#сильно доработать надо

class Shield(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture('recources/shield.png')
        self.center_x = x
        self.center_y = y + 50
        self.scale = 0.024
        self.alpha = 0
        self.t = 2.0
    
    def r(self, xm, ym, px, py):
        pass
        self.t = 2.0
        self.alpha = 255
    
    def update(self, delta_time, xp, yp):
        self.center_x = xp
        self.center_y = yp + 50
        if self.alpha > 0:
            self.t -= delta_time
            if self.t <= 0:
                self.alpha = 0