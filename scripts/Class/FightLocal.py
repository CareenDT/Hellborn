import arcade
from scripts.Class.Character.CharacterComponent import CharacterComponent
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
from scripts.Class.Character.Syorma import Syorma
from scripts.globals import WIDTH, HEIGHT

class FightLocal(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window
        self.game_objects = []
        self.Object_Batch = arcade.SpriteList()
        self.ui_sprite_list = arcade.SpriteList()
        self.keys_pressed = set()
        self.players = []

        self.world_camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()


        self._setup()

    def _setup(self):
        bg = GameObject("Background", Transform(WIDTH//2, HEIGHT//2))
        bg_renderer = SpriteRendererComponent(
            "assets/arena.png",
            scale=1.0,
            sprite_list=self.Object_Batch
        )
        bg.add_component(bg_renderer)
        self.game_objects.append(bg)
        if bg_renderer.sprite:
            original_width = bg_renderer.sprite.texture.width
            original_height = bg_renderer.sprite.texture.height
            custom_height = HEIGHT
            custom_width = HEIGHT * (original_width / original_height)
            bg_renderer.set_custom_size(custom_width, custom_height)
            bg_renderer.sprite.center_x = WIDTH // 2
            bg_renderer.sprite.center_y = HEIGHT // 2

        player1_controls = {
            'left': arcade.key.A,
            'right': arcade.key.D,
            'jump': arcade.key.W,
            'attack': arcade.key.E,
            'uppercut': arcade.key.Q
        }

        player2_controls = {
            'left': arcade.key.NUM_4,
            'right': arcade.key.NUM_6,
            'jump': arcade.key.NUM_8,
            'attack': arcade.key.NUM_9,
            'uppercut': arcade.key.NUM_7
        }

        self.syorma1 = Syorma("Syorma1", Transform(WIDTH//4, 500), self.Object_Batch, scale=4.0, controls=player1_controls)
        self.game_objects.append(self.syorma1)
        self.players.append(self.syorma1)
        self.syorma2 = Syorma("Syorma2", Transform(WIDTH*3//4, 500), self.Object_Batch, scale=4.0, controls=player2_controls)
        self.game_objects.append(self.syorma2)
        self.players.append(self.syorma2)

    def on_draw(self):
        self.clear()

        self.world_camera.use()
        for obj in self.game_objects:
            obj.draw()
        self.Object_Batch.draw(pixelated=True)
        arcade.draw_line(0, 150, WIDTH, 150, arcade.color.GREEN, 2)

        self.gui_camera.use()
        self.ui_sprite_list.clear()
        

        current_width = self.window.width
        current_height = self.window.height

        if self.syorma1:
            self._draw_player_ui(self.syorma1, current_width * 0.1, current_height * 0.9, "Player 1", arcade.color.BLUE, scale=1.5, flip=False)
        if self.syorma2:
            self._draw_player_ui(self.syorma2, current_width * 0.9, current_height * 0.9, "Player 2", arcade.color.RED, scale=1.5, flip=True)

        self.ui_sprite_list.draw(pixelated=True)

    def on_update(self, delta_time):
        for obj in self.game_objects:
            obj.update(delta_time)

        Middle = self.syorma1.transform.position.lerp(self.syorma2.transform.position,0.5)

        self.world_camera.position = (self.world_camera.position.lerp(Middle, 0.02) * arcade.Vec2(1,0)) + arcade.Vec2(0,self.world_camera.viewport.height//2)

    def on_key_press(self, key: int, modifiers: int):
        self.keys_pressed.add(key)
        if key == arcade.key.ESCAPE:
            from scripts.Menu import MenuObject
            menu_view = MenuObject(self.window)
            self.window.show_view(menu_view)

        if self.syorma1:
            char_comp1 = self.syorma1.get_component(CharacterComponent)
            if char_comp1:
                char_comp1.handle_key_press(key)

        if self.syorma2:
            char_comp2 = self.syorma2.get_component(CharacterComponent)
            if char_comp2:
                char_comp2.handle_key_press(key)

    def on_key_release(self, key: int, modifiers: int):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)

        if self.syorma1:
            char_comp1 = self.syorma1.get_component(CharacterComponent)
            if char_comp1:
                char_comp1.handle_key_release(key)

        if self.syorma2:
            char_comp2 = self.syorma2.get_component(CharacterComponent)
            if char_comp2:
                char_comp2.handle_key_release(key)

    def _draw_player_ui(self, character, x, y, player_label, color, scale=0.5, flip=False):
        char_comp = character.get_component(CharacterComponent)
        if not char_comp:
            return

        bar_offset = 100 * scale if not flip else -100 * scale
        fill_start = x + 50 * scale if not flip else x - 50 * scale
        heart_start = x + 200 * scale if not flip else x - 200 * scale
        heart_step = 30 * scale if not flip else -30 * scale

        arcade.draw_text(player_label, x, y, color, 20 * scale)

        hp_bar_sprite = arcade.Sprite("assets/images/FightUi/hp_bar.png", center_x=x + bar_offset, center_y=y - 20 * scale)
        hp_bar_sprite.scale = scale
        if flip:
            hp_bar_sprite.scale_x = -scale
        self.ui_sprite_list.append(hp_bar_sprite)

        hp_percentage = char_comp.health / char_comp.max_health
        hp_fill_width = 100 * scale * hp_percentage
        fill_x = fill_start if not flip else fill_start - hp_fill_width
        arcade.draw_rect_filled(arcade.rect.XYWH(fill_x, y - 20 * scale, hp_fill_width, 10 * scale), arcade.color.RED)

        rage_bar_sprite = arcade.Sprite("assets/images/FightUi/rage_bar.png", center_x=x + bar_offset, center_y=y - 40 * scale)
        rage_bar_sprite.scale = scale
        if flip:
            rage_bar_sprite.scale_x = -scale
        self.ui_sprite_list.append(rage_bar_sprite)

        rage_percentage = min(char_comp.rage / 100, 1.0)
        rage_fill_width = 100 * scale * rage_percentage
        fill_x = fill_start if not flip else fill_start - rage_fill_width
        arcade.draw_rect_filled(arcade.rect.XYWH(fill_x, y - 40 * scale, rage_fill_width, 10 * scale), arcade.color.PURPLE)

        for i in range(3):
            heart_x = heart_start + i * heart_step
            heart_y = y - 10 * scale
            if i < char_comp.lives:
                heart_sprite = arcade.Sprite("assets/images/FightUi/1hp.png", center_x=heart_x, center_y=heart_y)
            else:
                heart_sprite = arcade.Sprite("assets/images/FightUi/0hp.png", center_x=heart_x, center_y=heart_y)
            heart_sprite.scale = scale
            if flip:
                heart_sprite.scale_x = -scale
            self.ui_sprite_list.append(heart_sprite)
