import arcade

class Character(arcade.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, SCALE, SPEED, x, y):
        super().__init__()
        self.textures = [arcade.load_texture('recources/CharacterSprite.png')]
        self.set_texture(0)
        self.center_x = x
        self.width1 = SCREEN_WIDTH
        self.height1 = SCREEN_HEIGHT
        self.center_y = y
        self.scale = SCALE
        self.speed = SPEED
        self.is_walking = False
        self.pressed = []
        print(self.speed)

    def update(self, delta_time, keys_pressed):
        if len(keys_pressed) == 0:
            self.is_walking = False
        if len(keys_pressed) == 1 and keys_pressed[0] == arcade.key.LEFT:
            self.face_dir = False
            self.is_walking = True
            self.left = max(0, self.left - delta_time * self.speed)
        if len(keys_pressed) == 1 and keys_pressed[0] == arcade.key.RIGHT:
            self.face_dir = True
            self.is_walking = True
            self.right = min(self.width1, self.right + delta_time * self.speed)
        if len(keys_pressed) == 1 and keys_pressed[0] == arcade.key.UP:
            #self.face_dir = True
            self.is_walking = True
            self.top = min(self.height1, self.top + delta_time * self.speed)
        if len(keys_pressed) == 1 and keys_pressed[0] == arcade.key.DOWN:
            #self.face_dir = True
            self.is_walking = True
            self.bottom = max(0, self.bottom - delta_time * self.speed)
        if len(keys_pressed) == 2:
            if arcade.key.UP in keys_pressed and arcade.key.LEFT in keys_pressed:
                self.top = min(self.height1, self.top + delta_time * self.speed * 0.7071)
                self.left = max(0, self.left - delta_time * self.speed * 0.7071)
                self.face_dir = False
                self.is_walking = True
            if arcade.key.UP in keys_pressed and arcade.key.RIGHT in keys_pressed:
                self.face_dir = True
                self.is_walking = True
                self.top = min(self.height1, self.top + delta_time * self.speed * 0.7071)
                self.right = min(self.width1, self.right + delta_time * self.speed * 0.7071)
            if arcade.key.DOWN in keys_pressed and arcade.key.LEFT in keys_pressed:
                self.left = max(0, self.left - delta_time * self.speed * 0.7071)
                self.bottom = max(0, self.bottom - delta_time * self.speed * 0.7071)
                self.face_dir = False
                self.is_walking = True
            if arcade.key.DOWN in keys_pressed and arcade.key.RIGHT in keys_pressed:
                self.face_dir = True
                self.is_walking = True
                self.bottom = max(0, self.bottom - delta_time * self.speed * 0.7071)
                self.right = min(self.width1, self.right + delta_time * self.speed * 0.7071)