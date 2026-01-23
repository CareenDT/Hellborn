import arcade
from pyglet.graphics import Batch
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class MenuObject(arcade.View):
    def __init__(self, window):
        super().__init__()

        self.Batch = Batch()

        self.window = window

        self.game_objects: list[GameObject] = []

        self.Btn = GameObject("Butnni", Transform(50,50,0, arcade.Vec2(200,200)))
        self.Btn.add_component(ButtonComponent(self, self.Btn, "Play" ,on_click = self.onBtn_Play, normal_texture=arcade.load_texture("assets/TheSun.png")))

        self.Btn.add_component(SpriteRendererComponent("assets/TheSun.png", 1, window.Object_Batch))
        self.game_objects.append(self.Btn)

    def on_draw(self):
        self.clear()

        for obj in self.game_objects:
            obj.draw()

        self.Batch.draw()
    
    def onBtn_Play(self):
        print("Pressed")

    def on_update(self, delta_time):
        for obj in self.game_objects:
            obj.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        # Check all game objects for button components
        for obj in self.game_objects:
            # Get ButtonComponent if exists
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_click(x, y, button)
    
    def on_mouse_motion(self, x, y, dx, dy):
        # Update hover state
        for obj in self.game_objects:
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_mouse_hover(x, y)