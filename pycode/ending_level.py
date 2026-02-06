import arcade
from character import Character
from wall import Wall
#from end_screen import End
import arcade
from pyglet.graphics import Batch
from arcade.particles import EmitBurst, Emitter, FadeParticle, EmitMaintainCount
import random


class End_level(arcade.Window):
    def __init__(self, width, height, cell_size, curr_time):
        super().__init__(width, height, 'end')
        self.view_width = width
        self.view_height = height
        self.cell_size = cell_size
        self.player = arcade.SpriteList()
        self.creature = arcade.SpriteList()
        self.player_texture = arcade.load_texture(
                        'recources\\СharacterSprite.png')
        self.dead_player_texture = arcade.load_texture(
                        'recources\\СharacterSprite1.png')
        self.keys = set()
        self.time_spent = curr_time
        self.walls = arcade.SpriteList(use_spatial_hash=True)
        self.rows = 3000 // cell_size
        self.cols = 3000 // cell_size
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.zoom = 1.0
        self.anim_timer = 0.3
        self.curr_anim = 0
        self.can_move = True
        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )
        self.t_e = [] #эффект трэйла за игроком
        self.background_music = arcade.load_sound('recources/white_noise.wav')
        arcade.play_sound(self.background_music, volume=1.0, loop=True)
    
    def setup(self):
        for i in range(self.rows):
            for j in range(4):
                if i == 0 or i == self.rows - 1:
                    x = i * self.cell_size + self.cell_size // 2
                    y = j * self.cell_size + self.cell_size // 2
                    self.walls.append(Wall(x, y))
                if j == 0 or j == 3:
                    x = i * self.cell_size + self.cell_size // 2
                    y = j * self.cell_size + self.cell_size // 2
                    self.walls.append(Wall(x, y))
        self.player.append(Character(3000, 3000, 0.14, 200, self.cell_size * 2, self.cell_size * 2, self.player_texture))
        creature = arcade.Sprite()
        creature.textures = [arcade.load_texture(f'recources/pianist{i}.png') for i in range(9)]
        creature.set_texture(0)
        creature.scale = 0.65
        creature.center_x = 3000 - self.cell_size * 2 - 30
        creature.center_y = self.cell_size * 2
        self.creature.append(creature)
        self.physics = arcade.PhysicsEngineSimple(
            self.player[0],
            self.walls
        )
        self.t_e.append(self.trail(self.player[0].center_x, self.player[0].center_y))
    
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.camera_shake.update_camera()
        self.camera_shake.readjust_camera()
        self.creature.draw()
        self.player.draw()
        self.walls.draw()
        if self.t_e:
            self.t_e[0].draw()
    
    def on_update(self, delta_time):
        self.physics.update()
        self.player.update(delta_time, self.keys)
        self.time_spent += delta_time
        self.anim_timer -= delta_time
        current_x, current_y = self.world_camera.position
        target_x, target_y = self.player[0].center_x, self.player[0].center_y
        new_x = current_x + (target_x - current_x) * 0.12
        new_y = current_y + (target_y - current_y) * 0.12
        self.world_camera.position = (new_x, new_y)
        if self.player[0].center_x >= self.creature[0].center_x - 300:
            self.camera_shake.start()
            self.camera_shake.update(delta_time)
        if self.player[0].center_x >= self.creature[0].center_x - 130:
            self.keys = set()
            self.can_move = False
            if self.anim_timer <= 0:
                self.creature[0].set_texture(self.curr_anim)
                self.curr_anim += 1
                if self.curr_anim >= 9:
                    self.close()
                    end_screen = End(self.view_width, self.view_height, self.time_spent)
                    arcade.run()
                    #self.window.close()
                self.anim_timer = 0.3
        if self.t_e:
            self.t_e[0].center_x = self.player[0].center_x
            self.t_e[0].center_y = self.player[0].center_y
            self.t_e[0].update()

        
    def on_key_press(self, symbol, modifiers):
        if self.can_move:
            self.keys.add(symbol)
        if symbol == arcade.key.ESCAPE:
            self.close()
    
    def on_key_release(self, symbol, modifiers):
        if self.can_move:
            self.keys.remove(symbol)
    
    def trail(self, x, y, count=40):
        return Emitter(
            center_xy=(x, y),
            emit_controller=EmitMaintainCount(count),
            particle_factory=lambda x: FadeParticle(
                filename_or_texture=arcade.make_soft_square_texture(
                    10, arcade.color.GHOST_WHITE, 255, 255),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 2.2),
                lifetime=random.uniform(0.35, 0.6),
                start_alpha=255, end_alpha=255,
                scale=random.uniform(0.25, 0.4)
            )
        )


class End(arcade.Window):
    def __init__(self, width, height, play_time):
        super().__init__(width, height, 'end_screen')
        self.view_width = width
        self.view_height = height
        self.play_time = play_time
        self.batch = Batch()
    
    def on_draw(self):
        arcade.draw_texture_rect(arcade.load_texture('recources/end_screen.png'), arcade.rect.XYWH(self.view_width / 2, self.view_height / 2, self.view_width, self.view_height))
        self.fonts = arcade.Text(
            text=f'Your play time: {round(self.play_time / 60, 2)}mins.',
            x=self.view_width // 2,
            y=self.view_height // 2,
            anchor_x='center',
            anchor_y='center',
            color=arcade.color.WHITE_SMOKE,
            font_size=40,
            batch=self.batch
        )     
        self.batch.draw()
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.close()



'''if __name__ == '__main__':
    window = arcade.Window(
        800,
        800,
        "end",
        resizable=False
    )
    game = End_level(800, 800, 100, 2.0)
    game.setup()
    window.show_view(game)
    window.center_window()
    arcade.run()'''