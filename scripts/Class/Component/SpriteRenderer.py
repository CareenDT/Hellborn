from typing import List
import arcade

from scripts.Class.GameObject import Component


class SpriteRendererComponent(Component):
    """Sprite component"""
    
    def __init__(self, image_path, scale=1.0, sprite_list = None, animation: FrameAnimation = None):
        super().__init__()
        self.batch: arcade.SpriteList = sprite_list

        self.sprite: arcade.Sprite = arcade.Sprite(image_path, scale)

        self.Animation: FrameAnimation = animation

        self.add_to_batch(self.batch)
    
    def start(self):
        if self.game_object and self.game_object.transform:
            self.sync_with_transform()

    def set_Animation(self, anim: FrameAnimation):
        self.Animation = anim
        anim.Bind(self)

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
    
    def update(self, delta_time):
        self.sync_with_transform()
        self.sprite.update()

        if self.Animation:
            if self.Animation.IsPlaying:
                self.Animation.on_update(delta_time)
    
    def add_to_batch(self, sprite_list):
        """Add to SpriteList for batch rendering"""
        if self.batch and self.sprite in self.batch:
            self.batch.remove(self.sprite)
        self.batch = sprite_list
        sprite_list.append(self.sprite)

class FrameAnimation:
    def __init__(self, Textures: List[str], FPS:int = 2, PlayOnStart:bool = False, IsLooped:bool = False):
        self.TextureList = [arcade.load_texture(T) for T in Textures]

        self.IsLooped = IsLooped
        self.IsPlaying = PlayOnStart

        self.FPS = FPS
        self.Sprite: SpriteRendererComponent = None

        self._elapsed = 0

        self._index = 0

    def Bind(self, To: SpriteRendererComponent):
        self.Sprite = To

    def _next(self):
        if self.Sprite:
            self.Sprite.sprite.texture = self.TextureList[(int)(self._index)]

    def on_update(self, delta_time):
        if self.Sprite:
            self._elapsed += delta_time
            if self._elapsed >= 1 / self.FPS:
                self._index = (self._index + (self._elapsed / (1 / self.FPS))) % len(self.TextureList)
                self._next()
                self._elapsed %= 1 / self.FPS