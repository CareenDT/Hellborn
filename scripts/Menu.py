import arcade
import math
from scripts.Transition import Transition
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class MenuObject(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.Object_Batch = arcade.SpriteList()
        self.background_sprite_list = arcade.SpriteList()
        self.game_objects = []
        self.time_elapsed = 0

        self.background = GameObject("Background", Transform(self.window.width // 2, self.window.height // 2))
        bg_renderer = SpriteRendererComponent("assets/bg_menu.png", 1.0, self.background_sprite_list)
        bg_renderer.set_custom_size(self.window.width, self.window.height)
        self.background.add_component(bg_renderer)

        self.sidebar = GameObject("Sidebar", Transform())
        self.sidebar.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.45, 1))
        self.game_objects.append(self.sidebar)

        sidebar_width = 0.35 * self.window.width
        btn_width = 0.8 * sidebar_width
        btn_height = btn_width * (32 / 128)

        self.btn_play = GameObject("Play", Transform())
        self.btn_play.add_component(ScreenRelativeTransform(self.sidebar, 0, 0.15, 0.8, 0.8))
        btn_play_renderer = SpriteRendererComponent("assets/images/play.png", 1, self.Object_Batch)
        btn_play_renderer.set_custom_size(btn_width, btn_height)
        self.btn_play.add_component(btn_play_renderer)
        self.btn_play.add_component(ButtonComponent(self, self.btn_play, "Play", on_click=self.onBtn_Play, normal_texture_path="assets/images/play.png"))
        self.game_objects.append(self.btn_play)

        self.btn_settings = GameObject("Settings", Transform())
        self.btn_settings.add_component(ScreenRelativeTransform(self.sidebar, 0, -0.1, 0.8, 0.8))
        btn_settings_renderer = SpriteRendererComponent("assets/images/settings.png", 1, self.Object_Batch)
        btn_settings_renderer.set_custom_size(btn_width, btn_height)
        self.btn_settings.add_component(btn_settings_renderer)
        self.btn_settings.add_component(ButtonComponent(self, self.btn_settings, "Settings", on_click=lambda: self.onBtn_Click("Settings"), normal_texture_path="assets/images/settings.png"))
        self.game_objects.append(self.btn_settings)

        self.btn_exit = GameObject("Exit", Transform())
        self.btn_exit.add_component(ScreenRelativeTransform(self.sidebar, 0, -0.35, 0.8, 0.8))
        btn_exit_renderer = SpriteRendererComponent("assets/images/EXIT.png", 1, self.Object_Batch)
        btn_exit_renderer.set_custom_size(btn_width, btn_height)
        self.btn_exit.add_component(btn_exit_renderer)
        self.btn_exit.add_component(ButtonComponent(self, self.btn_exit, "Exit", on_click=lambda: self.onBtn_Click("Exit"), normal_texture_path="assets/images/EXIT.png"))
        self.game_objects.append(self.btn_exit)

        self.logo = GameObject("Logo", Transform())
        self.logo.add_component(ScreenRelativeTransform(self, 0.5, 0.85, 1, 1))
        logo_renderer = SpriteRendererComponent("assets/images/hellborn.png", 1.5, self.Object_Batch)
        if logo_renderer.texture:
            original_width = logo_renderer.texture.width
            original_height = logo_renderer.texture.height
            target_width = self.window.width * 0.5
            target_height = target_width * (original_height / original_width)
            logo_renderer.set_custom_size(target_width, target_height)
        self.logo.add_component(logo_renderer)
        self.logo.add_component(AspectRatioComponent(1, True, self.logo))
        self.game_objects.append(self.logo)

    def onBtn_Play(self):
        self.onBtn_Click("Play")

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw(pixelated=True)
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
        rotation_angle = math.sin(self.time_elapsed * 0.5) * 5
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
