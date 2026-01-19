import arcade


class Custom(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 0.23
        self.texture = arcade.load_texture('recources/custom.png')
    
    def movement(self, delta_time, x, y):
        self.center_x += delta_time * 200 + x - self.center_x
        self.center_y += delta_time * 200 + y - self.center_y
    
    def change_view(self):
        pass  #логика для уменьшенного угла обзора