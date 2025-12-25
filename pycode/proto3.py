import arcade
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Клетчатое поле"

class GridGame(arcade.Window):
    def __init__(self, screen_width, screen_height, screen_title, cell_size):
        super().__init__(screen_width, screen_height, screen_title)

        self.cell_size = cell_size
        self.rows = screen_height // cell_size
        self.cols = screen_width // cell_size

        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.start_row = self.rows - 1
        self.start_col = 0
        self.target_row = 0
        self.target_col = self.cols - 1

        self.current_row = self.start_row
        self.current_col = self.start_col
        self.grid[self.current_row][self.current_col] = 1

        self.directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        
        self.generation_done = False

    def setup(self):
        self.generate_route()

    def generate_route(self):
        while not self.generation_done:
            if (self.current_row == self.target_row and 
                self.current_col == self.target_col):
                self.generation_done = True
                print("Маршрут успешно построен до цели!")
                break

            possible_moves = []
            for d_row, d_col in self.directions:
                new_row = self.current_row + d_row
                new_col = self.current_col + d_col
                
                if (0 <= new_row < self.rows and
                    0 <= new_col < self.cols and
                    self.grid[new_row][new_col] == 0):
                    
                    distance_to_target = abs(new_row - self.target_row) + abs(new_col - self.target_col)
                    current_distance = abs(self.current_row - self.target_row) + abs(self.current_col - self.target_col)
                    
                    if distance_to_target < current_distance:
                        possible_moves.extend([(new_row, new_col)] * 2)
                    else:
                        possible_moves.append((new_row, new_col))

            if possible_moves:
                self.current_row, self.current_col = random.choice(possible_moves)
                self.grid[self.current_row][self.current_col] = 1
            else:
                self.find_alternative_path()

    def find_alternative_path(self):
        occupied_cells = []
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == 1:
                    occupied_cells.append((row, col))
        
        for row, col in reversed(occupied_cells):
            for d_row, d_col in self.directions:
                new_row = row + d_row
                new_col = col + d_col
                
                if (0 <= new_row < self.rows and
                    0 <= new_col < self.cols and
                    self.grid[new_row][new_col] == 0):
                    
                    self.current_row, self.current_col = row, col
                    return 
        
        self.generation_done = True

    def on_draw(self):

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
                arcade.draw_rect_outline(
                    arcade.rect.XYWH(x, y, self.cell_size - 2, self.cell_size - 2),
                    arcade.color.BLACK, 1
                )

        start_x = self.start_col * self.cell_size + self.cell_size // 2
        start_y = self.start_row * self.cell_size + self.cell_size // 2
        arcade.draw_circle_filled(start_x, start_y, self.cell_size * 0.3, arcade.color.GREEN)

        target_x = self.target_col * self.cell_size + self.cell_size // 2
        target_y = self.target_row * self.cell_size + self.cell_size // 2
        arcade.draw_circle_filled(target_x, target_y, self.cell_size * 0.3, arcade.color.RED)

def main():
    game = GridGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, 40)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
