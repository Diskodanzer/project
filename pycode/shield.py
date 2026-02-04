import arcade

#сильно доработать надо

class Shield:
    def __init__(self, x, y):
        self.center_x = x
        self.center_y = y
        self.speed = 500
        self.r = 0
    
    def update(self, player_x, player_y):
        self.center_x = player_x
        self.center_y = player_y
    
    def draw(self):
        arcade.draw_circle_outline(self.center_x, self.center_y, self.r, arcade.color.GHOST_WHITE, border_width=4)
    
    def adjust(self, delta_time):
        if self.r < 85:
            self.r += self.speed * delta_time
    
    def disappear(self):
        self.r = 0
        self.alpha = 0
        