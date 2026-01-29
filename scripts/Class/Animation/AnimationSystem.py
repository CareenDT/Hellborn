import arcade
from enum import Enum
from typing import Dict, List

class CharacterState(Enum):
    IDLE = "idle"
    WALK_FORWARD = "walk_forward"
    WALK_BACKWARD = "walk_backward"
    PUNCH1 = "punch1"
    PUNCH2 = "punch2"
    KICK = "kick"
    UPPERCUT = "uppercut"
    JUMP = "jump"

class CharacterAnimation:
    def __init__(self):
        self.current_state = CharacterState.IDLE
        self.current_texture = None
        self.textures: Dict[CharacterState, List[arcade.Texture]] = {}
        self.frame_durations: Dict[CharacterState, List[float]] = {}
        self.frame_index = 0
        self.animation_timer = 0
        self.default_frame_duration = 0.25
        self.is_complete = False

    def add_animation(self, state: CharacterState, texture_paths: List[str], durations: List[float] = None):
        textures = [arcade.load_texture(path) for path in texture_paths]
        self.textures[state] = textures
        if durations is None:
            durations = [self.default_frame_duration] * len(textures)
        self.frame_durations[state] = durations
        if state == CharacterState.IDLE and self.current_texture is None:
            self.current_texture = textures[0]

    def change_state(self, new_state: CharacterState):
        if new_state in self.textures:
            self.current_state = new_state
            self.frame_index = 0
            self.animation_timer = 0
            self.is_complete = False
            self.current_texture = self.textures[new_state][0]
            return True
        return False

    def update(self, delta_time: float):
        if self.current_state in self.textures and not self.is_complete:
            textures = self.textures[self.current_state]
            durations = self.frame_durations[self.current_state]
            if len(textures) > 1:
                self.animation_timer += delta_time
                current_duration = durations[self.frame_index] if self.frame_index < len(durations) else self.default_frame_duration
                if self.animation_timer >= current_duration:
                    self.animation_timer = 0
                    next_index = self.frame_index + 1
                    if next_index >= len(textures):
                        if self.current_state in [CharacterState.PUNCH1, CharacterState.PUNCH2, CharacterState.KICK, CharacterState.UPPERCUT]:
                            self.is_complete = True
                            return
                        else:
                            self.frame_index = 0
                    else:
                        self.frame_index = next_index
                    self.current_texture = textures[self.frame_index]

    def get_current_texture(self):
        return self.current_texture
