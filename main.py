import arcade
from pycode.basewindow import BaseWindow


if __name__ == "__main__":
    window = BaseWindow()

    window.switch_view("start")

    arcade.run()
