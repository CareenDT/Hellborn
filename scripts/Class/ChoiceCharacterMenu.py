import arcade
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *


class CharacterChoiceObject(arcade.View):
    def __init__(self, window):
        super().__init__(window)
        self.window = window
        self.Object_Batch = arcade.SpriteList()
        self.background_sprite_list = arcade.SpriteList()
        self.game_objects = []
        self.time_elapsed = 0

        self.a = 0

        self.background = GameObject("Background", Transform(self.window.width // 2, self.window.height // 2))
        bg_renderer = SpriteRendererComponent("assets/bg_menu.png", 1.0, self.background_sprite_list)
        bg_renderer.set_custom_size(self.window.width, self.window.height)
        self.background.add_component(bg_renderer)

        self.selection_panel = GameObject("SelectionPanel", Transform())
        self.selection_panel.add_component(ScreenRelativeTransform(self, 0.5, 0.5, 0.8, 0.8))
        self.game_objects.append(self.selection_panel)

        panel_width = 0.5 * self.window.width
        btn_width = 0.8 * panel_width
        btn_height = btn_width * (32 / 128)

        #self.title = GameObject("Title", Transform())
        #self.title.add_component(ScreenRelativeTransform(self.selection_panel, 0, 0.4, 1, 1))
        #title_renderer = SpriteRendererComponent("assets/images/hellborn.png", 1, self.Object_Batch)
        #title_renderer.set_custom_size(btn_width * 1.2, btn_height * 0.9)
        #self.title.add_component(title_renderer)
        #self.game_objects.append(self.title)

        self.characters = ["Syorma", "ShadowTent", "DarkKnight"]
        self.path_textures = ["assets/images/syrma.png",
                              "assets/images/s_t.png",
                              "assets/images/knight.png"]
        self.current_player = 1
        self.selected_characters = {1: None, 2: None}
        self.current_selection = 0

        self.c_sprites = []
        c_spacing = 0.3
        char_y = 0.0

        for i in range(len(self.characters)):
            c_obj = GameObject(f"Char_{i}", Transform())
            c_obj.add_component(
                ScreenRelativeTransform(self.selection_panel, (i - 1) * c_spacing, char_y, 0.25, 0.8))

            c_renderer = SpriteRendererComponent(self.path_textures[i], 1, self.Object_Batch)
            c_renderer.set_custom_size(btn_width * 0.2, btn_height * 0.8)
            c_obj.add_component(c_renderer)
            self.game_objects.append(c_obj)
            self.c_sprites.append(c_obj)

        self.selection_arrow = GameObject("SelectionArrow", Transform())
        self.selection_arrow.add_component(ScreenRelativeTransform(self.selection_panel, -0.3, 0.15, 0.15, 0.3))
        arrow_renderer = SpriteRendererComponent("assets/images/down_btn.png", 1, self.Object_Batch)
        arrow_renderer.set_custom_size(btn_width * 0.15, btn_height * 0.3)
        arrow_renderer.sprite.angle = 90
        self.selection_arrow.add_component(arrow_renderer)
        self.game_objects.append(self.selection_arrow)

        self.btn_back = GameObject("Back", Transform())
        self.btn_back.add_component(ScreenRelativeTransform(self.selection_panel, 0, -0.35, 0.4, 0.15))
        btn_back_renderer = SpriteRendererComponent("assets/images/return.png", 1, self.Object_Batch)
        btn_back_renderer.set_custom_size(btn_width * 0.6, btn_height * 0.4)
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

        arcade.draw_text(f"Игрок {self.current_player} выбирает",
                         self.width // 2, self.height * 0.74,
                         arcade.color.BEAVER, 30, anchor_x="center", anchor_y="center",
                         font_name="Tahoma")

        arcade.draw_text("Игрок 1", self.width * 0.15, self.height * 0.65,
                         arcade.color.PURPLE, 24, anchor_x="center", anchor_y="center")

        if self.selected_characters[1]:
            arcade.draw_text(self.selected_characters[1], self.width * 0.15, self.height * 0.6,
                             arcade.color.BEAVER, 20, anchor_x="center", anchor_y="center",
                             font_name="Tahoma")
        else:
            arcade.draw_text("Не выбран", self.width * 0.15, self.height * 0.6,
                             arcade.color.GRAY, 20, anchor_x="center", anchor_y="center")

        arcade.draw_text("Игрок 2", self.width * 0.85, self.height * 0.65,
                         arcade.color.PURPLE, 24, anchor_x="center", anchor_y="center")

        if self.selected_characters[2]:
            arcade.draw_text(self.selected_characters[2], self.width * 0.85, self.height * 0.6,
                             arcade.color.BEAVER, 20, anchor_x="center", anchor_y="center",
                             font_name="Tahoma")
        else:
            arcade.draw_text("Не выбран", self.width * 0.85, self.height * 0.6,
                             arcade.color.GRAY, 20, anchor_x="center", anchor_y="center")

        arcade.draw_text(f"Выбран: {self.characters[self.current_selection]}",
                         self.width // 2, self.height * 0.35,
                         arcade.color.YELLOW, 25, anchor_x="center", anchor_y="center")

        arcade.draw_text("A/D: двигать  W: выбрать",
                         self.width // 2, self.height * 0.1,
                         arcade.color.RUBY, 30, anchor_x="center", anchor_y="center",
                         font_name="Tahoma")

    def onBtn_Click(self, btn):
        if btn == "Back":
            from scripts.Menu import MenuObject
            menu = MenuObject(self.window)
            self.window.show_view(menu)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.A:
            self.current_selection = (self.current_selection - 1) % len(self.characters)
            self.update_arrow_position()
        elif symbol == arcade.key.D:
            self.current_selection = (self.current_selection + 1) % len(self.characters)
            self.update_arrow_position()
        elif symbol == arcade.key.W:
            self.selected_characters[self.current_player] = self.characters[self.current_selection]

            if self.current_player == 1:
                self.current_player = 2
            else:
                self.a = True
                self.w_t = self.time_elapsed + 0.5

    def update_arrow_position(self):
        c_s = 0.3
        x_pos = (self.current_selection - 1) * c_s
        self.selection_arrow.add_component(ScreenRelativeTransform(self.selection_panel, x_pos, 0.15, 0.15, 0.3))


    def start_fight(self):
        from scripts.Class.FightLocal import FightLocal
        fight = FightLocal(self.window, self.selected_characters[1], self.selected_characters[2])
        self.window.show_view(fight)

    def on_update(self, delta_time):
        self.time_elapsed += delta_time
        for obj in self.game_objects:
            obj.update(delta_time)

        if self.a:
            if self.w_t < self.time_elapsed:
                self.start_fight()

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