import arcade
import os
from scripts.Class.GameObject import Component
from scripts.Class.Animation.AnimationSystem import CharacterState, CharacterAnimation

class CharacterStats():
    def __init__(self,max_health=120, base_damage=12, speed=180, defense=0.8):
        self.max_health=max_health
        self.base_damage=base_damage
        self.speed=speed
        self.defense=defense


class CharacterComponent(Component):
    def __init__(self, game_object=None):
        super().__init__(game_object)
        self.speed = 180
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.is_on_ground = False
        self.ground_level = 150
        self.animation = CharacterAnimation()
        self.current_state = CharacterState.IDLE
        self.sprite_renderer = None
        self.rage = 0
        self.is_awoken = False
        self.base_speed = 180
        self.base_scale = 2.0
    
    def start(self):
        from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
        self.sprite_renderer = self.game_object.get_component(SpriteRendererComponent)
        self._setup_animations()
        self.change_state(CharacterState.IDLE)
    
    def _setup_animations(self):
        pass
    
    def change_state(self, new_state: CharacterState):
        if new_state != self.current_state:
            if self.animation.change_state(new_state):
                self.current_state = new_state
                if self.sprite_renderer:
                    texture = self.animation.get_current_texture()
                    if texture:
                        self.sprite_renderer.set_texture(texture)
    
    def update(self, delta_time):
        super().update(delta_time)
        self.animation.update(delta_time)

        if hasattr(self.animation, 'is_complete') and self.animation.is_complete:
            if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT]:
                self.change_state(CharacterState.IDLE)

        if self.sprite_renderer:
            texture = self.animation.get_current_texture()
            if texture:
                self.sprite_renderer.set_texture(texture)

        if self.game_object and self.game_object.transform:
            t = self.game_object.transform
            t.x += self.velocity_x * delta_time
            t.y += self.velocity_y * delta_time
            GRAVITY = 500
            self.velocity_y -= GRAVITY * delta_time
            if t.y <= self.ground_level:
                t.y = self.ground_level
                self.velocity_y = 0
                self.is_on_ground = True
    
    def move(self, direction: int):
        if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT]:
            self.velocity_x = 0
            return

        self.velocity_x = direction * self.speed
        if direction != 0:
            self.facing_right = direction > 0
            if direction > 0:
                self.change_state(CharacterState.WALK_FORWARD)
            else:
                self.change_state(CharacterState.WALK_BACKWARD)
        else:
            self.change_state(CharacterState.IDLE)
    
    def jump(self):
        if self.is_on_ground:
            self.velocity_y = 400
            self.is_on_ground = False
    
    def attack(self):
        if self.uppercut_cooldown > 0:
            return

        if self.combo_timer > 0:
            self.combo_step += 1
        else:
            self.combo_step = 1

        if self.combo_step == 1:
            self.change_state(CharacterState.PUNCH1)
        elif self.combo_step == 2:
            self.change_state(CharacterState.PUNCH2)
        elif self.combo_step == 3:
            self.change_state(CharacterState.PUNCH1)
        elif self.combo_step == 4:
            self.change_state(CharacterState.KICK)
            self.combo_step = 0
        else:
            self.combo_step = 0

        self.combo_timer = self.combo_window
        self.velocity_x = 0
    
    def uppercut(self):
        if self.uppercut_cooldown > 0:
            return

        self.change_state(CharacterState.UPPERCUT)
        if self.is_on_ground:
            self.velocity_y = 300
            self.is_on_ground = False
        self.velocity_x = 0
        self.uppercut_cooldown = self.uppercut_cooldown_time
    
    def take_damage(self, damage: float):
        self.rage += damage
        if self.rage > 100:
            self.rage = 100

    def deal_damage(self, target, damage: float):
        if target and hasattr(target, 'take_damage'):
            target.take_damage(damage)
    
    def awaken(self):
        if not self.is_awoken and self.rage >= 100:
            self.is_awoken = True
            self.rage = 0
            self.speed = self.base_speed * 1.5
            if self.game_object:
                self.game_object.transform.scale_x = self.base_scale * 1.2
                self.game_object.transform.scale_y = self.base_scale * 1.2
            if self.sprite_renderer and self.sprite_renderer.sprite:
                self.sprite_renderer.sprite.scale = self.base_scale * 1.2