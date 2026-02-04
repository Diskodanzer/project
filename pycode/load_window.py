import time
import arcade

class LoadingWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height, "Loading")
        self.width = width
        self.height = height
        self.star_scale = 1.0
        self.grow = False
        self.star = arcade.SpriteList()
    
    def setup(self):
        star = arcade.Sprite()
        arcade.texture = arcade.load_texture('recources/star.png')
        star.scale = 1.0
        star.center_x = self.width / 2
        star.center_y = self.height / 2
        self.star.append(star)
    
    def on_draw(self):
        arcade.draw_rect_filled(arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height), arcade.color.BLACK)
        self.star.draw()
    
    def on_update(self, delta_time):
        if self.star[0].scale >= 1.0:
            self.grow = False
        if not self.grow:
            self.star[0].scale += 0.1 * delta_time
        if self.star[0].scale >= 0.15 and not self.grow:
            self.star[0].scale -= 0.1 * delta_time
        else:
            self.grow = True
    
            