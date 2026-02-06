import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox 
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Супер GUI Пример!")
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
        dropdown.on_change = lambda value: print(f"Выбрано: {value}")
        self.box_layout.add(dropdown)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        pass 

    def on_button_clicked(self):
        pass

    def open_game(self):
        print('fg')

    def open_settings(self):
        print('settings')


def main():
    window = MainWindow()
    window.run()
    arcade.run()


if __name__ == "__main__":
    main()