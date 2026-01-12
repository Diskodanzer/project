import arcade
import sys
import random
import pprint
from character import Character
from wall import Wall
sys.setrecursionlimit(10000)

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Клетчатое поле"


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)

        self.world_camera = arcade.camera.Camera2D()
        self.cell_size = cell_size
        self.rows = 1200 // cell_size
        self.cols = 1200 // cell_size
        self.painted = 0
        self.player = arcade.SpriteList()
        self.walls = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=cell_size*4) #1.создать класс стены, 2.Найти текстуру, 3.Подключить к проекту
        self.keys = []

        # Создаём пустую сетку нужного размера
        self.grid = None
        #self.setup()
    
    def check(self, row, col):
        if row <= 0 or row >= self.rows or col <= 0 or col >= self.cols:
            return False
        
        # Проверяем, что клетка пуста
        if self.grid[row][col] != 0:
            return False
        
        # Проверяем соседей (не больше 2 занятых соседей из 8)
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
        self.player.append(Character(1200, 1200, 0.25, 100, self.painted[0][0] * self.cell_size  + self.cell_size // 2, self.painted[0][1] * self.cell_size + self.cell_size // 2))
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
        #pprint.pprint(self.grid)
        #pprint.pprint(self.painted)
                
    def on_draw(self):
        self.clear()
        # Рисуем сетку
        self.world_camera.use()
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2
                if self.grid[row][col] == 1:
                    color = arcade.color.LIGHT_GRAY
                    arcade.draw_rect_filled(arcade.rect.XYWH(x, y,
                                            self.cell_size,
                                            self.cell_size),
                                            color)
        self.player.draw()
        self.walls.draw()
    
    def on_update(self, delta_time):
        for elem in self.player:
            elem.update(delta_time, self.keys)
        self.physics.update()
        self.world_camera.position = arcade.math.lerp_2d(
            self.world_camera.position,
            (self.player[0].center_x,
            self.player[0].center_y),
            0.12
        )
    
    def on_key_press(self, symbol, modifiers):
        self.keys.append(symbol)
    
    def on_key_release(self, symbol, modifiers):
        del self.keys[self.keys.index(symbol)]
    
            
def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()