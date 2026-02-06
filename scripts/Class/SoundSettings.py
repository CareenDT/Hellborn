import arcade
from pyglet.graphics import Batch

from scripts.globals import FILE_NAME
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *
import json

class SoundSettingsObject(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.Object_Batch = arcade.SpriteList()
        self.background_sprite_list = arcade.SpriteList()
        self.game_objects = []
        self.time_elapsed = 0
        self.file_name = FILE_NAME

        with open(self.file_name, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

        self.current_volume = self.settings["volume"]

        self.background = GameObject("Background", Transform(self.window.width // 2, self.window.height // 2))
        bg_renderer = SpriteRendererComponent("assets/bg_menu.png", 1.0, self.background_sprite_list)
        bg_renderer.set_custom_size(self.window.width, self.window.height)
        self.background.add_component(bg_renderer)

        self.settings_panel = GameObject("SettingsPanel", Transform())
        self.settings_panel.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.6, 0.8))
        self.game_objects.append(self.settings_panel)

        panel_width = 0.5 * self.window.width
        btn_width = 0.8 * panel_width
        btn_height = btn_width * (32 / 128)

        
        
        
        
        
        

        self.texture = arcade.load_texture("assets/images/down_btn.png").flip_horizontally()

        self.s_frame = GameObject("Sound_frame", Transform())
        self.s_frame.add_component(ScreenRelativeTransform(self.settings_panel, -0.8, 0.6, 1, 1))
        s_frame_renderer = SpriteRendererComponent("assets/images/sound_frame.png", 1, self.Object_Batch)
        s_frame_renderer.set_custom_size(btn_width * 0.06, btn_height * 0.2)
        self.s_frame.add_component(s_frame_renderer)
        self.game_objects.append(self.s_frame)

        self.down_btn = GameObject("down", Transform())
        self.down_btn.add_component(ScreenRelativeTransform(self.settings_panel, -0.2, -0.06, 1, 1))
        btn_down_render = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
        btn_down_render.set_custom_size(64, 64)
        btn_down_render.sprite.angle = 90
        self.down_btn.add_component(btn_down_render)
        self.down_btn.add_component(ButtonComponent(self, self.down_btn, "down",
                                                     on_click=lambda: self.onBtn_Click("down"),
                                                    normal_texture_path="assets/images/down_btn.png"))
        self.game_objects.append(self.down_btn)

        self.up_btn = GameObject("up", Transform())
        self.up_btn.add_component(ScreenRelativeTransform(self.settings_panel, 0.2, -0.06, 1, 1))
        up_btn_render = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
        up_btn_render.set_custom_size(64, 64)
        up_btn_render.sprite.angle = 270
        self.up_btn.add_component(up_btn_render)
        self.up_btn.add_component(ButtonComponent(self, self.up_btn, "up",
                                                     on_click=lambda: self.onBtn_Click("up"),
                                                     normal_texture_path="assets/images/down_btn.png"))
        self.game_objects.append(self.up_btn)

        self.btn_back = GameObject("Back", Transform())
        self.btn_back.add_component(ScreenRelativeTransform(self.settings_panel, 0, -0.25, 0.8, 0.8))
        btn_back_renderer = SpriteRendererComponent("assets/images/EXIT.png", 1, self.Object_Batch)
        btn_back_renderer.set_custom_size(btn_width // 2, btn_height // 2)
        self.btn_back.add_component(btn_back_renderer)
        self.btn_back.add_component(ButtonComponent(self, self.btn_back, "Back",
                                                    on_click=lambda: self.onBtn_Click("Back"),
                                                    normal_texture_path="assets/images/EXIT.png"))
        self.game_objects.append(self.btn_back)



    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw(pixelated=True)
        for obj in self.game_objects:
            obj.draw()
        self.Object_Batch.draw(pixelated=True)
        arcade.draw_text(f'{self.current_volume * 100}%', self.width // 2, self.height // 2 - 40, arcade.color.PURPLE,
                         anchor_x="center", anchor_y="center", font_size=60)

    def onBtn_Click(self, btn):
        if btn == "up":
            self.current_volume += 0.1
        elif btn == "down":
            self.current_volume -= 0.1
        elif btn == "Back":
            from scripts.Class.Settings import SettingsObject
            settings = SettingsObject(self.window)
            self.window.show_view(settings)
        if self.current_volume < 0:
            self.current_volume = 0
        if self.current_volume > 1:
            self.current_volume = 1
        self.current_volume *= 100
        self.current_volume //= 1
        self.current_volume /= 100
        if btn == "down" or btn == "up":
            self.settings["volume"] = self.current_volume

            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2)

    def on_update(self, delta_time):
        self.time_elapsed += delta_time
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
