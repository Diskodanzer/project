import arcade


class Sphere(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.scale = 0.014
        self.texture = arcade.load_texture('recources/sphere.png')
    