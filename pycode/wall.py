import arcade

class Wall(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.texture = arcade.load_texture('recources/wall.png')
        self.center_x = x
        self.center_y = y
        self.scale = 0.80
        
        