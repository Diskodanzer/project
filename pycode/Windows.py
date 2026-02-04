import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel, UIAnchorLayout, UIBoxLayout, UIDropdown

from prototype import GridGame

x = 800
y = 800


class MainWindow(arcade.View):
    def __init__(self, x=800, y=600):
        super().__init__()
        self.manager = UIManager()
        self.anchor_layout = None
        self.box_layout = None
        self.x = x
        self.y = y

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.create_ui()

    def create_ui(self):
        self.manager.disable()
        self.manager.clear()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=15)

        label = UILabel(
            text="Vymluva",
            font_size=50,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        self.box_layout.add(label)

        start_button = UIFlatButton(
            text="Начать",
            width=200,
            height=50,
            color=arcade.color.WHITE
        )
        start_button.on_click = lambda event: self.open_game()
        self.box_layout.add(start_button)

        texture_normal = arcade.load_texture(":resources:/gui_basic_assets/button/red_normal.png")
        texture_hovered = arcade.load_texture(":resources:/gui_basic_assets/button/red_hover.png")
        texture_pressed = arcade.load_texture(":resources:/gui_basic_assets/button/red_press.png")
        texture_button = UITextureButton(texture=texture_normal, 
                                        texture_hovered=texture_hovered,
                                        texture_pressed=texture_pressed,
                                        scale=1.0)

        settings_button = UIFlatButton(
            text="Настройки",
            width=200,
            height=50,
            color=arcade.color.GRAY
        )
        settings_button.on_click = lambda event: self.open_settings()
        self.box_layout.add(settings_button)

        self.anchor_layout.add(
            child=self.box_layout,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager.add(self.anchor_layout)

    # def on_hide_view(self):
    #     self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def open_game(self):
<<<<<<< Updated upstream
        game = GridGame(800, 800, 'Game', 100)
        game.setup()
        game.center_window()
=======
        game = GridGame(self.x, self.y, 'vymluva', 10)
>>>>>>> Stashed changes
        self.window.show_view(game)

    def open_settings(self):
        settings_view = SettingsWindow(self)
        self.window.show_view(settings_view)

    def update_window_size(self, width, height):
        self.x = width
        self.y = height
        self.window.set_size(width, height)
        self.create_ui()


class SettingsWindow(arcade.View):

    def __init__(self, menu_view):
        super().__init__()
        self.menu_view = menu_view
        self.manager = UIManager()
        self.anchor_layout = None
        self.box_layout = None

        self.current_width = self.window.width
        self.current_height = self.window.height
        self.new_width = self.current_width
        self.new_height = self.current_height

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.create_ui()

    def create_ui(self):
        self.manager.disable()
        self.manager.clear()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=15)

        title = UILabel(
            text="Настройки",
            font_size=50,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        self.box_layout.add(title)

        size_label = UILabel(
            text=f"Текущий размер: {self.current_width} x {self.current_height}",
            font_size=20,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        self.box_layout.add(size_label)

<<<<<<< Updated upstream
        resolution_options = ["800 x 800", "1024 x 1024", "1280 x 1280", "1080 x 1080"]
=======
        resolution_options = ["800 x 800", "1024 x 1024", "1280 x 1280", "1920 x 1920"]
>>>>>>> Stashed changes

        current_res = f"{self.current_width} x {self.current_height}"
        if current_res not in resolution_options:
            resolution_options.insert(0, current_res)

        dropdown = UIDropdown(
            options=resolution_options,
            width=200,
            default=current_res
        )
        dropdown.on_change = self.on_resolution_changed
        self.box_layout.add(dropdown)

        # fps_button = UIFlatButton(
        #     text="Счётчик фпс",
        #     width=200,
        #     height=50,
        #     color=arcade.color.GREEN
        # )
        # fps_button.on_click = self.fps_clicked
        # self.box_layout.add(fps_button)

        apply_button = UIFlatButton(
            text="Применить и вернуться",
            width=200,
            height=50,
            color=arcade.color.GREEN
        )
        apply_button.on_click = self.on_apply_button_click
        self.box_layout.add(apply_button)

        back_button = UIFlatButton(
            text="Назад без сохранения",
            width=200,
            height=50,
            color=arcade.color.RED
        )
        back_button.on_click = self.on_back_button_click
        self.box_layout.add(back_button)

        self.anchor_layout.add(
            child=self.box_layout,
            anchor_x="center",
            anchor_y="center"
        )
        self.manager.add(self.anchor_layout)

    def on_hide_view(self):
        self.manager.disable()

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_resolution_changed(self, event):
        try:
            value = event.new_value
            width_str, height_str = str(value).split(' x ')
            self.new_width = int(width_str)
            self.new_height = int(height_str)
            print(f"Выбрано разрешение: {self.new_width}x{self.new_height}")
        except (ValueError, AttributeError, TypeError) as e:
            print(f"Ошибка при разборе разрешения: {e}")
            self.new_width = self.current_width
            self.new_height = self.current_height

    def on_apply_button_click(self, event):
        self.apply_settings()

    def on_back_button_click(self, event):
        self.go_back()

    def apply_settings(self):
        if (self.new_width != self.current_width or
                self.new_height != self.current_height):

            self.window.set_size(self.new_width, self.new_height)
            self.window.center_window()

            self.menu_view.update_window_size(self.new_width, self.new_height)
            print(f"Размер окна изменен на: {self.new_width}x{self.new_height}")
        else:
            print("Размер не изменился")

        self.window.show_view(self.menu_view)

    def go_back(self):
        self.window.show_view(self.menu_view)


def main():
    window = arcade.Window(
        x,
        y,
        "Vymluva",
        resizable=False
    )

    menu_view = MainWindow(x, y)
    
    window.show_view(menu_view)
    window.center_window()

    arcade.run()


if __name__ == "__main__":
    main()