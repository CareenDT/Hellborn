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
        bg = GameObject("Background", Transform(WIDTH // 2, HEIGHT // 2))
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
            'uppercut': arcade.key.Q,
            'awaken': arcade.key.SPACE
        }

        player2_controls = {
            'left': arcade.key.NUM_4,
            'right': arcade.key.NUM_6,
            'jump': arcade.key.NUM_8,
            'attack': arcade.key.NUM_9,
            'uppercut': arcade.key.NUM_7,
            'awaken': arcade.key.SPACE
        }

        self.syorma1 = Syorma("Syorma1", Transform(WIDTH // 4, 500), self.Object_Batch, scale=6.0,
                              controls=player1_controls)
        self.game_objects.append(self.syorma1)
        self.players.append(self.syorma1)
        self.syorma2 = Syorma("Syorma2", Transform(WIDTH * 3 // 4, 500), self.Object_Batch, scale=6.0,
                              controls=player2_controls)
        self.game_objects.append(self.syorma2)
        self.players.append(self.syorma2)

        self.arena_left = 50
        self.arena_right = WIDTH - 50
        self.arena_top = HEIGHT - 50
        self.arena_bottom = 150

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
        hp_bar_center_x = current_width // 2
        hp_bar_center_y = current_height * 0.9
        large_scale = 6.0
        hp_bar_sprite = arcade.Sprite("assets/images/FightUi/hp_bar.png",
                                      center_x=hp_bar_center_x,
                                      center_y=hp_bar_center_y)
        hp_bar_sprite.scale = large_scale
        self.ui_sprite_list.append(hp_bar_sprite)
        if self.syorma1:
            char_comp1 = self.syorma1.get_component(CharacterComponent)
            if char_comp1:
                hp_percentage1 = char_comp1.health / char_comp1.max_health
                self._draw_hp_fill(hp_bar_center_x, hp_bar_center_y, hp_percentage1,
                                   arcade.color.YELLOW, large_scale, flip=False)
        if self.syorma2:
            char_comp2 = self.syorma2.get_component(CharacterComponent)
            if char_comp2:
                hp_percentage2 = char_comp2.health / char_comp2.max_health
                self._draw_hp_fill(hp_bar_center_x, hp_bar_center_y, hp_percentage2,
                                   arcade.color.YELLOW, large_scale, flip=True)
        if self.syorma1:
            self._draw_player_ui(self.syorma1, current_width * 0.1, current_height * 0.87,
                                 "Player 1", arcade.color.PURPLE, scale=1, flip=False)
        if self.syorma2:
            self._draw_player_ui(self.syorma2, current_width * 0.9, current_height * 0.87,
                                 "Player 2", arcade.color.YELLOW, scale=1, flip=True)
        self.ui_sprite_list.draw(pixelated=True)

    def on_update(self, delta_time):
        for obj in self.game_objects:
            obj.update(delta_time)

        if self.syorma1 and self.syorma2:
            char_comp1 = self.syorma1.get_component(CharacterComponent)
            char_comp2 = self.syorma2.get_component(CharacterComponent)

            if char_comp1 and char_comp2:
                old_facing1 = char_comp1.facing_right
                if self.syorma1.transform.position.x < self.syorma2.transform.position.x:
                    char_comp1.facing_right = True
                else:
                    char_comp1.facing_right = False

                old_facing2 = char_comp2.facing_right
                if self.syorma2.transform.position.x < self.syorma1.transform.position.x:
                    char_comp2.facing_right = True
                else:
                    char_comp2.facing_right = False

                if old_facing1 != char_comp1.facing_right and char_comp1.sprite_renderer and char_comp1.sprite_renderer.sprite:
                    char_comp1.sprite_renderer.sprite.scale_x = -abs(char_comp1.sprite_renderer.sprite.scale_x) if not char_comp1.facing_right else abs(char_comp1.sprite_renderer.sprite.scale_x)
                if old_facing2 != char_comp2.facing_right and char_comp2.sprite_renderer and char_comp2.sprite_renderer.sprite:
                    char_comp2.sprite_renderer.sprite.scale_x = -abs(char_comp2.sprite_renderer.sprite.scale_x) if not char_comp2.facing_right else abs(char_comp2.sprite_renderer.sprite.scale_x)

        self._check_hitbox_collisions()

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

    def _draw_hp_fill(self, center_x, center_y, hp_percentage, color, large_scale=6.0, flip=False):
        bar_width = 180 * large_scale
        bar_height = 6 * large_scale
        bar_left = center_x - (bar_width / 2)
        bar_bottom = center_y - (bar_height / 2)
        if flip:
            if hp_percentage > 0:
                fill_width = hp_percentage * (bar_width / 2)
                fill_left = center_x
                points = [
                    (fill_left, bar_bottom),
                    (fill_left + fill_width, bar_bottom),
                    (fill_left + fill_width, bar_bottom + bar_height),
                    (fill_left, bar_bottom + bar_height)
                ]
                arcade.draw_polygon_filled(points, color)
        else:
            if hp_percentage > 0:
                fill_width = hp_percentage * (bar_width / 2)
                fill_left = bar_left
                points = [
                    (fill_left, bar_bottom),
                    (fill_left + fill_width, bar_bottom),
                    (fill_left + fill_width, bar_bottom + bar_height),
                    (fill_left, bar_bottom + bar_height)
                ]
                arcade.draw_polygon_filled(points, color)

    def _draw_player_ui(self, character, x, y, player_label, color, scale=0.5, flip=False):
        char_comp = character.get_component(CharacterComponent)
        if not char_comp:
            return
        arcade.draw_text(player_label, x, y, color, 20 * scale, anchor_x="center")
        for i in range(3):
            heart_x = x + (i - 1) * 35 * scale
            heart_y = y + 30 * scale
            if i < char_comp.lives:
                heart_sprite = arcade.Sprite("assets/images/FightUi/1hp.png",
                                             center_x=heart_x,
                                             center_y=heart_y)
            else:
                heart_sprite = arcade.Sprite("assets/images/FightUi/0hp.png",
                                             center_x=heart_x,
                                             center_y=heart_y)
            heart_sprite.scale = scale
            if flip:
                heart_sprite.scale_x = -scale
            self.ui_sprite_list.append(heart_sprite)
        rage_y = 70
        rage_x = self.window.width * 0.25 if not flip else self.window.width * 0.75
        rage_bar_sprite = arcade.Sprite("assets/images/FightUi/rage_bar.png",
                                        center_x=rage_x,
                                        center_y=rage_y)
        rage_bar_sprite.scale = 2.5
        if flip:
            rage_bar_sprite.scale_x = -2.5
        self.ui_sprite_list.append(rage_bar_sprite)
        rage_percentage = min(char_comp.rage / 100, 1.0)
        rage_bar_width = 100 * 2.5
        rage_bar_height = 10 * 2.5
        rage_bar_left = rage_x - (rage_bar_width / 2)
        rage_bar_bottom = rage_y - (rage_bar_height / 2)
        if rage_percentage > 0:
            rage_left_fill_width = min(rage_percentage, 0.5) * rage_bar_width
            if rage_left_fill_width > 0:
                rage_left_points = [
                    (rage_bar_left, rage_bar_bottom),
                    (rage_bar_left + rage_left_fill_width, rage_bar_bottom),
                    (rage_bar_left + rage_left_fill_width, rage_bar_bottom + rage_bar_height),
                    (rage_bar_left, rage_bar_bottom + rage_bar_height)
                ]
                arcade.draw_polygon_filled(rage_left_points, arcade.color.PURPLE)
        if rage_percentage > 0.5:
            rage_right_fill_width = (rage_percentage - 0.5) * rage_bar_width
            if rage_right_fill_width > 0:
                rage_right_left = rage_x
                rage_right_points = [
                    (rage_right_left, rage_bar_bottom),
                    (rage_right_left + rage_right_fill_width, rage_bar_bottom),
                    (rage_right_left + rage_right_fill_width, rage_bar_bottom + rage_bar_height),
                    (rage_right_left, rage_bar_bottom + rage_bar_height)
                ]
                arcade.draw_polygon_filled(rage_right_points, arcade.color.PURPLE)

    def _check_hitbox_collisions(self):
        if not self.syorma1 or not self.syorma2:
            return

        char_comp1 = self.syorma1.get_component(CharacterComponent)
        char_comp2 = self.syorma2.get_component(CharacterComponent)

        if not char_comp1 or not char_comp2:
            return

        attack_hitboxes1 = char_comp1.get_attack_hitboxes()
        hurtbox2 = char_comp2.get_hurt_hitbox()
        for attack_hitbox in attack_hitboxes1:
            if hurtbox2:
                if attack_hitbox.check_collision(hurtbox2):
                    char_comp2.take_damage(attack_hitbox.damage, attack_hitbox.knockback_force, attack_hitbox.hitstun_duration)
                    attack_hitbox.active = False

        attack_hitboxes2 = char_comp2.get_attack_hitboxes()
        hurtbox1 = char_comp1.get_hurt_hitbox()
        for attack_hitbox in attack_hitboxes2:
            if hurtbox1:
                if attack_hitbox.check_collision(hurtbox1):
                    char_comp1.take_damage(attack_hitbox.damage, attack_hitbox.knockback_force, attack_hitbox.hitstun_duration)
                    attack_hitbox.active = False

        if char_comp1.lives <= 0 or char_comp2.lives <= 0:
            self._game_over()

    def _game_over(self):
        from scripts.Menu import Menu
        menu = Menu(self.window)
        self.window.show_view(menu)
