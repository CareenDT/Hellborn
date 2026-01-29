import arcade
import math
from scripts.Transition import Transition
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class MenuObject(arcade.View):
    def __init__(self, window):
        super().__init__()
        self.window = window
        self.Object_Batch = arcade.SpriteList()
        self.game_objects = []
        self.time_elapsed = 0

        # Background
        self.background = GameObject("Background", Transform(self.window.width // 2, self.window.height // 2))
        self.background.add_component(SpriteRendererComponent("assets/bg_menu.png", 1.0, self.Object_Batch))
        self.game_objects.append(self.background)

        # Play Button
        self.btn_play = GameObject("Play", Transform())
        self.btn_play.add_component(ScreenRelativeTransform(self, 0.5, 0.4, 0.5, 0.25))
        self.btn_play.add_component(SpriteRendererComponent("assets/images/play.png", 1, self.Object_Batch))
        self.btn_play.add_component(ButtonComponent(self, self.btn_play, "Play", on_click=self.onBtn_Play, normal_texture_path="assets/images/play.png"))
        self.game_objects.append(self.btn_play)

        # Exit Button
        self.btn_exit = GameObject("Exit", Transform())
        self.btn_exit.add_component(ScreenRelativeTransform(self, 0.5, 0.25, 0.5, 0.25))
        self.btn_exit.add_component(SpriteRendererComponent("assets/images/EXIT.png", 1, self.Object_Batch))
        self.btn_exit.add_component(ButtonComponent(self, self.btn_exit, "Exit", on_click=lambda: self.onBtn_Click("Exit"), normal_texture_path="assets/images/EXIT.png"))
        self.game_objects.append(self.btn_exit)

        # Settings Button
        self.btn_settings = GameObject("Settings", Transform())
        self.btn_settings.add_component(ScreenRelativeTransform(self, 0.5, 0.55, 0.5, 0.25))
        self.btn_settings.add_component(SpriteRendererComponent("assets/images/settings.png", 1, self.Object_Batch))
        self.btn_settings.add_component(ButtonComponent(self, self.btn_settings, "Settings", on_click=lambda: self.onBtn_Click("Settings"), normal_texture_path="assets/images/settings.png"))
        self.game_objects.append(self.btn_settings)

        # Logo
        self.logo = GameObject("Logo", Transform(self.window.width // 2, self.window.height * 0.75))
        self.logo.add_component(SpriteRendererComponent("assets/images/hellborn.png", 1.5, self.Object_Batch))
        self.game_objects.append(self.logo)

    def onBtn_Play(self):
        self.onBtn_Click("Play")

    def on_draw(self):
        self.clear()
        for obj in self.game_objects:
            obj.draw()
        self.Object_Batch.draw(pixelated=True)

    def onBtn_Click(self, btn):
        if btn == "Play":
            transition = Transition(self.window)
            self.window.show_view(transition)
        elif btn == "Exit":
            arcade.close_window()
        elif btn == "Settings":
            pass

    def on_update(self, delta_time):
        self.time_elapsed += delta_time
        rotation_angle = math.sin(self.time_elapsed * 0.5) * 10
        if self.logo.get_component(SpriteRendererComponent):
            self.logo.get_component(SpriteRendererComponent).sprite.angle = rotation_angle

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
