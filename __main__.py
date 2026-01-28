import arcade
from scripts.globals import HEIGHT, WIDTH
from scripts.Class.Character.Syorma import Syorma
from scripts.Class.Player.PlayerController import PlayerController
from scripts.Menu import MenuObject
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *
from scripts.Class.LoadingScreen import LoadingScreen
from scripts.Class.Tween import *


class Game(arcade.Window):
    def __init__(self, title: str):
        super().__init__(WIDTH, HEIGHT, title, resizable=True, antialiasing=False, fullscreen=True)
        self.background_color = arcade.color.WHITE

    def setup(self):
        loading_screen = LoadingScreen(self)
        loading_screen.setup()
        self.show_view(loading_screen)

        self._time = 0

        self.syorma = Syorma("Syorma", Transform(WIDTH // 4, HEIGHT // 2))
        
        from scripts.Class.Character.CharacterComponent import CharacterComponent
        character_comp = self.syorma.get_component(CharacterComponent)
        
        if character_comp:
            self.player1_controller = PlayerController(character_comp, {
                'left': arcade.key.A,
                'right': arcade.key.D,
                'jump': arcade.key.W,
                'attack': arcade.key.J,
                'uppercut': arcade.key.K,
                'awaken': arcade.key.L
            })
        
        self.syorma2 = Syorma("Syorma2", Transform(WIDTH * 3 // 4, HEIGHT // 2))
        character_comp2 = self.syorma2.get_component(CharacterComponent)
        
        if character_comp2:
            character_comp2.facing_right = False
            self.player2_controller = PlayerController(character_comp2, {
                'left': arcade.key.LEFT,
                'right': arcade.key.RIGHT,
                'jump': arcade.key.UP,
                'attack': arcade.key.NUM_1,
                'uppercut': arcade.key.NUM_2,
                'awaken': arcade.key.NUM_3
            })

        self.game_objects: list[GameObject] = [self.syorma, self.syorma2]

        from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
        self.player_sprites = arcade.SpriteList()
        
        for obj in self.game_objects:
            sprite_renderer = obj.get_component(SpriteRendererComponent)
            if sprite_renderer and sprite_renderer.batch:
                for sprite in sprite_renderer.batch:
                    self.player_sprites.append(sprite)

        self.keys_pressed = set()

    def on_update(self, delta_time):
        TweenManager.update()

        for obj in self.game_objects:
            obj.update(delta_time)

        if hasattr(self, 'player1_controller'):
            self.player1_controller.update(delta_time)
        if hasattr(self, 'player2_controller'):
            self.player2_controller.update(delta_time)

    def on_draw(self):
        self.clear()

        if hasattr(self, 'player_sprites'):
            self.player_sprites.draw(pixelated=True)

    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)
        
        if hasattr(self, 'player1_controller'):
            self.player1_controller.on_key_press(key)
        if hasattr(self, 'player2_controller'):
            self.player2_controller.on_key_press(key)

        if key == arcade.key.F11:
            self.set_fullscreen(not self.fullscreen)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        
        if hasattr(self, 'player1_controller'):
            self.player1_controller.on_key_release(key)
        if hasattr(self, 'player2_controller'):
            self.player2_controller.on_key_release(key)

def main():
    game = Game("HellBorn")
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
