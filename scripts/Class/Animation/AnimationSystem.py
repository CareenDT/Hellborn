# scripts/Class/Animation/AnimationSystem.py
import arcade
from enum import Enum
from typing import List, Dict, Optional

class CharacterState(Enum):
    """Animation states for Syorma"""
    IDLE = "idle"
    WALK_FORWARD = "walk_forward"
    WALK_BACKWARD = "walk_backward"
    PUNCH1 = "punch1"
    PUNCH2 = "punch2"
    KICK = "kick"
    UPPERCUT = "uppercut"
    # Awoken versions
    AWOKEN_IDLE = "awoken_idle"
    AWOKEN_WALK_FORWARD = "awoken_walk_forward"
    AWOKEN_WALK_BACKWARD = "awoken_walk_backward"
    AWOKEN_PUNCH1 = "awoken_punch1"
    AWOKEN_PUNCH2 = "awoken_punch2"
    AWOKEN_KICK = "awoken_kick"
    AWOKEN_UPPERCUT = "awoken_uppercut"

class CharacterAnimation:
    """Simple animation controller"""
    def __init__(self):
        self.current_state = CharacterState.IDLE
        self.is_awoken = False
        self.sprite_renderer = None
        
        self.animation_frames: Dict[CharacterState, List[str]] = {}
        
    def set_sprite_renderer(self, sprite_renderer):
        """Set the sprite renderer to update"""
        self.sprite_renderer = sprite_renderer
    
    def add_animation(self, state: CharacterState, frame_paths: List[str]):
        """Add animation frames for a state"""
        self.animation_frames[state] = frame_paths
        
        if state == CharacterState.IDLE and frame_paths:
            if self.sprite_renderer:
                self.sprite_renderer.sprite.texture = arcade.load_texture(frame_paths[0])
    
    def change_state(self, new_state: CharacterState):
        """Change animation state"""
        if self.is_awoken:
            awoken_name = f"AWOKEN_{new_state.name}"
            if hasattr(CharacterState, awoken_name):
                awoken_state = getattr(CharacterState, awoken_name)
                if awoken_state in self.animation_frames:
                    self.current_state = awoken_state
                    self._update_texture()
                    return
            if new_state in self.animation_frames:
                self.current_state = new_state
                self._update_texture()
        else:
            if new_state in self.animation_frames:
                self.current_state = new_state
                self._update_texture()
    
    def _update_texture(self):
        """Update sprite texture to first frame of current animation"""
        if (self.current_state in self.animation_frames and 
            self.sprite_renderer and 
            self.animation_frames[self.current_state]):
            
            frame_paths = self.animation_frames[self.current_state]
            if frame_paths:
                self.sprite_renderer.sprite.texture = arcade.load_texture(frame_paths[0])
    
    def awaken(self):
        """Enter awoken state"""
        self.is_awoken = True
        self.change_state(CharacterState(self.current_state.name.replace("AWOKEN_", "")))