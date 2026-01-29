import arcade
from scripts.Menu import MenuObject
from scripts.globals import HEIGHT, WIDTH
from scripts.Class.FightLocal import FightLocal

class LogoScreen(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.timer = 0
        self.alpha = 0
        self.fade_state = "in"
        
        self.sprite_list = arcade.SpriteList()
        self.sprite = arcade.Sprite("assets/images/hellborn.png")
        self.sprite.center_x = self.window.width // 2
        self.sprite.center_y = self.window.height // 2
        self.sprite.alpha = 0

        target_width = self.window.width * 0.8
        scale = target_width / self.sprite.width
        self.sprite.scale = scale

        self.sprite_list.append(self.sprite)

    def on_draw(self):
        self.clear()
        self.sprite_list.draw(pixelated=True)
    def on_update(self, delta_time):
        self.timer += delta_time
        
        if self.fade_state == "in":
            self.alpha = min(self.alpha + 200 * delta_time, 255)
            self.sprite.alpha = int(self.alpha)
            if self.alpha >= 255:
                self.fade_state = "hold"
                self.timer = 0
        
        elif self.fade_state == "hold":
            if self.timer >= 2.0:
                self.fade_state = "out"
                self.timer = 0
        
        elif self.fade_state == "out":
            self.alpha = max(self.alpha - 200 * delta_time, 0)
            self.sprite.alpha = int(self.alpha)
            if self.alpha <= 0:
                
                Menu_view = MenuObject(self.window)
                self.window.show_view(Menu_view)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            fight_view = FightLocal(self.window)
            self.window.show_view(fight_view)