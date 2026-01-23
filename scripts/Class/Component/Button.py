from typing import Any
import arcade
from scripts.Class.GameObject import Component, GameObject, Transform
from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent

class ButtonComponent(Component):
    def __init__(self, View, gameObject: GameObject, Text: str = "", normal_texture: arcade.Texture = None, hover_texture: arcade.Texture = None, on_click: Any = None):
        self.x = gameObject.transform.position.x
        self.y = gameObject.transform.position.y
        self.width = gameObject.transform.scale.x
        self.height = gameObject.transform.scale.y
        self.text = Text
        self.normal_texture = normal_texture
        self.hover_texture = hover_texture
        self.current_texture = normal_texture
        self.is_hovered = False
        self.is_pressed = False
        
        self.game_object = gameObject

        self.on_click = on_click

        self.SpriteComp = self.game_object.get_component(SpriteRendererComponent)

        if not self.SpriteComp:
            self.SpriteComp = self.game_object.add_component(SpriteRendererComponent)


    def sync_with_transform(self):
        """Update sprite to match GameObject's transform"""
        if self.game_object and self.game_object.transform:
            t = self.game_object.transform
            
            # Update
            self.x = t.position.x
            self.y = t.position.y
            self.width = t.rotation

            self.sprite.scale_x = t.scale.x / self.sprite.texture.width
            self.sprite.scale_y = t.scale.y / self.sprite.texture.height

    def on_mouse_press(self, x, y, button, modifiers):
        """Check if any button was clicked"""
        if button == arcade.MOUSE_BUTTON_LEFT:
            for btn in self.buttons:
                if btn.is_clicked(x, y):
                    btn.click()
    
    def on_mouse_motion(self, x, y, dx, dy):
        """Optional: Add hover effect"""
        for btn in self.buttons:
            if btn.is_clicked(x, y):
                btn.color = btn.hover_color
            else:
                btn.color = arcade.color.BLUE

    def check_mouse_hover(self, mouse_x, mouse_y):
        """Check if mouse is hovering over the button"""
        left = self.x - self.width // 2
        right = self.x + self.width // 2
        top = self.y + self.height // 2
        bottom = self.y - self.height // 2
        
        if left <= mouse_x <= right and bottom <= mouse_y <= top:
            self.is_hovered = True
            self.current_texture = self.hover_texture
            return True
        else:
            self.is_hovered = False
            self.current_texture = self.normal_texture
            return False
    
    def check_click(self, mouse_x, mouse_y, mouse_button):
        """Check if button was clicked"""
        if self.check_mouse_hover(mouse_x, mouse_y) and mouse_button == arcade.MOUSE_BUTTON_LEFT:
            if self.on_click:
                self.on_click()
                return True
        return False