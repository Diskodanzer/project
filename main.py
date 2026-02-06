import arcade
from pycode.Windows import MainWindow


if __name__ == "__main__":
    #window.switch_view("start")
    
    window = arcade.Window(
        800,
        800,
        "Vymluva",
        resizable=False
    )

    menu_view = MainWindow(800, 800)
    
    window.show_view(menu_view)
    window.center_window()

    arcade.run()