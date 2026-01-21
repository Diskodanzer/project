import arcade
from arcade.gui import UIManager, UIFlatButton, UITextureButton, UILabel, UIInputText, UITextArea, UISlider, UIDropdown, \
    UIMessageBox  # Это разные виджеты
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout  # А это менеджеры компоновки, как в pyQT

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class MainWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Супер GUI Пример!")
        arcade.set_background_color(arcade.color.BLACK)

        # UIManager — сердце GUI
        self.manager = UIManager()
        self.manager.enable()  # Включить, чтоб виджеты работали

        # Layout для организации — как полки в шкафу
        self.anchor_layout = UIAnchorLayout()  # Центрирует виджеты
        self.box_layout = UIBoxLayout(vertical=True, space_between=10)  # Вертикальный стек

        # Добавим все виджеты в box, потом box в anchor
        self.setup_widgets()  # Функция ниже

        self.anchor_layout.add(self.box_layout)  # Box в anchor
        self.manager.add(self.anchor_layout)  # Всё в manager



    def setup_widgets(self):
        label = UILabel(text="Vymluva",
                        font_size=50,
                        text_color=arcade.color.RED,
                        width=300,
                        align="center")
        self.box_layout.add(label)

        flat_button = UIFlatButton(text="Начать", width=200, height=50, color=arcade.color.RED)
        flat_button.on_click = lambda event: self.open_game()  # Не только лямбду, конечно
        self.box_layout.add(flat_button)

        flat_button1 = UIFlatButton(text="Настройки", width=200, height=50, color=(0, 0, 0))
        flat_button1.on_click = lambda event: self.open_settings()  # Не только лямбду, конечно
        self.box_layout.add(flat_button1)
        # Здесь добавим ВСЕ виджеты — по порядку! # Заполним ниже

    def on_draw(self):
        self.clear()
        self.manager.draw()  # Рисуй GUI поверх всего

    def on_mouse_press(self, x, y, button, modifiers):
        pass  # Для кликов, но manager сам обрабатывает

    def on_button_clicked(self):
        pass

    def open_game(self):
        print('fg')

    def open_settings(self):
        print('settings')


def main():
    # Создаём экземпляр нашего окна (800×600 пикселей, заголовок «Arcade Первый Контакт»)
    window = MainWindow()
    # Вызываем setup() для инициализации игровых объектов
    window.run()
    # Запускаем игровой цикл! Окно будет работать, пока его не закроют
    arcade.run()


if __name__ == "__main__":
    main()