import arcade


class Custom(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x + 40
        self.center_y = y - 40
        self.scale = 0.23
        self.texture = arcade.load_texture('recources/custom.png')
    
    def movement(self, delta_time, x, y):
        self.center_x += delta_time * 200 + x - self.center_x + 40
        self.center_y += delta_time * 200 + y - self.center_y - 40
    
    def change_view(self):
        pass  #логика для уменьшенного угла обзора