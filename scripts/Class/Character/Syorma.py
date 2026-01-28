# scripts/Class/Character/Syorma.py
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Character.CharacterComponent import CharacterComponent, CharacterStats
import arcade
import os

class Syorma(GameObject):
    """Syorma - The Cursed Knight character"""
    def __init__(self, name: str = "Syorma", transform: Transform = Transform(100, 100)):
        super().__init__(name, transform)
        
        try:
            from scripts.Class.Component.SpriteRenderer import SpriteRendererComponent
            default_image = "assets/characters/syorma/idle_1.png"
            if not os.path.exists(default_image):
                default_image = "assets/Preview.png"
                print(f"Warning: {default_image} not found, using placeholder")
            
            sprite_renderer = SpriteRendererComponent(
                image_path=default_image,
                scale=2.0
            )
            self.add_component(sprite_renderer)
            
        except ImportError:
            print("Warning: SpriteRendererComponent not available")
        
        stats = CharacterStats(
            max_health=120,
            base_damage=12,
            speed=180,
            defense=0.8
        )
        
        character = SyormaCharacterComponent(stats=stats)
        self.add_component(character)

class SyormaCharacterComponent(CharacterComponent):
    def _setup_animations(self):
        assets_dir = "assets/characters/syorma"
        if not os.path.exists(assets_dir):
            print(f"Warning: Assets directory not found: {assets_dir}")
            placeholder = "assets/Preview.png"
            from scripts.Class.Animation.AnimationSystem import CharacterState
            
            for state in CharacterState:
                self.animation.add_animation(state, [placeholder])
            return
        
        from scripts.Class.Animation.AnimationSystem import CharacterState
        
        animations = {
            CharacterState.IDLE: ["idle_1.png", "idle_2.png", "idle_3.png"],
            CharacterState.WALK_FORWARD: ["walk_1.png", "walk_2.png", "walk_3.png"],
            CharacterState.WALK_BACKWARD: ["walk_back_1.png", "walk_back_2.png"],
            CharacterState.PUNCH1: ["punch1_1.png", "punch1_2.png"],
            CharacterState.PUNCH2: ["punch2_1.png", "punch2_2.png"],
            CharacterState.KICK: ["kick_1.png", "kick_2.png", "kick_3.png"],
            CharacterState.UPPERCUT: ["uppercut_1.png", "uppercut_2.png", "uppercut_3.png"],
            CharacterState.AWOKEN_IDLE: ["awoken_idle_1.png", "awoken_idle_2.png"],
            CharacterState.AWOKEN_WALK_FORWARD: ["walk_1.png"],
            CharacterState.AWOKEN_WALK_BACKWARD: ["walk_back_1.png"],
            CharacterState.AWOKEN_PUNCH1: ["punch1_1.png"],
            CharacterState.AWOKEN_PUNCH2: ["punch2_1.png"],
            CharacterState.AWOKEN_KICK: ["kick_1.png"],
            CharacterState.AWOKEN_UPPERCUT: ["uppercut_1.png"]
        }
        
        for state, filenames in animations.items():
            frame_paths = []
            for filename in filenames:
                full_path = f"{assets_dir}/{filename}"
                if os.path.exists(full_path):
                    frame_paths.append(full_path)
                else:
                    print(f"Warning: Missing frame {filename} for {state}")
                    frame_paths.append("assets/Preview.png")
            
            if frame_paths:
                self.animation.add_animation(state, frame_paths)