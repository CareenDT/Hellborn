import arcade
from scripts.Class.GameObject import Component, GameObject


class AspectRatioComponent(Component):
    def __init__(self, Ratio:float = 1, RelativeToX:bool = True, game_object: GameObject = None):
        self.game_object = game_object
        self.RelativeToX = RelativeToX
        self.ratio = Ratio
    
    def update(self, delta_time):
        if self.RelativeToX:
            self.game_object.transform.scale = arcade.Vec2(self.game_object.transform.scale.x, self.game_object.transform.scale.x * self.ratio)
        else:
            self.game_object.transform.scale = arcade.Vec2(self.game_object.transform.scale.y * self.ratio, self.game_object.transform.scale.y)