import arcade
from arcade import SpriteList
from pyglet.graphics import Batch

from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *
from scripts.globals import WIDTH, HEIGHT

class FightLocal(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)

        self.Batch = Batch()

        self.window = window

        self.Object_Batch = arcade.SpriteList()

        self.game_objects: list[GameObject] = []

        self.obj_Side = GameObject("Menu_Sidebar", Transform())
        self.obj_Side.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.35, 1))

        self.obj_Side.add_component(BoxRenderer((255, 0, 0, 60), self.obj_Side))
        self.game_objects.append(self.obj_Side)

        self.background_sprite_list = SpriteList()

        self.background_sprite = arcade.Sprite("assets/arena.png",
                                               center_x=WIDTH // 2,
                                               center_y=HEIGHT // 2)

        self.background_sprite.width = WIDTH
        self.background_sprite.height = HEIGHT
        self.background_sprite_list.append(self.background_sprite)

        self.hp_bar = arcade.Sprite("assets/images/hp_bar.png",
                                    center_y=HEIGHT // 1.22,
                                    center_x=WIDTH // 2 - 200)

        self.hp_bar.width = (192 * (WIDTH / 192 / 1.4)) // 1
        self.hp_bar.height = 64 * 5
        self.background_sprite_list.append(self.hp_bar)

        self.rage_bar1 = arcade.Sprite("assets/images/rage_bar.png",
                                    center_y=HEIGHT - HEIGHT // 1.07,
                                    center_x=WIDTH // 6.5)

        self.rage_bar1.width = (236 * (WIDTH / 236 / 3.7)) // 1
        self.rage_bar1.height = 32 * 2.5
        self.background_sprite_list.append(self.rage_bar1)

        texture_r_b =arcade.load_texture("assets/images/rage_bar.png")

        self.rage_bar2 = arcade.Sprite(texture_r_b,
                                    center_y=HEIGHT - HEIGHT // 1.07,
                                    center_x=WIDTH // 1.565)

        self.rage_bar2.width = -(236 * (WIDTH / 236 / 3.7)) // 1
        self.rage_bar2.height = 32 * 2.5
        self.background_sprite_list.append(self.rage_bar2)

        self.hp1 = arcade.Sprite("assets/images/1hp.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 15)

        self.hp1.width = 32
        self.hp1.height = 32
        self.background_sprite_list.append(self.hp1)

        self.av1 = arcade.Sprite("assets/images/avotarochka.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 15)

        self.av1.width = 36
        self.av1.height = 36
        self.background_sprite_list.append(self.av1)

        self.hp2 = arcade.Sprite("assets/images/1hp.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 11)

        self.hp2.width = 32
        self.hp2.height = 32
        self.background_sprite_list.append(self.hp2)

        self.av2 = arcade.Sprite("assets/images/avotarochka.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 11)

        self.av2.width = 36
        self.av2.height = 36
        self.background_sprite_list.append(self.av2)

        self.hp3 = arcade.Sprite("assets/images/1hp.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 1.378)

        self.hp3.width = 32
        self.hp3.height = 32
        self.background_sprite_list.append(self.hp3)

        self.av3 = arcade.Sprite("assets/images/avotarochka.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 1.378)

        self.av3.width = -36
        self.av3.height = 36
        self.background_sprite_list.append(self.av3)

        self.hp4 = arcade.Sprite("assets/images/1hp.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 1.425)

        self.hp4.width = 32
        self.hp4.height = 32
        self.background_sprite_list.append(self.hp4)

        self.av4 = arcade.Sprite("assets/images/avotarochka.png",
                                    center_y=HEIGHT // 1.27,
                                    center_x=WIDTH // 1.425)

        self.av4.width = -36
        self.av4.height = 36
        self.background_sprite_list.append(self.av4)




    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw(pixelated=True)

        for obj in self.game_objects:
            obj.draw()

        self.Object_Batch.draw(pixelated=True)

        self.Batch.draw()

    def on_update(self, delta_time):

        self.background_sprite.width = WIDTH
        self.background_sprite.height = HEIGHT
        self.background_sprite.center_x = WIDTH // 2
        self.background_sprite.center_y = HEIGHT // 2

        for obj in self.game_objects:
            obj.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        for obj in self.game_objects:
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_click(x, y, button)

    def on_mouse_motion(self, x, y, dx, dy):
        for obj in self.game_objects:
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_mouse_hover(x, y)

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.SPACE:
            arcade.close_window()