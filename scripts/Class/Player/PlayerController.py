import arcade
from typing import Set

class PlayerController:
    def __init__(self, character_component, key_bindings: dict = None):
        self.character = character_component
        self.keys_pressed: Set[int] = set()
        self.key_bindings = key_bindings or {
            'left': arcade.key.A,
            'right': arcade.key.D,
            'jump': arcade.key.W,
            'attack': arcade.key.J,
            'uppercut': arcade.key.K,
            'awaken': arcade.key.L
        }
    
    def on_key_press(self, key: int):
        self.keys_pressed.add(key)
        self._process_input()
    
    def on_key_release(self, key: int):
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        self._process_input()
    
    def _process_input(self):
        if not self.character:
            return
        moving_left = self.key_bindings['left'] in self.keys_pressed
        moving_right = self.key_bindings['right'] in self.keys_pressed
        if moving_left and not moving_right:
            self.character.move(-1)
        elif moving_right and not moving_left:
            self.character.move(1)
        else:
            self.character.move(0)
        if self.key_bindings['jump'] in self.keys_pressed:
            self.character.jump()
            self.keys_pressed.discard(self.key_bindings['jump'])
        if self.key_bindings['attack'] in self.keys_pressed:
            self.character.attack()
            self.keys_pressed.discard(self.key_bindings['attack'])
        if self.key_bindings['uppercut'] in self.keys_pressed:
            self.character.uppercut()
            self.keys_pressed.discard(self.key_bindings['uppercut'])
        if self.key_bindings['awaken'] in self.keys_pressed:
            self.character.awaken()
            self.keys_pressed.discard(self.key_bindings['awaken'])
    
    def update(self, delta_time: float):
        self._process_input()