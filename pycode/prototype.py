import arcade
import sys
import random
import pprint
from character import Character
from wall import Wall
from key import Key
from custom_camera import Custom
from enemy import Enemy
from shield import Shield
from bar import Bar
from arcade.particles import EmitBurst, Emitter, FadeParticle, EmitMaintainCount
sys.setrecursionlimit(10000)

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Game"


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title, fullscreen=False, resizable=True)

        self.world_camera = arcade.camera.Camera2D()
        self.cell_size = cell_size
        self.rows = 3000 // cell_size
        self.cols = 3000 // cell_size
        self.painted = 0
        self.player = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=cell_size*4) 
        self.ex_keys = arcade.SpriteList()
        self.keys = []
        self.ex_key_count = 0
        self.pickable = False
        self.emitters = []
        self.t_e = []
        self.ex_e = None
        self.exit = arcade.SpriteList() # Сделать логику выхода с уровня
        self.path = arcade.shape_list.ShapeElementList()
        self.custom = arcade.SpriteList()
        self.grid = None
        self.enemies = arcade.SpriteList()
        #self.shield = arcade.SpriteList()
        self.camera_shake = arcade.camera.grips.ScreenShake2D(   #спросить что тут не так
            self.world_camera.view_data,  
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )
    
    def check(self, row, col):
        if row <= 0 or row >= self.rows or col <= 0 or col >= self.cols:
            return False
        
        if self.grid[row][col] != 0:
            return False
        
        try:
            neighbors = 0
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = row + dr, col + dc
                    if self.grid[nr][nc] == 1:
                        neighbors += 1
        
            return neighbors <= 2
        except IndexError:
            pass
    
    def check_for_directions(self, lst):
        new_lst = []
        for elem in lst:
            directions = []
            if self.check(elem[0], elem[1] - 1):
                directions.append((elem[0], elem[1] - 1))
            if self.check(elem[0], elem[1] + 1):
                directions.append((elem[0], elem[1] + 1))
            if self.check(elem[0] + 1, elem[1]):
                directions.append((elem[0] + 1, elem[1]))
            if self.check(elem[0] - 1, elem[1]):
                directions.append((elem[0] - 1, elem[1]))
            if not directions:
                continue
            n1, n2 = random.choice(directions)
            new_lst.append([n1, n2])
            self.grid[n1][n2] = 1
        return lst + new_lst
    
    def setup(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid[self.rows // 2 - 1][self.cols // 2 - 1] = 1
        self.painted = [[self.rows // 2 - 1, self.cols // 2 - 1]]
        self.prev = []
        while self.prev != self.painted:
            self.prev = self.painted
            self.painted = self.check_for_directions(self.painted)
        self.player.append(Character(3000, 3000, 0.14, 200, self.painted[0][0] * self.cell_size  + self.cell_size // 2, self.painted[0][1] * self.cell_size + self.cell_size // 2))
        self.bar = Bar(self.player[0].center_x, self.player[0].center_y - 350, 25)
        self.custom.append(Custom(self.player[0].center_x, self.player[0].center_y))
        self.t_e.append(self.trail(self.painted[0][0] * self.cell_size  + self.cell_size // 2, self.painted[0][1] * self.cell_size + self.cell_size // 2))
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] != 1:
                    x = col * self.cell_size + self.cell_size // 2
                    y = row * self.cell_size + self.cell_size // 2
                    wall = Wall(x, y)
                    self.walls.append(wall)
        self.physics = arcade.physics_engines.PhysicsEngineSimple(
            self.player[0],
            self.walls
        )
        self.enemies.append(Enemy(random.randint(100, 2900), random.randint(100, 2900), 100))
        #self.shield.append(Shield(self.player[0].center_x, self.player[0].center_y))
        y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        if self.grid[y][x] == 0:
            while self.grid[y][x] == 0:
                y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self.ex_keys.append(Key(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2, 0.15))
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                if self.grid[row][col] == 1:
                    rect = arcade.shape_list.create_rectangle_filled(center_x=x, center_y=y,
                                            width=self.cell_size,
                                            height=self.cell_size, color=arcade.color.DAVY_GREY)
                    self.path.append(rect)
        #pprint.pprint(self.grid)
        #pprint.pprint(self.painted)
                
    def on_draw(self):
        self.clear()
        self.world_camera.use()
        self.camera_shake.update_camera()
        self.path.draw()
        self.player.draw()
        self.t_e[0].draw()
        self.walls.draw()
        self.ex_keys.draw()
        for elem in self.emitters:
            elem.draw()
        self.camera_shake.readjust_camera()
        self.enemies.draw()
        #self.shield.draw()
        self.custom.draw()
        self.bar.draw()
        
    
    def on_update(self, delta_time):
        for elem in self.player:
            elem.update(delta_time, self.keys)
        self.physics.update()
        self.camera_shake.update(delta_time)
        self.custom[0].movement(delta_time, self.player[0].center_x, self.player[0].center_y)
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player[0].center_x,
            self.player[0].center_y),
            0.12
        )
        if self.ex_keys:
            self.ex_keys[0].update_animation(delta_time)
        if self.ex_keys:
            coll = arcade.check_for_collision_with_list(self.player[0], self.ex_keys)
            if coll:
                for elem in self.ex_keys:
                    self.pickable = True
                    self.camera_shake.start()
            else:
                self.pickable = False
        for elem in self.emitters:
            elem.update()
            if elem.can_reap():
                self.emitters.remove(elem)
        for elem in self.t_e:
            self.t_e[0].center_x = self.player[0].center_x
            self.t_e[0].center_y = self.player[0].center_y
            elem.update()
        self.enemies.update(delta_time, self.player[0].center_x, self.player[0].center_y)
        self.bar.update(delta_time, self.world_camera.position)
        #self.shield.update(delta_time, self.player[0].center_x, self.player[0].center_y)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.E:
            if self.pickable:
                self.emitters.append(self.collect_eff(self.ex_keys[0].center_x, self.ex_keys[0].center_y))
                self.ex_keys[0].pickup()
                self.ex_key_count += 1
        self.keys.append(symbol)
    
    def on_key_release(self, symbol, modifiers):
        del self.keys[self.keys.index(symbol)]
    
    #def on_mouse_press(self, x, y):
    #    self.shield[0].r(x, y, self.player[0].center_x, self.player[0].center_y)
    
    def collect_eff(self, x, y, count=40, radius=5.0):
        return Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(count),
            particle_factory=lambda x: FadeParticle(
                filename_or_texture=arcade.make_soft_square_texture(10, arcade.color.GRAY, 255, 255),
                change_xy=arcade.math.rand_on_circle((0.0, 0.0), radius),
                lifetime=random.uniform(0.5, 0.9),
                start_alpha=255, end_alpha=0,
                scale=random.uniform(0.5, 1.4),
                
            )
        )
    def trail(self, x, y, count=40):
        return Emitter(
            center_xy=(x, y),
            emit_controller=EmitMaintainCount(count),
            particle_factory=lambda x: FadeParticle(
                filename_or_texture=arcade.make_soft_square_texture(10, arcade.color.GHOST_WHITE, 255, 255),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 2.2),
                lifetime=random.uniform(0.35, 0.6),
                start_alpha=255, end_alpha=255,
                scale=random.uniform(0.25, 0.4)
            )
        )
    
    
            
def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 100)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()