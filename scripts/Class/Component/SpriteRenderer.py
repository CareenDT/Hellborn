from typing import List
import arcade

from scripts.Class.GameObject import Component

class SpriteRendererComponent(Component):
    """Sprite component"""
    
    def __init__(self, image_path, scale=1.0, sprite_list = None):
        super().__init__()
        self.batch: arcade.SpriteList = sprite_list

        self.sprite: arcade.Sprite = arcade.Sprite(image_path, scale)

        if (self.batch):
            self.add_to_batch(self.batch)


    def sync_with_transform(self):
        """Update sprite to match GameObject's transform"""
        if self.game_object and self.game_object.transform:
            t = self.game_object.transform
            
            # Update
            self.sprite.center_x = t.position.x
            self.sprite.center_y = t.position.y
            self.sprite.angle = t.rotation

            self.sprite.scale_x = t.scale.x / self.sprite.texture.width
            self.sprite.scale_y = t.scale.y / self.sprite.texture.height

    def start(self):
        if self.game_object and self.game_object.transform:
            self.sync_with_transform()
    
    def update(self, delta_time):
        self.sync_with_transform()
        self.sprite.update()
    
    def add_to_batch(self, sprite_list: arcade.SpriteList):
        """Add to SpriteList for batch rendering"""
        self.batch = sprite_list
        sprite_list.append(self.sprite)
