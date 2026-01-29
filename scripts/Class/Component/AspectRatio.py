import arcade
from scripts.Class.GameObject import Component, GameObject


class AspectRatioComponent(Component):
    def __init__(self, Ratio:float = 1, RelativeToX:bool = True, game_object: GameObject = None):
        super().__init__(game_object)
        self.RelativeToX = RelativeToX
        self.ratio = Ratio
    
    def start(self):
        # Calculate ratio from texture if not set
        if self.ratio == 1:
            from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
            sprite_comp = self.game_object.get_component(SpriteRendererComponent)
            if sprite_comp and sprite_comp.texture:
                self.ratio = sprite_comp.texture.height / sprite_comp.texture.width
    
    def update(self, delta_time):
        if self.RelativeToX:
            self.game_object.transform.scale = arcade.Vec2(self.game_object.transform.scale.x, self.game_object.transform.scale.x * self.ratio)
        else:
            self.game_object.transform.scale = arcade.Vec2(self.game_object.transform.scale.y * self.ratio, self.game_object.transform.scale.y)
