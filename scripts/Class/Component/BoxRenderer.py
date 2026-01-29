import arcade
from scripts.Class.GameObject import Component


class BoxRenderer(Component):

    def __init__(self, color, game_object=None):
        super().__init__(game_object)
        self.game_object = game_object
        self.color = color

    def on_draw(self):
        if not self.game_object or not self.game_object.transform:
            return

        t = self.game_object.transform

        arcade.draw_rect_filled(
            arcade.rect.XYRR(t.x, t.y, t.scale.x/2, t.scale.y/2),
            self.color
        )
