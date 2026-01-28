import arcade
from pyglet.graphics import Batch

from scripts.globals import HEIGHT, WIDTH
from scripts.Menu import MenuObject
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class FightLocal(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)

        self.loading_progress = 0

        self.loading_complete = False

        self.background = None

        self.alpha_low = False

        self.alpha = 0

        self.load_prog = 0

        self.game_objects = []

        self.background_color = (0,0,0)

    def setup(self):

        self.create_loading_animation()

        self.batch = Batch()

        self.Object_Batch = arcade.SpriteList()

        try:
            self.background = arcade.load_texture("assets/b_gg.jpg")
        except Exception as e:
            self.background = None

        self.creators_txt = arcade.Text(
            "Game by Careen, Fizis, Waqman",
            WIDTH // 2 - WIDTH // 10,
            HEIGHT // 4,
            arcade.color.PURPLE,
            32,
            align="center",
            anchor_x="center",
            batch=self.batch,
            alpha=self.alpha,
        )

        self.Logo = GameObject("Logo", Transform())
        self.Logo.add_component(ScreenRelativeTransform(self, 0.5, 0.65, 0.5, 1))
        self.Logo.add_component(AspectRatioComponent(0.15702479,True))
        self.Logo.add_component(SpriteRendererComponent("assets/images/hellborn.png", 1, self.Object_Batch))
        self.game_objects.append(self.Logo)

    def create_loading_animation(self):
        self.animation_timer = 0

    def on_draw(self):

        self.clear()

        if self.alpha >= 50:
            self.alpha_2 = self.alpha - 50
        else:
            self.alpha_2 = 0

        arcade.draw_text(
            "Game by Careen, Fizis, Waqman",
            WIDTH // 2 - WIDTH // 10,
            HEIGHT // 4,
            (arcade.color.PURPLE[0], arcade.color.PURPLE[1], arcade.color.PURPLE[2], int(self.alpha_2)),
            32,
            align="center",
            anchor_x="center"
        )

        for i in self.game_objects:
            i.draw()

        self.Object_Batch.draw(pixelated=True)

        self.batch.draw()

    def on_update(self, delta_time):
        if self.loading_complete and self.animation_timer >= 0.5:
            self.Menu_obj = MenuObject(self)
            self.window.show_view(self.Menu_obj)
        if self.alpha >= 254:
            self.alpha_low = True
        if self.alpha_low:
            if self.load_prog >= 0.8:
                if self.alpha <= 10:
                    self.loading_complete = True
                self.alpha -= 80 * delta_time
        else:
            self.alpha += 80 * delta_time
        if self.loading_complete:
            self.animation_timer += delta_time
        if self.alpha_low:
            self.load_prog += delta_time

        self.Logo.get_component(SpriteRendererComponent).sprite.alpha = self.alpha

        for i in self.game_objects:
            i.update(delta_time)

    def on_btn_Play(self):
        pass

    def on_key_press(self, key: int, modifiers: int):
        if key == arcade.key.ENTER or key == arcade.key.SPACE:
            menu_view = MenuObject(self.window)
            self.window.show_view(menu_view)