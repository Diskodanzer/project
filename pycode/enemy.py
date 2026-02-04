import arcade


class Enemy(arcade.Sprite):
    
    tex = arcade.load_texture('recources/enemy.png')
    
    def __init__(self, x, y, speed):
        super().__init__()
        self.center_x = x
        self.center_y = y
        self.speed = speed
        self.scale = 0.024
        self.knockback_time = 1.5 #время для кнокбека от щита
        self.texture = Enemy.tex
    
    def update(self, delta_time, xp, yp):
        if self.speed < 0:
            self.knockback_time -= delta_time
        if self.knockback_time <= 0:
            self.speed *= -1
            self.knockback_time = 1.5
        dx = xp - self.center_x
        dy = yp - self.center_y
        if dx > 200 or dy > 200:
            pass
        else:
            dist = (dx ** 2 + dy ** 2) ** (1/2)
            if dist != 0:
                dx = dx / dist
                dy = dy / dist
            self.center_x += self.speed * delta_time * dx
            self.center_y += self.speed * delta_time * dy
    
    def knockback(self):
        self.speed *= -1
        