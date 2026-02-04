import arcade
from pycode.Windows import MainWindow


if __name__ == "__main__":
    window = MainWindow()

    window.switch_view("start")

    arcade.run()
