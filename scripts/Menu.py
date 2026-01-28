import arcade
from arcade import SpriteList
from pyglet.graphics import Batch
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *
from Globals import WIDTH, HEIGHT


class MenuObject(arcade.View):
    def __init__(self, window):
        super().__init__()

        self.Batch = Batch()

        self.window = window

        self.Object_Batch = arcade.SpriteList()

        self.game_objects: list[GameObject] = []

        self.obj_Side = GameObject("Menu_Sidebar", Transform())
        self.obj_Side.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.35, 1))

        self.obj_Side.add_component(BoxRenderer((0, 0, 0, 0), self.obj_Side))
        self.game_objects.append(self.obj_Side)

        self.background_sprite_list = SpriteList()

        self.background_sprite = arcade.Sprite("assets/bg_menu.png",
                                               center_x=WIDTH // 2,
                                               center_y=HEIGHT // 2)
        self.background_sprite.width = WIDTH
        self.background_sprite.height = HEIGHT
        self.background_sprite_list.append(self.background_sprite)

        self.Btn = GameObject("Start", Transform())

        self.Btn.add_component(ScreenRelativeTransform(self.obj_Side, 0, 0, 0.5, 0.1))

<<<<<<< HEAD
        self.Btn.add_component(ButtonComponent(self, self.Btn, "Play", on_click = self.onBtn_Play,
=======
        self.Btn.add_component(ButtonComponent(self, self.Btn, "Play", on_click=lambda: self.onBtn_Click('Play'),
>>>>>>> 20e52fe7a1498179ae907001e76d342ff1fdabdd
                                               normal_texture=arcade.load_texture("assets/images/play.png")))

        self.Btn.add_component(SpriteRendererComponent("assets/images/play.png", 1, self.Object_Batch))
        self.game_objects.append(self.Btn)

        self.Btn_close = GameObject("Exit", Transform())

        self.Btn_close.add_component(ScreenRelativeTransform(self.obj_Side, 0, -0.2, 0.5, 0.1))

        self.Btn_close.add_component(
            ButtonComponent(self, self.Btn_close, "Play", on_click=lambda: self.onBtn_Click("Exit"),
                            normal_texture=arcade.load_texture("assets/images/EXIT.png")))

        self.Btn_close.add_component(SpriteRendererComponent("assets/images/EXIT.png", 1, self.Object_Batch))
        self.game_objects.append(self.Btn_close)

        self.Btn_settings = GameObject("Settings", Transform())

        self.Btn_settings.add_component(ScreenRelativeTransform(self.obj_Side, 0, 0.2, 0.5, 0.1))

        self.Btn_settings.add_component(
            ButtonComponent(self, self.Btn_settings, "Play", on_click=lambda: self.onBtn_Click('Settings'),
                            normal_texture=arcade.load_texture("assets/images/settings.png")))

        self.Btn_settings.add_component(SpriteRendererComponent("assets/images/settings.png", 1, self.Object_Batch))
        self.game_objects.append(self.Btn_settings)

        self.hellborn_sprite = arcade.Sprite('assets/images/hellborn.png',
                                             center_x=-120,
                                             center_y=HEIGHT // 1.2,
                                             scale=1.5)

        self.hellborn_sprite_list = SpriteList()
        self.hellborn_sprite_list.append(self.hellborn_sprite)

        self.animation = True

    def on_draw(self):
        self.clear()

        self.background_sprite_list.draw(pixelated=True)

        self.hellborn_sprite_list.draw(pixelated=True)

        for obj in self.game_objects:
            obj.draw()

        self.Object_Batch.draw(pixelated=True)

        self.Batch.draw()

    def onBtn_Click(self, btn):
        print(btn)
        if btn == "Play":
            from scripts.Perexodnik import Perexodnik

            transition = Perexodnik(self.window)
            self.window.show_view(transition)
        elif btn == "Exit":
            arcade.close_window()
        elif btn == "Settings":
            pass

    def on_update(self, delta_time):

        self.background_sprite.width = WIDTH
        self.background_sprite.height = HEIGHT
        self.background_sprite.center_x = WIDTH // 2
        self.background_sprite.center_y = HEIGHT // 2

        if self.animation:
            self.hellborn_sprite.center_x += 50 * delta_time
            if self.hellborn_sprite.center_x >= 100:
                self.animation = False


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
