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

        # Создаём пустую сетку нужного размера
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.grid[0][0] = 1
        self.curr = [0, 0]
        self.setup()

    def setup(self):
        # Заполняем сетку случайными значениями
        #for i in range(self.rows):
        #    for j in range(self.cols):
        #        self.grid[i][j] = random.randint(0, 2)
        for row in range(self.rows):
            for col in range(self.cols):
                if row == self.curr[0] and col == self.curr[-1] + 1:
                    if random.choice([1, 0]):
                        self.grid[row][col] = 1
                        self.curr = [row, col]
                if row == self.curr[0] and col == self.curr[-1] - 1:
                    if random.choice([1, 0]) == 1:
                        self.grid[row][col] = 1
                        self.curr = [row, col]
                if row == self.curr[0] + 1 and col == self.curr[-1]:
                    if random.choice([1, 0]) == 1:
                        self.grid[row][col] = 1
                        self.curr = [row, col]
                if row == self.curr[0] - 1 and col == self.curr[-1]:
                    if random.choice([1, 0]) == 1:
                        self.grid[row][col] = 1
                        self.curr = [row, col]
        pprint.pprint(self.grid)
                         

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
                # Цвет в зависимости от значения в сетке
                #if self.grid[row][col] == 1:
                #    color = arcade.color.BLUE
                #if self.grid[row][col] == 2:
                #    color = arcade.color.RED
                #else:
                #    color = arcade.color.LIGHT_GRAY
                #arcade.draw_rect_filled(arcade.rect.XYWH(x, y,
                #                            self.cell_size,
                #                            self.cell_size),
                #                            color)
                # Для красоты рисуем границы, чтобы всё не сливалось
                #arcade.draw_rect_outline(arcade.rect.XYWH(x, y,
                #                             self.cell_size - 2,
                #                             self.cell_size - 2),
                #                             arcade.color.BLACK, 1)


def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()