import arcade
from scripts.Class.GameObject import Component


class BoxRenderer(Component):
    """Box drawing"""

    def __init__(self, color, game_object = None):
        self.game_object = game_object
        self.color = color

    def on_draw(self):
        if not self.game_object or not self.game_object.transform:
            return
            
        t = self.game_object.transform

        x = t.position.x
        y = t.position.y
        width = t.scale.x
        height = t.scale.y

        arcade.draw_rect_filled(
            arcade.rect.XYWH(x, y, width, height),
            self.color
        )