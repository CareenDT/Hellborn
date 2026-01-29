import arcade
from scripts.Class.GameObject import Component, GameObject

class ScreenRelativeTransform(Component):
    def __init__(self, Subject: arcade.Window | GameObject | arcade.View, x = 0, y = 0, scale_x: float = 1, scale_y: float = 1, game_object = None):
        super().__init__(game_object)

        self.RelativePosX = x
        self.RelativePosY = y

        self.RelativeTo = Subject

        self.RelativeScaleX = scale_x
        self.RelativeScaleY = scale_y

    def update(self, delta_time):
        if (type(self.RelativeTo) == GameObject):
            self.game_object.transform.position = arcade.Vec2(self.RelativePosX * self.RelativeTo.transform.scale.x + self.RelativeTo.transform.position.x, self.RelativePosY * self.RelativeTo.transform.scale.y + self.RelativeTo.transform.position.y)
            self.game_object.transform.scale = arcade.Vec2(self.RelativeScaleX * self.RelativeTo.transform.scale.x, self.RelativeScaleY * self.RelativeTo.transform.scale.y)
        else:
            self.game_object.transform.position = arcade.Vec2(self.RelativePosX * self.RelativeTo.width,self.RelativePosY * self.RelativeTo.height)
            self.game_object.transform.scale = arcade.Vec2(self.RelativeScaleX * self.RelativeTo.width, self.RelativeScaleY * self.RelativeTo.height)
