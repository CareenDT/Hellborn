from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Character.CharacterComponent import CharacterComponent, CharacterStats
import os
from scripts.Class.Animation.AnimationSystem import CharacterState
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent

class Syorma(GameObject):
    def __init__(self, name: str = "Syorma", transform: Transform = Transform(500, 100), sprite_list=None, scale=2.0, controls=None):
        super().__init__(name, transform)

        default_image = "assets/images/characters/syorma/Base/base.png"
        if not os.path.exists(default_image):
            default_image = "assets/Preview.png"

        sprite_renderer = SpriteRendererComponent(
            image_path=default_image,
            scale=scale,
            sprite_list=sprite_list
        )
        self.add_component(sprite_renderer)

        stats = CharacterStats(
            max_health=120,
            base_damage=12,
            speed=180,
            defense=0.8
        )

        character = SyormaCharacterComponent(stats=stats, controls=controls)
        self.add_component(character)

class SyormaCharacterComponent(CharacterComponent):
    def __init__(self, stats, game_object=None, controls=None):
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
        self.uppercut_cooldown_time = 2.0
        self.awoken_timer = 0
        self.awoken_duration = 30.0

        self.attack_animation_started = False
        self.last_frame_index = 0

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

        if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT, CharacterState.JUMP]:
            current_frame = getattr(self.animation, 'frame_index', 0)
            if current_frame != self.last_frame_index:
                if current_frame == 0 and self.last_frame_index > 0:
                    if self.combo_timer <= 0:
                        self.change_state(CharacterState.IDLE)
                self.last_frame_index = current_frame

        if self.is_awoken:
            self.awoken_timer += delta_time
            if self.awoken_timer >= self.awoken_duration:
                self.is_awoken = False
                self.awoken_timer = 0
                self.speed = self.base_speed
                if self.game_object:
                    self.game_object.transform.scale_x = self.base_scale
                    self.game_object.transform.scale_y = self.base_scale
                if self.sprite_renderer and self.sprite_renderer.sprite:
                    self.sprite_renderer.sprite.scale = self.base_scale
                self._setup_animations()

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
        """Deal damage to another character"""
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
        else:
            return [0.25] * frame_count

    def _setup_animations(self):
        super()._setup_animations()
        assets_dir = "assets/images/characters/syorma/"

        animations = {
            CharacterState.IDLE: ["Base/base.png", "Base/idle/1.png", "Base/idle/2.png"],
            CharacterState.WALK_FORWARD: ["Base/base.png", "Base/walk/1.png", "Base/walk/2.png"],
            CharacterState.WALK_BACKWARD: ["Base/base.png", "Base/walk_back/1.png", "Base/walk_back/2.png"],
            CharacterState.PUNCH1: ["Base/base.png", "Base/M1_1/1.png", "Base/M1_1/2.png", "Base/M1_1/1.png"],
            CharacterState.PUNCH2: ["Base/base.png", "Base/M1_2/1.png", "Base/M1_2/2.png", "Base/M1_2/1.png"],
            CharacterState.KICK: ["Base/base.png", "Base/M1_4/1.png", "Base/M1_4/2.png", "Base/M1_4/1.png"],
            CharacterState.UPPERCUT: [
                "Base/base.png",
                "Base/uppercut/1.png",
                "Base/uppercut/2.png",
                "Base/uppercut/3.png",
                "Base/uppercut/4.png",
                "Base/uppercut/5.png",
                "Base/uppercut/6.png",
                "Base/uppercut/7.png"
            ],
            CharacterState.JUMP: ["Base/jump/1.png", "Base/jump/2.png", "Base/jump/1.png"],
        }

        for state, filenames in animations.items():
            frame_paths = []
            for filename in filenames:
                if self.is_awoken:
                    awoken_path = os.path.join(assets_dir, "Awoken", filename)
                    if os.path.exists(awoken_path):
                        frame_paths.append(awoken_path)
                        continue
                full_path = os.path.join(assets_dir, filename)
                if os.path.exists(full_path):
                    frame_paths.append(full_path)
                else:
                    frame_paths.append("assets/Preview.png")

            if frame_paths:
                durations = self._get_frame_durations(state, len(frame_paths))
                self.animation.add_animation(state, frame_paths, durations)


