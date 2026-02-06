import arcade
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *
from scripts.Class.SoundSettings import SoundSettingsObject
from scripts.Class.ControlsSettings import ControlsSettingsObject


class SettingsObject(arcade.View):
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

        self.settings_panel = GameObject("SettingsPanel", Transform())
        self.settings_panel.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.6, 0.8))
        self.game_objects.append(self.settings_panel)

        panel_width = 0.5 * self.window.width
        btn_width = 0.8 * panel_width
        btn_height = btn_width * (32 / 128)

        self.title = GameObject("Title", Transform())
        self.title.add_component(ScreenRelativeTransform(self.settings_panel, 0, 0.4, 1, 1))
        title_renderer = SpriteRendererComponent("assets/images/hellborn.png", 1, self.Object_Batch)
        title_renderer.set_custom_size(btn_width * 1.2, btn_height * 0.9)
        self.title.add_component(title_renderer)
        self.game_objects.append(self.title)

        self.s_frame = GameObject("Settings_frame", Transform())
        self.s_frame.add_component(ScreenRelativeTransform(self.settings_panel, -0.8, 0.6, 1, 1))
        s_frame_renderer = SpriteRendererComponent("assets/images/settings_frame.png", 1, self.Object_Batch)
        s_frame_renderer.set_custom_size(btn_width * 0.06, btn_height * 0.2)
        self.s_frame.add_component(s_frame_renderer)
        self.game_objects.append(self.s_frame)

        self.btn_music = GameObject("Music", Transform())
        self.btn_music.add_component(ScreenRelativeTransform(self.settings_panel, 0, 0.15, 0.8, 0.8))
        btn_music_renderer = SpriteRendererComponent("assets/images/sound.png", 1, self.Object_Batch)
        btn_music_renderer.set_custom_size(btn_width * 1.2, btn_height)
        self.btn_music.add_component(btn_music_renderer)
        self.btn_music.add_component(ButtonComponent(self, self.btn_music, "Music",
                                                     on_click=lambda: self.onBtn_Click("Music"),
                                                     normal_texture_path="assets/images/sound.png"))
        self.game_objects.append(self.btn_music)

        self.btn_customization = GameObject("Customization", Transform())
        self.btn_customization.add_component(ScreenRelativeTransform(self.settings_panel, 0, -0.15, 0.8, 0.8))
        btn_customization_renderer = SpriteRendererComponent("assets/images/key_btn.png", 1, self.Object_Batch)
        btn_customization_renderer.set_custom_size(btn_width * 1.2, btn_height)
        self.btn_customization.add_component(btn_customization_renderer)
        self.btn_customization.add_component(ButtonComponent(self, self.btn_customization, "Customization",
                                                             on_click=lambda: self.onBtn_Click("Customization"),
                                                             normal_texture_path="assets/images/key_btn.png"))
        self.game_objects.append(self.btn_customization)

        self.btn_back = GameObject("Back", Transform())
        self.btn_back.add_component(ScreenRelativeTransform(self.settings_panel, 0, -0.45, 0.8, 0.8))
        btn_back_renderer = SpriteRendererComponent("assets/images/return.png", 1, self.Object_Batch)
        btn_back_renderer.set_custom_size(btn_width * 1.2, btn_height)
        self.btn_back.add_component(btn_back_renderer)
        self.btn_back.add_component(ButtonComponent(self, self.btn_back, "Back",
                                                    on_click=lambda: self.onBtn_Click("Back"),
                                                    normal_texture_path="assets/images/return.png"))
        self.game_objects.append(self.btn_back)

    def on_draw(self):
        self.clear()
        self.background_sprite_list.draw(pixelated=True)
        for obj in self.game_objects:
            obj.draw()
        self.Object_Batch.draw(pixelated=True)

    def onBtn_Click(self, btn):
        if btn == "Back":
            from scripts.Menu import MenuObject
            menu = MenuObject(self.window)
            self.window.show_view(menu)
        elif btn == "Music":
            sound = SoundSettingsObject(self.window)
            self.window.show_view(sound)
        elif btn == "Customization":
            custom_keys = ControlsSettingsObject(self.window)
            self.window.show_view(custom_keys)

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
