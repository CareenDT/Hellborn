import arcade
from scripts.globals import HEIGHT, WIDTH
from scripts.Menu import MenuObject
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class Game(arcade.Window):
    def __init__(self, title: str):
        super().__init__(WIDTH, HEIGHT, title, resizable=True, antialiasing=False)
        self.background_color = arcade.color.WHITE
        self.bg_texture = arcade.load_texture(
            "assets/images/PlaceHolder.png"
        )

    def setup(self):
        self._time = 0

        self.game_objects: list[GameObject] = []

        self.Object_Batch = arcade.SpriteList()

        self.keys_pressed = set()

        self.Menu_View = MenuObject(self)

        self.show_view(self.Menu_View)

    def on_draw(self):
        self.clear()
        arcade.draw_texture_rect(
            self.bg_texture,
            arcade.rect.XYWH( 
                self.width // 2,
                self.height // 2,
                self.width,
                self.height,
            ),
        )
        self.Object_Batch.draw(pixelated=True)

        for obj in self.game_objects:
            obj.draw()
     
    def on_update(self, delta_time):

        for obj in self.game_objects:
            obj.update(delta_time)
    
    def on_key_press(self, key, modifiers):
        self.keys_pressed.add(key)

    def on_key_release(self, key, modifiers):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)


def main():
    game = Game("HellBorn")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()