from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Character.CharacterComponent import CharacterComponent, CharacterStats
import os
import random
from scripts.Class.Animation.AnimationSystem import CharacterState
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
from scripts.Class.Component.Hitbox import HitboxComponent, HitboxType

class DarkKnight(GameObject):
    def __init__(self, name: str = "DarkKnight", transform: Transform = Transform(500, 100), sprite_list=None, scale=2.0, controls=None):
        super().__init__(name, transform)

        default_image = "assets/images/characters/dark_knight/idle/1.png"

        sprite_renderer = SpriteRendererComponent(
            image_path=default_image,
            scale=scale,
            sprite_list=sprite_list
        )
        self.add_component(sprite_renderer)

        stats = CharacterStats(
            max_health=140,
            base_damage=14,
            speed=250,
            defense=0.75
        )

        character = DarkKnightCharacterComponent(stats=stats, controls=controls, sprite_list=sprite_list)
        self.add_component(character)

class DarkKnightCharacterComponent(CharacterComponent):
    def __init__(self, stats, game_object=None, controls=None, sprite_list=None):
        super().__init__(game_object, controls)
        self.stats = stats
        self.speed = stats.speed
        self.base_damage = stats.base_damage
        self.max_health = stats.max_health
        self.defense = stats.defense
        self.combo_step = 0
        self.combo_timer = 0
        self.combo_window = 1.0
        self.uppercut_cooldown = 0
        self.uppercut_cooldown_time = 10.0  
        self.awoken_timer = 0
        self.awoken_duration = 0  
        self.potion_boost_timer = 0
        self.potion_boost_duration = 10.0  
        self.potion_type = None  

        self.attack_animation_started = False
        self.last_frame_index = 0

    def start(self):
        super().start()
        hurtbox = HitboxComponent(HitboxType.HURT, damage=0, width=150, height=200, offset_x=0, offset_y=0)
        hurtbox.active = True
        self.add_hitbox(hurtbox)
        self.punch1_hitbox = HitboxComponent(HitboxType.ATTACK, damage=self.base_damage, width=80, height=60, offset_x=80, offset_y=0, knockback_force=150, hitstun_duration=0.3)
        self.add_hitbox(self.punch1_hitbox)
        self.punch2_hitbox = HitboxComponent(HitboxType.ATTACK, damage=self.base_damage, width=75, height=60, offset_x=72.5, offset_y=0, knockback_force=180, hitstun_duration=0.4)
        self.add_hitbox(self.punch2_hitbox)
        self.kick_hitbox = HitboxComponent(HitboxType.ATTACK, damage=self.base_damage * 1.5, width=100, height=70, offset_x=95, offset_y=0, knockback_force=300, hitstun_duration=0.6)
        self.add_hitbox(self.kick_hitbox)
        self.uppercut_hitbox = HitboxComponent(HitboxType.ATTACK, damage=self.base_damage * 2, width=200, height=50, offset_x=100, offset_y=0, knockback_force=400, hitstun_duration=0.8)  
        self.add_hitbox(self.uppercut_hitbox)

    def on_draw(self):
        super().on_draw()

    def update(self, delta_time):
        super().update(delta_time)

        if self.combo_timer > 0:
            self.combo_timer -= delta_time
            if self.combo_timer <= 0:
                self.combo_step = 0

        if self.uppercut_cooldown > 0:
            self.uppercut_cooldown -= delta_time

        if self.potion_boost_timer > 0:
            self.potion_boost_timer -= delta_time
            if self.potion_boost_timer <= 0:
                self.reset_stats()

        if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT, CharacterState.JUMP]:
            current_frame = getattr(self.animation, 'frame_index', 0)
            if current_frame != self.last_frame_index:
                if current_frame == 0 and self.last_frame_index > 0:
                    if self.combo_timer <= 0:
                        self.change_state(CharacterState.IDLE)
                self.last_frame_index = current_frame

    def attack(self):
        if self.uppercut_cooldown > 0:
            return

        if self.combo_timer > 0:
            self.combo_step += 1
        else:
            self.combo_step = 1

        if self.combo_step == 1:
            self.change_state(CharacterState.PUNCH1)
            self.punch1_hitbox.activate(0.2)
        elif self.combo_step == 2:
            self.change_state(CharacterState.PUNCH2)
            self.punch2_hitbox.activate(0.2)
        elif self.combo_step == 3:
            self.change_state(CharacterState.PUNCH1)
            self.punch1_hitbox.activate(0.2)
        elif self.combo_step == 4:
            self.change_state(CharacterState.KICK)
            self.kick_hitbox.activate(0.3)
            self.combo_step = 0
        else:
            self.combo_step = 0

        self.combo_timer = self.combo_window
        self.velocity_x = 0

    def uppercut(self):
        if self.uppercut_cooldown > 0:
            return

        self.change_state(CharacterState.UPPERCUT)
        self.uppercut_hitbox.activate(0.5)
        
        dash_distance = 200
        if self.facing_right:
            self.velocity_x += dash_distance / 0.5  
        else:
            self.velocity_x -= dash_distance / 0.5
        self.velocity_x = 0  
        self.uppercut_cooldown = self.uppercut_cooldown_time

    def take_damage(self, damage: float, knockback_force: float = 0, hitstun_duration: float = 0.5):
        super().take_damage(damage, knockback_force, hitstun_duration)
        self.rage += damage
        if self.rage > 100:
            self.rage = 100

    def deal_damage(self, target, damage: float):
        if target and hasattr(target, 'take_damage'):
            target.take_damage(damage)

    def awaken(self):
        if self.rage >= 100:
            self.rage = 0
            
            potions = ['damage', 'heal', 'speed']
            self.potion_type = random.choice(potions)
            self.potion_boost_timer = self.potion_boost_duration
            if self.potion_type == 'damage':
                self.base_damage *= 1.5
                
                self.punch1_hitbox.damage = self.base_damage
                self.punch2_hitbox.damage = self.base_damage
                self.kick_hitbox.damage = self.base_damage * 1.5
                self.uppercut_hitbox.damage = self.base_damage * 2
            elif self.potion_type == 'heal':
                self.health = min(self.health + 50, self.max_health)
            elif self.potion_type == 'speed':
                self.speed *= 1.5

    def reset_stats(self):
        self.base_damage = self.stats.base_damage
        self.speed = self.stats.speed
        
        self.punch1_hitbox.damage = self.base_damage
        self.punch2_hitbox.damage = self.base_damage
        self.kick_hitbox.damage = self.base_damage * 1.5
        self.uppercut_hitbox.damage = self.base_damage * 2
        self.potion_type = None

    def _get_frame_durations(self, state: CharacterState, frame_count: int) -> list[float]:
        if state == CharacterState.IDLE:
            return [0.4] * frame_count
        elif state in [CharacterState.WALK_FORWARD, CharacterState.WALK_BACKWARD]:
            return [0.15] * frame_count
        elif state in [CharacterState.PUNCH1, CharacterState.PUNCH2]:
            return [0.08] * frame_count
        elif state == CharacterState.KICK:
            return [0.01, 0.3, 0.08, 0.08]
        elif state == CharacterState.UPPERCUT:
            return [0.1] * frame_count
        elif state == CharacterState.JUMP:
            return [0.2, 0.3, 0.2]
        elif state == CharacterState.DAMAGE:
            return [0.1] * frame_count
        else:
            return [0.25] * frame_count

    def _setup_animations(self):
        super()._setup_animations()
        assets_dir = "assets/images/characters/dark_knight/"

        animations = {
            CharacterState.IDLE: ["idle/1.png", "idle/2.png"],
            CharacterState.WALK_FORWARD: ["walk/1.png", "walk/2.png"],
            CharacterState.WALK_BACKWARD: ["walk_back/1.png", "walk_back/2.png"],
            CharacterState.PUNCH1: ["M1_1/1.png", "M1_1/2.png", "M1_1/1.png"],
            CharacterState.PUNCH2: ["M1_2/1.png", "M1_2/2.png", "M1_2/1.png"],
            CharacterState.KICK: ["M1_4/1.png", "M1_4/2.png", "M1_4/3.png"],
            CharacterState.UPPERCUT: ["bull/1.png", "bull/2.png", "bull/3.png", "bull/4.png", "bull/5.png"],
            CharacterState.JUMP: ["jump/1.png", "jump/2.png", "jump/base.png"],
            CharacterState.DAMAGE: ["damage/1.png", "damage/2.png", "damage/3.png", "damage/4.png", "damage/5.png", "damage/6.png", "damage/7.png"],
        }

        for state, filenames in animations.items():
            frame_paths = []
            for filename in filenames:
                full_path = os.path.join(assets_dir, filename)
                if os.path.exists(full_path):
                    frame_paths.append(full_path)
                else:
                    frame_paths.append("assets/Preview.png")

            if frame_paths:
                durations = self._get_frame_durations(state, len(frame_paths))
                self.animation.add_animation(state, frame_paths, durations)
