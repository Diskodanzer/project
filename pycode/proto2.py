import arcade
import random

# Параметры экрана
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Клетчатое поле"

class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)


        self.cell_size = cell_size
        self.rows = screen_height // cell_size  # строки (по вертикали)
        self.cols = screen_width // cell_size   # столбцы (по горизонтали)

        # Создаём пустую сетку
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        # Стартовая позиция — левый нижний угол
        self.current_row = 0  # нижняя строка
        self.current_col = 0              # левый столбец
        self.grid[self.current_row][self.current_col] = 1

        # Список направлений: вверх, вправо, вниз, влево
        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        # Флаг для остановки генерации, когда некуда идти
        self.generation_done = False

    def setup(self):
        pass

    def on_update(self, delta_time):
        """Начинаем генерировать случайный маршрут"""
        """Генерируем один шаг маршрута при каждом вызове"""
        #if self.generation_done:
        #    return

        # Собираем возможные направления (чтобы не выйти за границы и не зайти в уже занятую клетку)
        possible_moves = [1]
        '''for d_row, d_col in self.directions:
            new_row = self.current_row + d_row
            new_col = self.current_col + d_col
            # Проверяем границы и пустоту клетки
            if (0 <= new_row < self.rows and 
                0 <= new_col < self.cols and
                self.grid[new_row][new_col] == 0):
                possible_moves.append((new_row, new_col))'''

        if possible_moves:
            # Выбираем случайное направление
            self.current_row, self.current_col = random.choice(possible_moves)
            self.grid[self.current_row][self.current_col] = 1
       # else:
        #    # Никуда нельзя пойти — завершаем генерацию
        #    self.generation_done = True
        #    print("Маршрут завершён. Дальнейшее движение невозможно.")

    def on_draw(self):
        # Рисуем сетку
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * self.cell_size + self.cell_size // 2
                y = row * self.cell_size + self.cell_size // 2

                if self.grid[row][col] == 1:
                    color = arcade.color.LIGHT_GRAY
                    arcade.draw_rect_filled(
                        arcade.rect.XYWH(x, y, self.cell_size, self.cell_size),
                        color
                    )

def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    arcade.run()

if __name__ == "__main__":
    main()
