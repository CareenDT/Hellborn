# scripts/Class/Player/PlayerController.py
import arcade
from typing import Set

class PlayerController:
    """Handles input for a player, separate from character logic"""
    def __init__(self, character_component, key_bindings: dict = None):
        self.character = character_component
        self.keys_pressed: Set[int] = set()
        
        # Default key bindings (Player 1)
        self.key_bindings = key_bindings or {
            'left': arcade.key.A,
            'right': arcade.key.D,
            'jump': arcade.key.W,
            'attack': arcade.key.J,
            'uppercut': arcade.key.K,
            'awaken': arcade.key.L
        }
    
    def on_key_press(self, key: int):
        """Called when a key is pressed"""
        self.keys_pressed.add(key)
        self._process_input()
    
    def on_key_release(self, key: int):
        """Called when a key is released"""
        if key in self.keys_pressed:
            self.keys_pressed.remove(key)
        self._process_input()
    
    def _process_input(self):
        """Process all current key states"""
        if not self.character:
            return
            
        # Movement
        moving_left = self.key_bindings['left'] in self.keys_pressed
        moving_right = self.key_bindings['right'] in self.keys_pressed
        
        if moving_left and not moving_right:
            self.character.move(-1)
        elif moving_right and not moving_left:
            self.character.move(1)
        else:
            self.character.move(0)
        
        # Jump
        if self.key_bindings['jump'] in self.keys_pressed:
            self.character.jump()
            # Remove jump key to prevent continuous jumping
            self.keys_pressed.discard(self.key_bindings['jump'])
        
        # Attacks
        if self.key_bindings['attack'] in self.keys_pressed:
            self.character.attack()
            # Remove attack key to prevent spam
            self.keys_pressed.discard(self.key_bindings['attack'])
        
        if self.key_bindings['uppercut'] in self.keys_pressed:
            self.character.uppercut()
            self.keys_pressed.discard(self.key_bindings['uppercut'])
        
        # Awaken
        if self.key_bindings['awaken'] in self.keys_pressed:
            self.character.awaken()
            self.keys_pressed.discard(self.key_bindings['awaken'])
    
    def update(self, delta_time: float):
        """Update input processing"""
        self._process_input()