import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox  # Это разные виджеты
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  # А это менеджеры компоновки, как в pyQT
# from prototype import GridGame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MainWindow(arcade.Window):
    def __init__(self, x=800, y=600):
        self.x = x
        self.y = y
        super().__init__(self.x, self.y, "vymluva")
        arcade.set_background_color(arcade.color.BLACK)


        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)



    def setup_widgets(self):
        label = UILabel(text="Vymluva",
                        font_size=50,
                        text_color=arcade.color.RED,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        flat_button = UIFlatButton(text="Начать", width=200, height=50, color=arcade.color.RED)
        flat_button.on_click = lambda event: self.open_game()
        self.box_layout.add(flat_button)

        flat_button1 = UIFlatButton(text="Настройки", width=200, height=50, color=(0, 0, 0))
        flat_button1.on_click = lambda event: self.open_settings()
        self.box_layout.add(flat_button1)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass

    def on_button_clicked(self):
        pass

    def open_game(self):
        game = GridGame(self.x, self.y)
        self.window.show_view(game)

    def open_settings(self):
        win = SettingsWindow(self.x, self.y)
        self.show_view(win)

class SettingsWindow(arcade.Window):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        super().__init__(self.x, self.y, "vymluva: настройки")
        arcade.set_background_color(arcade.color.BLACK)


        self.manager = UIManager()
        self.manager.enable()
        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)
        self.setup_widgets()

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)



    def setup_widgets(self):
        label = UILabel(text="Настройки",
                        font_size=50,
                        text_color=arcade.color.RED,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        label = UILabel(text="Размер экрана",
                        font_size=30,
                        text_color=arcade.color.RED,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        dropdown = UIDropdown(options=["1080 x 720", "800 x 600", "1440 x 1080"], width=200)
        dropdown.on_change = lambda value: self.xy(str(value).split(' x '))
        self.box_layout.add(dropdown)

        flat_button1 = UIFlatButton(text="Назад", width=200, height=50, color=(0, 0, 0))
        flat_button1.on_click = lambda event: self.open_game()  # Не только лямбду, конечно
        self.box_layout.add(flat_button1)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass
    
    def xy(self, mass):
        self.x = mass[0]
        self.y = mass[1]

    def open_game(self):
        game = MainWindow(self.x, self.y)
        self.window.show_view(game)


def main():
    window = MainWindow()
    window.run()
    arcade.run()


if __name__ == "__main__":
    main()