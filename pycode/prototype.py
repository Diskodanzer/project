import arcade
import random
import pprint

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Клетчатое поле"


class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)

        self.cell_size = cell_size
        self.rows = screen_width // cell_size
        self.cols = screen_height // cell_size
        self.painted = 0

        # Создаём пустую сетку нужного размера
        self.grid = None
        self.setup()
    
    def check(self, row, col, ch):
        if ch == 'l':
            y = row
            x = col - 1
            
            return x >= 0 and self.grid[y][x] == 0 #and self.grid[y + 1][x] == 0 and self.grid[y - 1][x] == 0 and self.grid[y][x - 1] == 0
        if ch == 'r':
            return col + 1 < self.cols and self.grid[row][col + 1] == 0
        if ch == 'u':
            return row + 1 < self.rows and self.grid[row + 1][col] == 0
        if ch == 'd':
            return row - 1 >= 0 and self.grid[row - 1][col] == 0

    def setup(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        row, col = 0, 0
        self.grid[row][col] = 1
    
        steps = 100
        total = 0
    
        for _ in range(steps):
            directions = []
            if self.check(row, col, 'l'):
                directions.append(('l', row, col - 1))
            if self.check(row, col, 'r'):
                directions.append(('r', row, col + 1))
            if self.check(row, col, 'u'):
                directions.append(('u', row + 1, col))
            if self.check(row, col, 'd'):
                directions.append(('d', row - 1, col))
        
            if not directions:
                break
            total += 1
            
            ch, new_row, new_col = random.choice(directions)
        
            row, col = new_row, new_col
            self.grid[row][col] = 1
        if total < steps:
            self.setup()


    '''def setup(self):
        for row in range(self.rows):
            for col in range(self.cols):
                ch = random.choice(['l', 'r', 'd', 'u'])
                if ch == 'l':
                    if self.check(row, col, ch):
                        self.grid[row][col - 1] = 1
                        self.curr = [row, col - 1]
                    else:
                        while not self.check(row, col, ch):
                            ch = random.choice(['l', 'r', 'd', 'u'])
                        if ch == 'l':
                            self.grid[row][col - 1] = 1
                            self.curr = [row, col - 1]
                        if ch == 'r':
                            self.grid[row][col + 1] = 1
                            self.curr = [row, col + 1]
                        if ch == 'd':
                            self.grid[row - 1][col] = 1
                            self.curr = [row - 1, col]
                        if ch == 'u':
                            self.grid[row + 1][col] = 1
                            self.curr = [row + 1, col]
                if ch == 'r':
                    if self.check(row, col, ch):
                        self.grid[row][col + 1] = 1
                        self.curr = [row, col + 1]
                    else:
                        while not self.check(row, col, ch):
                            ch = random.choice(['l', 'r', 'd', 'u'])
                        if ch == 'l':
                            self.grid[row][col - 1] = 1
                            self.curr = [row, col - 1]
                        if ch == 'r':
                            self.grid[row][col + 1] = 1
                            self.curr = [row, col + 1]
                        if ch == 'd':
                            self.grid[row - 1][col] = 1
                            self.curr = [row - 1, col]
                        if ch == 'u':
                            self.grid[row + 1][col] = 1
                            self.curr = [row + 1, col]
                if ch == 'd':
                    if self.check(row, col, ch):
                        self.grid[row - 1][col] = 1
                        self.curr = [row - 1, col]
                    else:
                        while not self.check(row, col, ch):
                            ch = random.choice(['l', 'r', 'd', 'u'])
                        if ch == 'l':
                            self.grid[row][col - 1] = 1
                            self.curr = [row, col - 1]
                        if ch == 'r':
                            self.grid[row][col + 1] = 1
                            self.curr = [row, col + 1]
                        if ch == 'd':
                            self.grid[row - 1][col] = 1
                            self.curr = [row - 1, col]
                        if ch == 'u':
                            self.grid[row + 1][col] = 1
                            self.curr = [row + 1, col]
                if ch == 'u':
                    if self.check(row, col, ch):
                        self.grid[row + 1][col] = 1
                        self.curr = [row + 1, col]
                    else:
                        while not self.check(row, col, ch):
                            ch = random.choice(['l', 'r', 'd', 'u'])
                        if ch == 'l':
                            self.grid[row][col - 1] = 1
                            self.curr = [row, col - 1]
                        if ch == 'r':
                            self.grid[row][col + 1] = 1
                            self.curr = [row, col + 1]
                        if ch == 'd':
                            self.grid[row - 1][col] = 1
                            self.curr = [row - 1, col]
                        if ch == 'u':
                            self.grid[row + 1][col] = 1
                            self.curr = [row + 1, col]'''
                

    def on_draw(self):
        # Рисуем сетку
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

def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()