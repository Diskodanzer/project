import math
import arcade
import sys
import random
import pprint
import threading
import time
from queue import Queue
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
from ending_level import End_level
import json

# Параметры экрана
SCREEN_WIDTH = None
SCREEN_HEIGHT = None
with open('settings/settings.json', 'r') as f:
    data = json.load(f)
    SCREEN_WIDTH = data['curr_res_x']
    SCREEN_HEIGHT = data['curr_res_y']
SCREEN_TITLE = "Game"


class Game(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        
        self.is_loading = True
        self.loading_progress = 0
        self.loading_text = "Генерация мира..."
        self.loading_thread = None
        self.load_timer = 0
        self.last_update_time = 0

        self.progress_queue = Queue()
        
        self.cell_size = cell_size
        self.points_to_end = 3
        self.rows = 3000 // cell_size
        self.cols = 3000 // cell_size
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.tex = None
        
        super().__init__(screen_width, screen_height, 'game')
        
        self.world_camera = arcade.camera.Camera2D()
        self.world_camera.zoom = 1.0
        self.background_music = arcade.load_sound('recources/music.wav')
        self.initialize_game_objects()
        
        self.star_list = arcade.SpriteList()
        self.star = arcade.Sprite('recources/star.png', scale=0.1)
        self.star.center_x = self.screen_width / 2
        self.star.center_y = self.screen_height / 2
        self.star_list.append(self.star)
        self.star_angle = 0
        self.star_pulse = 0
        self.star_growing = True
        self.star_pulse_speed = 2.0
        

    def initialize_game_objects(self):
        """Инициализирует пустые списки и объекты для игры"""
        self.painted = 0
        self.player = arcade.SpriteList()
        self.walls = arcade.SpriteList(
            use_spatial_hash=True, spatial_hash_cell_size=self.cell_size*4)
        self.ex_keys = arcade.SpriteList() #ключ для открытия вфхода
        self.keys = set()
        self.ex_key_count = 3
        self.pickable = False
        self.emitters = []
        self.t_e = []  #эффект трейла за игроком
        self.ex_e = None #эффект для выхода
        self.path = arcade.SpriteList()
        self.custom = arcade.SpriteList()
        self.grid = None
        self.enemies = arcade.SpriteList()
        self.shield = None
        self.spheres = arcade.SpriteList()
        self.exit = None
        self.timer = 0.0

        self.camera_shake = arcade.camera.grips.ScreenShake2D(
            self.world_camera.view_data,
            max_amplitude=15.0,
            acceleration_duration=0.1,
            falloff_time=0.5,
            shake_frequency=10.0,
        )

        self.bar = None
        self.physics = None

    def on_show(self):
        """Окно показано - начинаем загрузку в фоновом потоке"""
        
        if self.is_loading and not self.loading_thread:
            self.loading_thread = threading.Thread(
                target=self.setup_in_thread, daemon=True)
            self.loading_thread.start()

    def setup_in_thread(self):
        """Загрузка уровня в фоновом потоке"""
        try:
            self.update_progress("Генерация карты...", 0.1)

            self.grid = [[0 for _ in range(self.cols)]
                         for _ in range(self.rows)]
            self.grid[self.rows // 2 - 1][self.cols // 2 - 1] = 1
            self.painted = [[self.rows // 2 - 1, self.cols // 2 - 1]]
            self.prev = []

            iterations = 0
            while self.prev != self.painted:
                self.prev = self.painted
                self.painted = self.check_for_directions(self.painted)
                iterations += 1

                if iterations % 10 == 0:
                    progress = 0.1 + min(0.2, iterations / 1000 * 0.2)
                    self.update_progress("Генерация карты...", progress)

            self.update_progress("Создание персонажа...", 0.35)
            time.sleep(0.01)

            self.progress_queue.put(('load_texture', None))

            while self.tex is None:
                time.sleep(0.01)

            start_x = self.painted[0][0] * self.cell_size + self.cell_size // 2
            start_y = self.painted[0][1] * self.cell_size + self.cell_size // 2

            self.progress_queue.put(('create_player', (start_x, start_y)))

            self.update_progress("Создание стен...", 0.4)

            batch_size = 50
            total_cells = self.rows * self.cols

            walls_batch = []
            for row in range(self.rows):
                for col in range(self.cols):
                    if self.grid[row][col] != 1:
                        x = col * self.cell_size + self.cell_size // 2
                        y = row * self.cell_size + self.cell_size // 2
                        walls_batch.append((x, y))

                    if len(walls_batch) >= batch_size or (row == self.rows - 1 and col == self.cols - 1):
                        if walls_batch:
                            self.progress_queue.put(('add_walls', walls_batch))
                            walls_batch = []

                        progress = 0.4 + 0.2 * \
                            (row * self.cols + col) / total_cells
                        self.update_progress(
                            "Создание стен...", min(0.6, progress))

            self.update_progress("Настройка физики...", 0.65)
            time.sleep(0.01)

            self.progress_queue.put(('create_physics_ui', (start_x, start_y)))

            self.update_progress("Размещение объектов...", 0.75)
            time.sleep(0.01)

            y, x = random.randint(
                0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[y][x] == 0:
                while self.grid[y][x] == 0:
                    y, x = random.randint(
                        0, self.rows - 1), random.randint(0, self.cols - 1)
            key_pos = (x * self.cell_size + self.cell_size // 2,
                       y * self.cell_size + self.cell_size // 2, 0.15)
            self.progress_queue.put(('add_key', key_pos))

            y, x = random.randint(
                0, self.rows - 1), random.randint(0, self.cols - 1)
            if self.grid[y][x] == 0:
                while self.grid[y][x] == 0:
                    y, x = random.randint(
                        0, self.rows - 1), random.randint(0, self.cols - 1)
            self.progress_queue.put(('add_exit', (x * self.cell_size + self.cell_size // 2, y * self.cell_size + self.cell_size // 2)))

            self.update_progress("Размещение сфер...", 0.85)

            spheres_batch = []
            for i in range(15):
                y, x = random.randint(
                    0, self.rows - 1), random.randint(0, self.cols - 1)
                if self.grid[y][x] == 0:
                    while self.grid[y][x] == 0:
                        y, x = random.randint(
                            0, self.rows - 1), random.randint(0, self.cols - 1)
                spheres_batch.append((x * self.cell_size + self.cell_size // 2,
                                     y * self.cell_size + self.cell_size // 2))

                if i % 3 == 0 or i == 14:
                    if spheres_batch:
                        self.progress_queue.put(('add_spheres', spheres_batch))
                        spheres_batch = []

                    progress = 0.85 + 0.1 * (i / 15)
                    self.update_progress("Размещение сфер...", progress)

            self.update_progress("Завершение загрузки...", 0.95)
            time.sleep(0.01)

            self.progress_queue.put(('create_shield', None))

            self.update_progress("Готово!", 1.0)
            time.sleep(0.5)

            self.progress_queue.put(('finish_loading', None))

        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            import traceback
            traceback.print_exc()
            self.update_progress(f"Ошибка: {str(e)}", 1.0)

    def update_progress(self, text, progress):
        """Обновляет прогресс загрузки (вызывается из фонового потока)"""
        self.progress_queue.put(('progress', (text, progress)))

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

    def on_draw(self):
        self.clear()

        if self.is_loading:
            arcade.draw_lrbt_rectangle_filled(
                left=0,
                right=self.screen_width,
                top=self.screen_height,
                bottom=0,
                color=arcade.color.BLACK
            )

            self.star_list.draw()

            bar_width = 400
            bar_height = 30
            bar_x = self.screen_width / 2 - bar_width / 2
            bar_y = self.screen_height / 2 - 100

            arcade.draw_lbwh_rectangle_filled(
                bar_x, bar_y, bar_width, bar_height,
                arcade.color.DARK_GRAY
            )

            progress_width = bar_width * self.loading_progress
            color = arcade.color.BLUEBERRY

            if self.loading_progress < 1.0:
                pulse = (math.sin(time.time() * 5) + 1) / \
                    2 
                color = (
                    int(color[0] * (0.7 + pulse * 0.3)),
                    int(color[1] * (0.7 + pulse * 0.3)),
                    int(color[2] * (0.7 + pulse * 0.3))
                )

            arcade.draw_lbwh_rectangle_filled(
                bar_x, bar_y, progress_width, bar_height,
                color
            )

            arcade.draw_text(
                self.loading_text,
                self.screen_width / 2, bar_y + 50,
                arcade.color.WHITE, font_size=24,
                anchor_x="center", anchor_y="center",
                bold=True
            )

            arcade.draw_text(
                f"{int(self.loading_progress * 100)}%",
                self.screen_width / 2, bar_y - 40,
                arcade.color.WHITE, font_size=20,
                anchor_x="center", anchor_y="center"
            )

            arcade.draw_text(
                "Пожалуйста, подождите...",
                self.screen_width / 2, bar_y - 80,
                arcade.color.LIGHT_GRAY, font_size=16,
                anchor_x="center", anchor_y="center"
            )
        else:
            self.world_camera.use()
            self.camera_shake.update_camera()
            self.path.draw()
            self.player.draw()
            if self.t_e:
                self.t_e[0].draw()
            self.walls.draw()
            self.ex_keys.draw()
            for elem in self.emitters:
                elem.draw()
            self.camera_shake.readjust_camera()
            self.enemies.draw()
            self.spheres.draw()
            self.custom.draw()
            if self.bar:
                self.bar.draw()
            if self.shield:
                self.shield.draw()
            if self.exit:
                self.exit.draw()

    def on_update(self, delta_time):
        self.process_queue()

        if self.is_loading:
            self.load_timer += delta_time
            self.star_angle += delta_time * 60
            self.star.angle = self.star_angle
            if self.star_growing:
                self.star_pulse += delta_time * self.star_pulse_speed
                if self.star_pulse >= 1.0:
                    self.star_growing = False
            else:
                self.star_pulse -= delta_time * self.star_pulse_speed
                if self.star_pulse <= 0.0:
                    self.star_growing = True

            self.star.scale = 0.1 + self.star_pulse * 0.1
            angle_rad = math.radians(self.load_timer * 20)
            self.star.center_x = self.screen_width / 2 + math.cos(angle_rad) * 10
            self.star.center_y = self.screen_height / \
                2 + math.sin(angle_rad * 0.75) * 10
        else:
            for elem in self.player:
                elem.update(delta_time, self.keys)

            if self.physics:
                self.physics.update()

            self.camera_shake.start()
            self.camera_shake.update(delta_time)

            if self.custom:
                self.custom[0].movement(
                    delta_time, self.player[0].center_x, self.player[0].center_y)

            current_x, current_y = self.world_camera.position
            target_x, target_y = self.player[0].center_x, self.player[0].center_y

            new_x = current_x + (target_x - current_x) * 0.12
            new_y = current_y + (target_y - current_y) * 0.12
            self.world_camera.position = (new_x, new_y)

            if self.ex_keys:
                self.ex_keys[0].update_animation(delta_time)
                coll = arcade.check_for_collision_with_list(
                    self.player[0], self.ex_keys)
                self.pickable = bool(coll)

            for elem in self.emitters[:]:
                elem.update()
                if elem.can_reap():
                    self.emitters.remove(elem)

            if self.t_e:
                self.t_e[0].center_x = self.player[0].center_x
                self.t_e[0].center_y = self.player[0].center_y
                self.t_e[0].update()

            self.enemies.update(
                delta_time, self.player[0].center_x, self.player[0].center_y)

            if self.bar:
                self.bar.update(delta_time, self.world_camera.position)

            coll_sph = arcade.check_for_collision_with_list(
                self.player[0], self.spheres)
            if coll_sph:
                for elem in coll_sph:
                    elem.remove_from_sprite_lists()
                    self.emitters.append(self.collect_eff(
                        elem.center_x, elem.center_y))
                    self.bar.stretch()

            if self.bar and self.bar.width <= 0:
                if self.custom:
                    self.custom[0].scale = 0.115
                self.world_camera.zoom = 2.2
            else:
                if self.custom:
                    self.custom[0].scale = 0.23
                self.world_camera.zoom = 1.0

            if self.shield:
                self.shield.update(
                    self.player[0].center_x, self.player[0].center_y)
                if arcade.key.SPACE in self.keys:
                    self.shield.adjust(delta_time)
                    for elem in self.enemies:
                        if abs(self.player[0].center_x - elem.center_x) <= 85 and abs(self.player[0].center_y - elem.center_y) <= 85:
                            elem.knockback()
                else:
                    self.shield.disappear()

            if self.exit:
                self.exit.update(delta_time)
                if abs(self.exit.x - self.player[0].center_x) <= 25 and abs(self.exit.y - self.player[0].center_y) <= 25:
                    self.reset_level()
            self.timer += delta_time
            self.coll_with_enemies = arcade.check_for_collision_with_list(self.player[0], self.enemies)
            if self.coll_with_enemies:
                self.reset_level()

    def process_queue(self):
        """Обрабатывает сообщения из очереди (только в основном потоке)"""
        while not self.progress_queue.empty():
            try:
                msg_type, data = self.progress_queue.get_nowait()

                if msg_type == 'progress':
                    self.loading_text, self.loading_progress = data

                elif msg_type == 'load_texture':
                    self.tex = arcade.load_texture(
                        'recources\\СharacterSprite.png')

                elif msg_type == 'create_player':
                    start_x, start_y = data
                    self.player.append(
                        Character(3000, 3000, 0.14, 200, start_x, start_y, self.tex))

                elif msg_type == 'add_walls':
                    for x, y in data:
                        wall = Wall(x, y)
                        self.walls.append(wall)

                elif msg_type == 'create_physics_ui':
                    start_x, start_y = data
                    self.physics = arcade.physics_engines.PhysicsEngineSimple(
                        self.player[0],
                        self.walls
                    )
                    self.bar = Bar(
                        self.player[0].center_x, self.player[0].center_y - 350, 10)
                    self.custom.append(
                        Custom(self.player[0].center_x, self.player[0].center_y))
                    self.t_e.append(self.trail(start_x, start_y))

                elif msg_type == 'add_key':
                    x, y, scale = data
                    self.ex_keys.append(Key(x, y, scale))

                elif msg_type == 'add_exit':
                    x, y = data
                    self.exit = Exit(x, y)

                elif msg_type == 'add_spheres':
                    for x, y in data:
                        self.spheres.append(Sphere(x, y))

                elif msg_type == 'create_shield':
                    if self.player:
                        self.shield = Shield(
                            self.player[0].center_x, self.player[0].center_y)

                elif msg_type == 'finish_loading':
                    self.is_loading = False
                    self.music_player = arcade.play_sound(self.background_music, volume=0.2, loop=True)
                    
            except Exception as e:
                print(f"Ошибка при обработке сообщения: {e}")

    def reset_level(self):
        """Сброс уровня для новой генерации"""
        self.is_loading = True
        self.loading_progress = 0
        if random.random() <= 0.5 and not self.coll_with_enemies:
            self.points_to_end -= 1
        if self.points_to_end <= 0:
            arcade.stop_sound(self.music_player)
            self.close()
            game = End_level(self.width, self.height, self.cell_size, self.timer)
            game.setup()
            arcade.run()
        self.loading_text = "Генерация нового уровня..."
        self.initialize_game_objects()
        self.loading_thread = threading.Thread(
            target=self.setup_in_thread, daemon=True)
        self.loading_thread.start()

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.E and self.ex_keys and not self.is_loading:
            if self.pickable:
                self.emitters.append(self.collect_eff(
                    self.ex_keys[0].center_x, self.ex_keys[0].center_y))
                self.ex_keys[0].pickup()
                if self.exit:
                    self.exit.appear = True
                self.ex_key_count += 1
                for i in range(10):
                    self.enemies.append(Enemy(random.randint(
                        100, 2900), random.randint(100, 2900), 100))

        if symbol == arcade.key.ESCAPE:
            self.close()

        self.keys.add(symbol)

    def on_key_release(self, symbol, modifiers):
        if symbol in self.keys:
            self.keys.remove(symbol)

    def collect_eff(self, x, y, count=40, radius=5.0):
        return Emitter(
            center_xy=(x, y),
            emit_controller=EmitBurst(count),
            particle_factory=lambda x: FadeParticle(
                filename_or_texture=arcade.make_soft_square_texture(
                    10, arcade.color.GRAY, 255, 255),
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
                filename_or_texture=arcade.make_soft_square_texture(
                    10, arcade.color.GHOST_WHITE, 255, 255),
                change_xy=arcade.math.rand_in_circle((0.0, 0.0), 2.2),
                lifetime=random.uniform(0.35, 0.6),
                start_alpha=255, end_alpha=255,
                scale=random.uniform(0.25, 0.4)
            )
        )



def main():
    """Главная функция"""
    window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, 'game', 100)
    arcade.run()


if __name__ == "__main__":
    main()