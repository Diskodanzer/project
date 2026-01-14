import arcade
from arcade.particles import EmitBurst, Emitter, FadeParticle
import random


class Key(arcade.Sprite):
    def __init__(self, x, y, scale):
        super().__init__()
        self.textures = [arcade.load_texture(f'recources/{i}.png') for i in range(1, 10)]
        self.anim_frame = 0
        self.set_texture(0)
        self.center_x = x
        self.center_y = y
        self.scale = scale
        self.c = 0
        
    def update_animation(self, delta_time = 1 / 60):
        self.c += delta_time
        if self.c >= 0.1:
            self.anim_frame += 1
            self.set_texture(self.anim_frame % len(self.textures) - 1)
            self.c = 0
    
    def pickup(self):
        self.remove_from_sprite_lists()
    