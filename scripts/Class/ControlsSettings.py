import arcade
import json
from scripts.globals import FILE_NAME
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *


class ControlsSettingsObject(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.Object_Batch = arcade.SpriteList()
        self.background_sprite_list = arcade.SpriteList()
        self.game_objects = []
        self.time_elapsed = 0
        self.file_name = FILE_NAME
        self.waiting_for_key = None
        self.player = "player_1"

        with open(self.file_name, "r", encoding="utf-8") as f:
            self.settings = json.load(f)

        self.background = GameObject("Background", Transform(self.window.width // 2, self.window.height // 2))
        bg_renderer = SpriteRendererComponent("assets/bg_menu.png", 1.0, self.background_sprite_list)
        bg_renderer.set_custom_size(self.window.width, self.window.height)
        self.background.add_component(bg_renderer)

        self.settings_panel = GameObject("SettingsPanel", Transform())
        self.settings_panel.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.8, 0.9))
        self.game_objects.append(self.settings_panel)

        panel_width = 0.5 * self.window.width
        btn_width = 0.8 * panel_width
        btn_height = btn_width * (32 / 128)

        self.title = GameObject("Title", Transform())
        self.title.add_component(ScreenRelativeTransform(self.settings_panel, 0, 0.45, 1, 1))
        title_renderer = SpriteRendererComponent("assets/images/hellborn.png", 1, self.Object_Batch)
        title_renderer.set_custom_size(btn_width * 1.2, btn_height * 0.9)
        self.title.add_component(title_renderer)
        self.game_objects.append(self.title)

        self.btn_player1 = GameObject("Player1", Transform())
        self.btn_player1.add_component(ScreenRelativeTransform(self.settings_panel, -0.185, 0.23, 0.15, 0.8))
        btn_player1_renderer = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
        btn_player1_renderer.set_custom_size(btn_width * 0.2, btn_height * 0.3)
        self.btn_player1.add_component(btn_player1_renderer)
        self.btn_player1.add_component(ButtonComponent(self, self.btn_player1, "player1",
                                                       on_click=lambda: self.onBtn_Click("player1"),
                                                       normal_texture_path="assets/images/down_btn.png"))
        self.game_objects.append(self.btn_player1)

        self.btn_player2 = GameObject("Player2", Transform())
        self.btn_player2.add_component(ScreenRelativeTransform(self.settings_panel, 0.19, 0.23, 0.15, 0.8))
        btn_player2_renderer = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
        btn_player2_renderer.set_custom_size(btn_width * 0.2, btn_height * 0.3)
        btn_player2_renderer.sprite.angle = 180
        self.btn_player2.add_component(btn_player2_renderer)
        self.btn_player2.add_component(ButtonComponent(self, self.btn_player2, "player2",
                                                       on_click=lambda: self.onBtn_Click("player2"),
                                                       normal_texture_path="assets/images/down_btn.png"))
        self.game_objects.append(self.btn_player2)

        y_positions = [0.08, 0.005, -0.073, -0.15, -0.225, -0.305]
        actions = ["jump", "sit", "backward", "forward", "hand strike", "kick"]

        self.action_buttons = {}

        for i, action in enumerate(actions):
            btn = GameObject(f"btn_{action}", Transform())
            btn.add_component(ScreenRelativeTransform(self.settings_panel, -0.32, y_positions[i], 0.15, 0.8))
            btn_renderer = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
            btn_renderer.set_custom_size(btn_width * 0.04, btn_height * 0.2)
            btn_renderer.sprite.angle = 90
            btn.add_component(btn_renderer)
            btn.add_component(ButtonComponent(self, btn, action,
                                              on_click=lambda act=action[:]: self.on_action_click(act),
                                              normal_texture_path="assets/images/down_btn.png"))
            self.game_objects.append(btn)
            self.action_buttons[action] = btn

        self.btn_back = GameObject("Back", Transform())
        self.btn_back.add_component(ScreenRelativeTransform(self.settings_panel, 0, -0.45, 0.15, 0.8))
        btn_back_renderer = SpriteRendererComponent("assets/images/return.png", 1, self.Object_Batch)
        btn_back_renderer.set_custom_size(btn_width * 0.6, btn_height)
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

        arcade.draw_text("Игрок 1", self.width * 0.35, self.height * 0.65, arcade.color.BEAVER, 24, anchor_x="center",
                         anchor_y="center", font_name="Tahoma")
        arcade.draw_text("Игрок 2", self.width * 0.65, self.height * 0.65, arcade.color.BEAVER, 24, anchor_x="center",
                         anchor_y="center", font_name="Tahoma")

        y_positions = [0.58, 0.51, 0.44, 0.37, 0.3, 0.23]
        action_names = ["Прыжок", "Присед", "Назад", "Вперед", "Удар рукой", "Удар ногой"]
        action_keys = ["jump", "sit", "backward", "forward", "hand strike", "kick"]

        for i in range(len(action_names)):
            arcade.draw_text(action_names[i], self.width * 0.38, self.height * y_positions[i],
                             arcade.color.BEAVER, 25, anchor_x="right", anchor_y="center", font_name="Tahoma")

            current_key = self.settings["controls"][self.player][action_keys[i]]
            arcade.draw_text(f"[{current_key.upper()}]", self.width * 0.65, self.height * y_positions[i],
                             arcade.color.YELLOW if self.waiting_for_key == action_keys[i] else arcade.color.BEAVER,
                             25, anchor_x="left", anchor_y="center", font_name="Tahoma")

        if self.waiting_for_key:
            waiting_name = action_names[action_keys.index(
                self.waiting_for_key)]
            arcade.draw_text(f"Нажмите клавишу для: {waiting_name}",
                             self.width // 2, self.height * 0.8,
                             arcade.color.RED, 30, anchor_x="center", anchor_y="center")

    def onBtn_Click(self, btn):
        if btn == "player1":
            self.player = "player_1"
            self.waiting_for_key = False
        elif btn == "player2":
            self.player = "player_2"
            self.waiting_for_key = False
        elif btn == "Back":
            from scripts.Class.Settings import SettingsObject
            settings = SettingsObject(self.window)
            self.window.show_view(settings)

    def on_action_click(self, action):
        self.waiting_for_key = action

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.ESCAPE:
            self.waiting_for_key = False

        if self.waiting_for_key:
            key_char = chr(symbol)
            self.settings["controls"][self.player][self.waiting_for_key] = key_char

            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)

            self.waiting_for_key = False

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
