import arcade
from scripts.Class.GameObject import Component

class HitboxType:
    ATTACK = "attack"
    HURT = "hurt"

class HitboxComponent(Component):
    def __init__(self, hitbox_type: str, damage: float = 0, width: float = 50, height: float = 50, offset_x: float = 0, offset_y: float = 0, sprite_list=None, game_object=None, knockback_force: float = 0, hitstun_duration: float = 0.5):
        super().__init__(game_object)
        self.hitbox_type = hitbox_type
        self.damage = damage
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.active = False
        self.timer = 0
        self.sprite = arcade.Sprite("assets/HITBOX.png")
        if sprite_list is not None:
            sprite_list.append(self.sprite)
        self.sprite.width = self.width
        self.sprite.height = self.height
        self.knockback_force = knockback_force
        self.hitstun_duration = hitstun_duration
        if self.hitbox_type == HitboxType.ATTACK:
            self.sprite.color = arcade.color.RED
        elif self.hitbox_type == HitboxType.HURT:
            self.sprite.color = arcade.color.BLUE

    def activate(self, duration: float):
        self.active = True
        self.timer = duration

    def update(self, delta_time):
        if self.active and self.hitbox_type != HitboxType.HURT:
            self.timer -= delta_time
            if self.timer <= 0:
                self.active = False

        if self.game_object:
            from scripts.Class.Character.CharacterComponent import CharacterComponent
            char_comp = self.game_object.get_component(CharacterComponent)
            facing_right = char_comp.facing_right if char_comp else True
            x_offset = self.offset_x if facing_right else -self.offset_x
            self.sprite.center_x = self.game_object.transform.position.x + x_offset
            self.sprite.center_y = self.game_object.transform.position.y + self.offset_y

    def check_collision(self, other_hitbox):
        if not self.active or not other_hitbox.active:
            return False
        if self.hitbox_type == other_hitbox.hitbox_type:
            return False
        return arcade.check_for_collision(self.sprite, other_hitbox.sprite)

    def on_draw(self):
        pass
