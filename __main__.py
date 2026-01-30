import arcade
from scripts.globals import HEIGHT, WIDTH
from scripts.Class.LogoScreen import LogoScreen
from scripts.Class.FightLocal import FightLocal
from scripts.Menu import MenuObject
from scripts.Class.Tween import TweenManager

class Game(arcade.Window):
    def __init__(self, title: str):
        super().__init__(WIDTH, HEIGHT, title, resizable=False, antialiasing=False, fullscreen=False)
        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        loading_screen = FightLocal(self)
        self.show_view(loading_screen)

    def on_update(self, delta_time):
        TweenManager.update()

    def on_key_press(self, key, modifiers):
        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)
        elif key == arcade.key.F2:
            fight_view = FightLocal(self)
            self.show_view(fight_view)
        elif key == arcade.key.F3:
            menu_view = MenuObject(self)
            self.show_view(menu_view)

def main():
    game = Game("HellBorn")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()