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
from sphere import Sphere
from exit import Exit
from arcade.particles import EmitBurst, Emitter, FadeParticle, EmitMaintainCount
from load_window import LoadingWindow
import threading
sys.setrecursionlimit(10000)

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Game"


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title, fullscreen=False, resizable=True)

        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.zoom = 1.0
        self.cell_size = cell_size
        self.points_to_end = 3   #Механика с кол-вом лабиринтов, которое нужно будет пройти, чтобы дойти до концовки
        self.cell_size = cell_size
        self.rows = 3000 // cell_size
        self.cols = 3000 // cell_size
        self.painted = 0
        self.player = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=self.cell_size*4) 
        self.ex_keys = arcade.SpriteList()
        self.keys = set()
        self.ex_key_count = 0
        self.pickable = False
        self.emitters = []
        self.t_e = [] #trail_effect(для персонажа)
        self.ex_e = None
        self.exit = arcade.SpriteList() # Сделать логику выхода с уровня
        self.path = arcade.SpriteList()
        self.custom = arcade.SpriteList()
        self.grid = None
        self.enemies = arcade.SpriteList()
        self.shield = None
        self.camera_shake = arcade.camera.grips.ScreenShake2D(   #спросить что тут не так
            self.world_camera.view_data,  
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )
        self.spheres = arcade.SpriteList()
        self.exit = None
        self.is_loaded = False
        
        self.grow = False
        self.star = arcade.SpriteList()
        star = arcade.Sprite()
        arcade.texture = arcade.load_texture('recources/star.png')
        star.scale = 0.5
        star.center_x = self.width / 2
        star.center_y = self.height / 2
        self.star.append(star)
        self.start_loading_thread()
        self.tex = arcade.load_texture('recources\СharacterSprite.png')

    def start_loading_thread(self):
        """Запускаем setup() в отдельном потоке"""
        import threading
        
        def thread_target():
            # ВСЯ ЗАГРУЗКА ЗДЕСЬ
            self.setup()  # <-- Вызываем наш setup
            
            # Когда всё загружено
            #self.game_state = "PLAYING"
            print("Загрузка завершена!")
        
        # Создаем и запускаем поток
        thread = threading.Thread(target=thread_target)
        thread.daemon = True  # Поток завершится с программой
        thread.start()

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
        self.player.append(Character(3000, 3000, 0.14, 200, self.painted[0][0] * self.cell_size  + self.cell_size // 2, self.painted[0][1] * self.cell_size + self.cell_size // 2, self.tex))
        self.bar = Bar(self.player[0].center_x, self.player[0].center_y - 350, 10)
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
        #self.shield.append(Shield(self.player[0].center_x, self.player[0].center_y))
        y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        if self.grid[y][x] == 0:
            while self.grid[y][x] == 0:
                y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self.ex_keys.append(Key(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2, 0.15))
        
        y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        if self.grid[y][x] == 0:
            while self.grid[y][x] == 0:
                y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
        self.exit = Exit(x, y)
                
        for i in range(15):
            y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[y][x] == 0:
                while self.grid[y][x] == 0:
                    y, x = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            self.spheres.append(Sphere(x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2))
        '''for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                if self.grid[row][col] == 1:
                    rect = arcade.Sprite()
                    rect.texture = arcade.load_texture('recources/path.png')
                    rect.scale = 1.0
                    rect.center_x = x
                    rect.center_y = y
                    self.path.append(rect)'''
        self.shield = Shield(self.player[0].center_x, self.player[0].center_y)
        self.is_loaded = True
        print('Загрузилось!')
        #pprint.pprint(self.grid)
        #pprint.pprint(self.painted)
                
    def on_draw(self):
        self.clear()
        if self.is_loaded:
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
            self.spheres.draw()
            self.custom.draw()
            self.bar.draw()
            self.shield.draw()
            self.exit.draw()
        else:
            arcade.draw_rect_filled(arcade.rect.XYWH(self.width / 2, self.height / 2, self.width, self.height), arcade.color.BLACK)
            self.star.draw()
        
    
    def on_update(self, delta_time):
        if self.is_loaded:
            for elem in self.player:
                elem.update(delta_time, self.keys)
            self.physics.update()
            self.camera_shake.start()
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
                else:
                    self.pickable = False
            for elem in self.emitters:
                elem.update()
                if elem.can_reap():
                    self.emitters.remove(elem)
            for elem in self.t_e:
                elem.center_x = self.player[0].center_x
                elem.center_y = self.player[0].center_y
                elem.update()
            self.enemies.update(delta_time, self.player[0].center_x, self.player[0].center_y)
            self.bar.update(delta_time, self.world_camera.position)
            #self.shield.update(delta_time, self.player[0].center_x, self.player[0].center_y)
            coll_sph = arcade.check_for_collision_with_list(self.player[0], self.spheres)
            if coll_sph:
                for elem in coll_sph:
                    elem.remove_from_sprite_lists()
                    self.emitters.append(self.collect_eff(elem.center_x, elem.center_y))
                    self.bar.stretch()
            if self.bar.width <= 0:
                self.custom[0].scale = 0.115
                self.world_camera.zoom = 2.2
            else:  
                self.custom[0].scale = 0.23
                self.world_camera.zoom = 1.0
            self.shield.update(self.player[0].center_x, self.player[0].center_y)
            if arcade.key.SPACE in self.keys:
                self.shield.adjust(delta_time)
                for elem in self.enemies:
                    if abs(self.player[0].center_x - elem.center_x) <= 85 and abs(self.player[0].center_y - elem.center_y) <= 85:
                        elem.knockback()
            else:
                self.shield.disappear()
            self.exit.update(delta_time)
            if abs(self.exit.x - self.player[0].center_x) <= 25 and abs(self.exit.y - self.player[0].center_y) <= 25:
                self.painted = 0
                self.player = arcade.SpriteList()
                self.walls = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=self.cell_size*4) 
                self.ex_keys = arcade.SpriteList()
                self.keys = set()
                self.ex_key_count = 0
                self.pickable = False
                self.emitters = []
                self.t_e = [] #trail_effect(для персонажа)
                self.ex_e = None
                self.exit = arcade.SpriteList() # Сделать логику выхода с уровня
                self.path = arcade.SpriteList()
                self.custom = arcade.SpriteList()
                self.grid = None
                self.enemies = arcade.SpriteList()
                self.shield = None
                self.spheres = arcade.SpriteList()
                self.exit = None
                self.setup()
        else:
            if self.star[0].scale[0] >= 0.5:
                self.grow = False
            if not self.grow:
                self.star[0].scale = (self.star[0].scale[0] + 0.1 * delta_time, self.star[0].scale[1] + 0.1 * delta_time)
            if self.star[0].scale[0] >= 0.15 and not self.grow:
                self.star[0].scale = (self.star[0].scale[0] - 0.1 * delta_time, self.star[0].scale[1] - 0.1 * delta_time)
            else:
                self.grow = True
    
    
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.E and self.ex_keys:
            if self.pickable:
                self.emitters.append(self.collect_eff(self.ex_keys[0].center_x, self.ex_keys[0].center_y))
                self.ex_keys[0].pickup()
                self.exit.appear = True
                self.ex_key_count += 1
                for i in range(10):
                    self.enemies.append(Enemy(random.randint(100, 2900), random.randint(100, 2900), 100))
        if symbol == arcade.key.ESCAPE:
            self.close()
        self.keys.add(symbol)
    
    def on_key_release(self, symbol, modifiers):
       self.keys.remove(symbol)
    
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
    #game.setup()
    arcade.run()

if __name__ == "__main__":
    main()