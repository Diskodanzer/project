import arcade


class Enemy(arcade.Sprite):
    
    tex = arcade.load_texture('recources/enemy.png')
    
    def __init__(self, x, y, speed):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.scale = 0.024
        self.knockback = 1.5 #время для кнокбека от щита
        self.texture = Enemy.tex
    
    def update(self, delta_time, xp, yp):
        dx = xp - self.center_x
        dy = yp - self.center_y
        dist = (dx ** 2 + dy ** 2) ** (1/2)
        if dist != 0:
            dx = dx / dist
            dy = dy / dist
        self.center_x += self.speed * delta_time * dx
        self.center_y += self.speed * delta_time * dy
        