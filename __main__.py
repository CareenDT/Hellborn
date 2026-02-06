import arcade

from scripts.Class.LogoScreen import LogoScreen
from scripts.globals import HEIGHT, WIDTH, FILE_NAME
from scripts.Class.FightLocal import FightLocal
from scripts.Menu import MenuObject
from scripts.Class.Tween import TweenManager
import os
import json

class Game(arcade.Window):
    def __init__(self, title: str):
        super().__init__(WIDTH, HEIGHT, title, resizable=False, antialiasing=False, fullscreen=True)
        arcade.set_background_color(arcade.color.BLACK)
        self.file_name = FILE_NAME
        self.MenuMusic = arcade.load_sound("assets/audio/msc_music.mp3")

    def setup(self):
        loading_screen = LogoScreen(self)
        self.show_view(loading_screen)

        self.MenuMusicPlayer = self.MenuMusic.play(loop=True)

        if not os.path.exists(self.file_name):
            settings = {
                "volume": 1,
                "controls":
                    {'player_1':
                        {
                            "jump": "w",
                            "backward": "a",
                            "forward": "d",
                            "hand strike": "e",
                            "uppercut": "q"
                        },
                    'player_2':
                        {
                            "jump": "i",
                            "backward": "j",
                            "forward": "l",
                            "hand strike": "o",
                            "uppercut": "u"
                        },
                    }
            }
            with open(self.file_name, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)

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
