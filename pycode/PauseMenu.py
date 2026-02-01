import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel, UIAnchorLayout, UIBoxLayout, UIDropdown

# from pycode.prototype import GridGame

from pycode.Windows import MainWindow

x = 800
y = 600


class PauseMenu(arcade.View):

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
        self.box_layout = UIBoxLayout(vertical=True, space_between=20)

        label = UILabel(
            text="Пауза",
            font_size=50,
            text_color=arcade.color.WHITE,
            width=300,
            align="center"
        )
        self.box_layout.add(label)

        start_button = UIFlatButton(
            text="Продолжить",
            width=200,
            height=50,
            color=arcade.color.WHITE
        )
        start_button.on_click = lambda event: self.cont()
        self.box_layout.add(start_button)

        settings_button = UIFlatButton(
            text="В главное меню",
            width=200,
            height=50,
            color=arcade.color.GRAY
        )
        settings_button.on_click = lambda event: self.open_menu()
        self.box_layout.add(settings_button)

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

    def cont(self):
        game = GridGame(self.x, self.y)
        self.window.show_view(game)

    def open_menu(self):
        settings_view = MainWindow(self)
        self.window.show_view(settings_view)

    def update_window_size(self, width, height):
        self.x = width
        self.y = height
        self.window.set_size(width, height)
        self.create_ui()


def main():
    window = arcade.Window(
        x,
        y,
        "Vymluva - Главное меню",
        resizable=True
    )

    menu_view = PauseMenu(x, y)
    window.show_view(menu_view)

    arcade.run()


if __name__ == "__main__":
    main()