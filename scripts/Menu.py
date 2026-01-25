import arcade
from pyglet.graphics import Batch
from scripts.Class.GameObject import GameObject, Transform
from scripts.Class.Components import *

class MenuObject(arcade.View):
    def __init__(self, window):
        super().__init__()

        self.Batch = Batch()

        self.window = window

        self.Object_Batch = arcade.SpriteList()

        self.game_objects: list[GameObject] = []

        self.obj_Side = GameObject("Menu_Sidebar", Transform())
        self.obj_Side.add_component(ScreenRelativeTransform(self,0.5, 0.5, 0.35, 1))

        self.obj_Side.add_component(BoxRenderer((0, 0, 0, 255), self.obj_Side))
        self.game_objects.append(self.obj_Side)

        self.Btn = GameObject("Butnni", Transform())

        self.Btn.add_component(ScreenRelativeTransform(self.obj_Side,0, 0, 1, .25))

        self.Btn.add_component(ButtonComponent(self, self.Btn, "Play" ,on_click = self.onBtn_Play, normal_texture=arcade.load_texture("assets/TheSun.png")))

        self.Btn.add_component(SpriteRendererComponent("assets/TheSun.png", 1, window.Object_Batch))
        self.game_objects.append(self.Btn)

    def on_draw(self):
        self.clear()

        for obj in self.game_objects:
            obj.draw()

        self.Object_Batch.draw(pixelated=True)

        self.Batch.draw()
    
    def onBtn_Play(self):
        print("Pressed")

    def on_update(self, delta_time):
        for obj in self.game_objects:
            obj.update(delta_time)

    def on_mouse_press(self, x, y, button, modifiers):
        for obj in self.game_objects:
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_click(x, y, button)
    
    def on_mouse_motion(self, x, y, dx, dy):
        for obj in self.game_objects:
            btn_comp = obj.get_component(ButtonComponent)
            if btn_comp:
                btn_comp.check_mouse_hover(x, y)