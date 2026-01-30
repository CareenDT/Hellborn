import arcade
import os
from scripts.Class.GameObject import Component
from scripts.Class.Animation.AnimationSystem import CharacterState, CharacterAnimation
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
from scripts.Class.Component.Hitbox import HitboxComponent, HitboxType

class CharacterStats():
    def __init__(self,max_health=120, base_damage=12, speed=180, defense=0.8, lives=3):
        self.max_health=max_health
        self.base_damage=base_damage
        self.speed=speed
        self.defense=defense
        self.lives=lives


class CharacterComponent(Component):
    def __init__(self, game_object=None, controls=None):
        super().__init__(game_object)
        self.controls = controls or {
            'left': arcade.key.A,
            'right': arcade.key.D,
            'jump': arcade.key.W,
            'attack': arcade.key.J,
            'uppercut': arcade.key.K,
            'awaken': arcade.key.SPACE
        }
        self.speed = 300
        self.facing_right = True
        self.velocity_x = 0
        self.velocity_y = 0
        self.friction = 0.85
        self.is_on_ground = False
        self.ground_level = 150
        self.animation = CharacterAnimation()
        self.current_state = CharacterState.IDLE
        self.sprite_renderer = None
        self.rage = 0
        self.is_awoken = False
        self.base_speed = 180
        self.base_scale = 2.0
        self.health = 120
        self.max_health = 120
        self.lives = 3
        self.left_pressed = False
        self.right_pressed = False
        self.hitboxes = []
        self.hurtbox = None
        self.combo_step = 0
        self.combo_timer = 0
        self.combo_window = 1.0
        self.uppercut_cooldown = 0
        self.uppercut_cooldown_time = 2.0
        self.hitstun_timer = 0
        self.is_in_hitstun = False
        self.is_awakening = False
        self.awaken_charge_timer = 0
        self.awaken_charge_duration = 2.0
        self.awaken_timer = 0
        self.awaken_duration = 25.0
        self.combo_cooldown = 0
        self.combo_cooldown_time = 1.0
    
    def start(self):
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
                if self.sprite_renderer.sprite:
                    self.sprite_renderer.sprite.scale_x = -abs(self.sprite_renderer.sprite.scale_x) if not self.facing_right else abs(self.sprite_renderer.sprite.scale_x)
    
    def update(self, delta_time):
        super().update(delta_time)
        self.animation.update(delta_time)

        if self.combo_timer > 0:
            self.combo_timer -= delta_time
        if self.uppercut_cooldown > 0:
            self.uppercut_cooldown -= delta_time
        if self.hitstun_timer > 0:
            self.hitstun_timer -= delta_time
            if self.hitstun_timer <= 0:
                self.is_in_hitstun = False
        if self.is_awakening:
            self.awaken_charge_timer += delta_time
            if self.awaken_charge_timer >= self.awaken_charge_duration:
                self.is_awakening = False
                self.awaken_charge_timer = 0
                self.awaken()
        if self.is_awoken:
            self.awaken_timer += delta_time
            if self.awaken_timer >= self.awaken_duration:
                self.is_awoken = False
                self.awaken_timer = 0
                self.speed = self.base_speed
                if self.game_object:
                    self.game_object.transform.scale_x = self.base_scale
                    self.game_object.transform.scale_y = self.base_scale
                if self.sprite_renderer and self.sprite_renderer.sprite:
                    self.sprite_renderer.sprite.scale = self.base_scale
                self._setup_animations()

        if hasattr(self.animation, 'is_complete') and self.animation.is_complete:
            if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT]:
                self.change_state(CharacterState.IDLE)

        if self.sprite_renderer:
            texture = self.animation.get_current_texture()
            if texture:
                self.sprite_renderer.set_texture(texture)
                if self.sprite_renderer.sprite:
                    self.sprite_renderer.sprite.scale_x = -abs(self.sprite_renderer.sprite.scale_x) if not self.facing_right else abs(self.sprite_renderer.sprite.scale_x)

        if self.game_object and self.game_object.transform:
            t = self.game_object.transform
            t.x += self.velocity_x * delta_time
            t.y += self.velocity_y * delta_time

            if not self.left_pressed and not self.right_pressed:
                self.velocity_x *= self.friction

            GRAVITY = 500
            self.velocity_y -= GRAVITY * delta_time
            if t.y <= self.ground_level:
                t.y = self.ground_level
                self.velocity_y = 0
                self.is_on_ground = True

            arena_left = 50
            arena_right = 1920 - 50
            arena_top = 1080 - 50
            arena_bottom = 150

            if t.x < arena_left:
                t.x = arena_left
                self.velocity_x = 0
            elif t.x > arena_right:
                t.x = arena_right
                self.velocity_x = 0

            if t.y > arena_top:
                t.y = arena_top
                self.velocity_y = 0
    
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
    
    def take_damage(self, damage: float, knockback_force: float = 0, hitstun_duration: float = 0.5):
        self.health -= damage
        if self.health <= 0:
            self.health = self.max_health
            self.lives -= 1
            if self.lives <= 0:
                self.lives = 0
        self.rage += damage
        if self.rage > 100:
            self.rage = 100

        if knockback_force > 0:
            direction = -1 if self.facing_right else 1
            self.velocity_x += knockback_force * direction
            self.velocity_y += knockback_force * 0.5
        if hitstun_duration > 0:
            self.hitstun_timer = hitstun_duration
            self.is_in_hitstun = True
            self.change_state(CharacterState.IDLE)

    def deal_damage(self, target, damage: float):
        if target and hasattr(target, 'take_damage'):
            target.take_damage(damage)
    
    def awaken(self):
        if not self.is_awoken and self.rage >= 100:
            self.is_awoken = True
            self.rage = 0
            self.speed = self.base_speed * 1.5

    def handle_key_press(self, key: int):
        if key == self.controls['left']:
            self.left_pressed = True
        elif key == self.controls['right']:
            self.right_pressed = True
        elif key == self.controls['jump']:
            self.jump()
        elif key == self.controls['attack']:
            self.attack()
        elif key == self.controls['uppercut']:
            self.uppercut()
        elif key == self.controls['awaken']:
            self.awaken()
        self.update_movement()

    def handle_key_release(self, key: int):
        if key == self.controls['left']:
            self.left_pressed = False
        elif key == self.controls['right']:
            self.right_pressed = False
        self.update_movement()

    def update_movement(self):
        if self.is_in_hitstun:
            return

        if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT]:
            self.velocity_x = 0
            return

        if self.left_pressed and not self.right_pressed:
            self.velocity_x = -self.speed
            self.facing_right = False
            self.change_state(CharacterState.WALK_BACKWARD)
        elif self.right_pressed and not self.left_pressed:
            self.velocity_x = self.speed
            self.facing_right = True
            self.change_state(CharacterState.WALK_FORWARD)
        else:
            self.velocity_x = 0
            self.change_state(CharacterState.IDLE)

    def add_hitbox(self, hitbox: HitboxComponent):
        hitbox.game_object = self.game_object
        self.hitboxes.append(hitbox)
        if hitbox.hitbox_type == HitboxType.HURT:
            self.hurtbox = hitbox
        self.game_object.add_component(hitbox)

    def remove_hitbox(self, hitbox: HitboxComponent):
        if hitbox in self.hitboxes:
            self.hitboxes.remove(hitbox)
            if self.hurtbox == hitbox:
                self.hurtbox = None

    def get_attack_hitboxes(self):
        return [h for h in self.hitboxes if h.hitbox_type == HitboxType.ATTACK and h.active]

    def get_hurt_hitbox(self):
        return self.hurtbox if self.hurtbox and self.hurtbox.active else None
