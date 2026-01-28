from typing import List
import arcade
import os
from scripts.Class.GameObject import Component

class SpriteRendererComponent(Component):
    def __init__(self, image_path, scale=1.0, sprite_list=None):
        super().__init__()

        if os.path.exists(image_path):
            self.texture = arcade.load_texture(image_path)
        else:
            self.texture = arcade.load_texture("assets/Preview.png")

        self.sprite = arcade.Sprite()
        self.sprite.texture = self.texture
        self.sprite.scale = scale
        self.sprite.center_x = 0
        self.sprite.center_y = 0

        self.scale = scale
        self.custom_width = None
        self.custom_height = None
        self.batch = sprite_list
        if self.batch is not None:
            self.batch.append(self.sprite)

    def sync_with_transform(self):
        if self.game_object and self.game_object.transform:
            t = self.game_object.transform
            if self.sprite:
                self.sprite.center_x = t.x
                self.sprite.center_y = t.y
                if self.custom_width is None and self.custom_height is None:
                    self.sprite.scale = self.scale * t.scale_x

    def start(self):
        self.sync_with_transform()

    def update(self, delta_time):
        self.sync_with_transform()

    def set_texture(self, texture):
        if self.sprite:
            self.sprite.texture = texture

    def set_custom_size(self, width, height):
        self.custom_width = width
        self.custom_height = height
        if self.sprite:
            self.sprite.width = width
            self.sprite.height = height

    def on_draw(self):
        pass
