import arcade
from scripts.globals import WIDTH, HEIGHT
from scripts.Class.FightLocal import FightLocal

class Transition(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.timer = 0
        self.duration = 2.0
        arcade.set_background_color(arcade.color.BLACK)

    def on_show(self):
        self.timer = 0

    def on_update(self, delta_time):
        self.timer += delta_time
        if self.timer >= self.duration + 0.2:
            self.go_to_fight()

    def go_to_fight(self):
        fight_screen = FightLocal(self.window)
        self.window.show_view(fight_screen)

    def on_draw(self):
        self.clear()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.SPACE:
            self.go_to_fight()