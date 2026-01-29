from typing import Any
import arcade
from scripts.Class.GameObject import Component, GameObject, Transform
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent


class ButtonComponent(Component):
    def __init__(self, view, gameObject: GameObject, Text: str = "", normal_texture_path: str = None,
                 hover_texture_path: str = None, on_click: Any = None):
        super().__init__(gameObject)

        self.text = Text
        self.normal_texture = arcade.load_texture(normal_texture_path) if normal_texture_path else None
        self.hover_texture = arcade.load_texture(hover_texture_path) if hover_texture_path else None
        self.is_hovered = False
        self.on_click = on_click

        self.SpriteComp: SpriteRendererComponent = self.game_object.get_component(SpriteRendererComponent)

        if self.SpriteComp and self.normal_texture:
            self.SpriteComp.sprite.texture = self.normal_texture

    def check_mouse_hover(self, mouse_x, mouse_y):
        if not self.SpriteComp or not self.SpriteComp.sprite:
            return False

        sprite = self.SpriteComp.sprite
        left = sprite.left
        right = sprite.right
        bottom = sprite.bottom
        top = sprite.top

        if left <= mouse_x <= right and bottom <= mouse_y <= top:
            self.is_hovered = True
            if self.hover_texture:
                self.SpriteComp.sprite.texture = self.hover_texture
            return True
        else:
            self.is_hovered = False
            if self.normal_texture:
                self.SpriteComp.sprite.texture = self.normal_texture
            return False

    def check_click(self, mouse_x, mouse_y, mouse_button):
        if self.check_mouse_hover(mouse_x, mouse_y) and mouse_button == arcade.MOUSE_BUTTON_LEFT:
            if self.on_click:
                self.on_click()
            return True
        return False
