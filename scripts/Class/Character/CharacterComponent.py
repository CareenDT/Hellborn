import arcade
from scripts.Class.GameObject import Component
from scripts.Class.Animation.AnimationSystem import CharacterState, CharacterAnimation

class CharacterStats:
    def __init__(self, max_health: float = 100, base_damage: float = 10, 
                 speed: float = 200, defense: float = 1.0):
        self.max_health = max_health
        self.current_health = max_health
        self.base_damage = base_damage
        self.speed = speed
        self.defense = defense
        self.rage = 0.0
        self.is_awoken = False

class CharacterComponent(Component):
    def __init__(self, game_object=None, stats: CharacterStats = None):
        super().__init__(game_object)
        self.stats = stats or CharacterStats()
        self.animation = CharacterAnimation()
        self.facing_right = True
        
        self.combo_step = 0
        self.combo_timer = 0.0
        self.combo_timeout = 0.5
        self.is_attacking = False
        self.attack_damage = 0
        
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.is_on_ground = True
        self.move_direction = 0
        
        self.sprite_renderer = None
    
    def start(self):
        try:
            from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
            self.sprite_renderer = self.game_object.get_component(SpriteRendererComponent)
            if self.sprite_renderer:
                self.animation.set_sprite_renderer(self.sprite_renderer)
        except ImportError:
            print("Note: SpriteRendererComponent not available")
        
        self._setup_animations()
        
        self.animation.change_state(CharacterState.IDLE)
    
    def _setup_animations(self):
        pass
    
    def update(self, delta_time):
        super().update(delta_time)
        
        if self.combo_step > 0:
            self.combo_timer += delta_time
            if self.combo_timer >= self.combo_timeout:
                self.reset_combo()
                self.animation.change_state(CharacterState.IDLE)
        
        if self.game_object and self.game_object.transform:
            transform = self.game_object.transform

            transform.x += self.velocity_x * delta_time
            transform.y += self.velocity_y * delta_time
            
            GRAVITY = 500
            self.velocity_y -= GRAVITY * delta_time
            
            if transform.y <= 50:
                transform.y = 50
                self.velocity_y = 0
                self.is_on_ground = True
            
            if self.sprite_renderer:
                self.sprite_renderer.sprite.scale_x = abs(self.sprite_renderer.sprite.scale_x)
                if not self.facing_right:
                    self.sprite_renderer.sprite.scale_x *= -1
    
    def move(self, direction: int):
        if self.is_attacking:
            return
            
        self.move_direction = direction
        
        if direction == 0:
            self.velocity_x = 0
            if not self.is_attacking:
                self.animation.change_state(CharacterState.IDLE)
        else:
            self.velocity_x = direction * self.stats.speed
            self.facing_right = direction > 0

            if direction > 0:
                self.animation.change_state(CharacterState.WALK_FORWARD)
            else:
                self.animation.change_state(CharacterState.WALK_BACKWARD)
    
    def jump(self):
        if self.is_on_ground:
            self.velocity_y = 400
            self.is_on_ground = False
    
    def attack(self):
        if self.is_attacking:
            return
            
        self.is_attacking = True
        self.combo_timer = 0
        
        if self.combo_step == 0:
            self.combo_step = 1
            self.attack_damage = self.stats.base_damage
            self.animation.change_state(CharacterState.PUNCH1)
        elif self.combo_step == 1:
            self.combo_step = 2
            self.attack_damage = self.stats.base_damage * 1.2
            self.animation.change_state(CharacterState.PUNCH2)
        elif self.combo_step == 2:
            self.combo_step = 3
            self.attack_damage = self.stats.base_damage * 1.5
            self.animation.change_state(CharacterState.KICK)
        else:
            self.combo_step = 1
            self.attack_damage = self.stats.base_damage
            self.animation.change_state(CharacterState.PUNCH1)
        
        self.velocity_x = 0
    
    def uppercut(self):
        if self.is_attacking:
            return
            
        self.is_attacking = True
        self.reset_combo()
        
        self.attack_damage = self.stats.base_damage * 2.0
        self.animation.change_state(CharacterState.UPPERCUT)
        
        if self.is_on_ground:
            self.velocity_y = 300
            self.is_on_ground = False
        
        self.velocity_x = 0
    
    def reset_combo(self):
        self.combo_step = 0
        self.combo_timer = 0.0
        self.is_attacking = False
        self.velocity_x = self.move_direction * self.stats.speed
    
    def finish_attack(self):
        self.reset_combo()
        if self.move_direction == 0:
            self.animation.change_state(CharacterState.IDLE)
        else:
            self.move(self.move_direction)
    
    def take_damage(self, damage: float):
        actual_damage = damage * self.stats.defense
        self.stats.current_health -= actual_damage
        
        self.stats.rage += actual_damage
        if self.stats.rage > 100:
            self.stats.rage = 100
        
        if self.stats.current_health <= 0:
            self.die()
    
    def die(self):
        print(f"{self.game_object.Name if self.game_object else 'Character'} has been defeated!")
    
    def awaken(self):
        if not self.stats.is_awoken and self.stats.rage >= 100:
            self.stats.is_awoken = True
            self.stats.rage = 0
            self.animation.awaken()
            self.stats.base_damage *= 1.5
            self.stats.speed *= 1.2