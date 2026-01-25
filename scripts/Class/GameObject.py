import arcade
from typing import List, Type, Dict, Optional, Any

class Component:
    """Base class for all components"""
    def __init__(self, game_object: 'GameObject' = None, ):
        self.game_object = game_object
        
    def start(self):
        """[ABSTRACT] called when the component is added /// Setup function"""
        pass
    
    def update(self, delta_time: float):
        """[ABSTRACT] called on gameobject update"""
        pass
    
    def on_draw(self):
        """[ABSTRACT] called on gameobject draw"""
        pass
    
    def destroy(self):
        """[ABSTRACT] called when the component is destroyed /// Cleanup function"""
        pass

class GameObject():
    def __init__(self, Name, transform: Transform = None, ):

        self.Name = Name
        self.transform = transform

        self.components: Dict[Type[Component], List[Component]] = {}

    # Components
    def add_component(self, component: Component) -> Component:

        """Add a component to this GameObject"""

        component.game_object = self
        comp_type = type(component)
        if comp_type not in self.components: # Null safety
            self.components[comp_type] = []
        
        self.components[comp_type].append(component)

        component.start()

        return component
    
    def get_component(self, component_type: Type[Component]) -> Optional[Component]:

        """Get the first component of specified type"""

        if component_type in self.components and self.components[component_type]:
            return self.components[component_type][0]

        return None
    
    def get_components(self, component_type: Type[Component]) -> List[Component]:

        """Get all components of specified type"""

        return self.components.get(component_type, [])
    
    def remove_component(self, component: Component):
        """Remove a specific component"""

        comp_type = type(component)

        if comp_type in self.components and component in self.components[comp_type]:
            component.destroy()
            self.components[comp_type].remove(component)
            
            if not self.components[comp_type]: # Clean up
                del self.components[comp_type]
    
    def remove_all_components(self):

        """Remove all components from this GameObject"""

        for comp_list in self.components.values():
            for component in comp_list:
                component.destroy()
        self.components.clear()
    
    def has_component(self, component_type: Type[Component]) -> bool:

        """Check if GameObject has at least one component of specified type"""

        return component_type in self.components
    
    def get_all_components(self) -> List[Component]:

        """Get list of all components"""

        all_components = []

        for comp_list in self.components.values():
            all_components.extend(comp_list)
        return all_components
    
    # General
    
    def update(self, delta_time):

        """Update all components"""

        for comp_list in self.components.values():
            for component in comp_list:
                component.update(delta_time)
    
    def draw(self):

        """Draw the GameObject and its components"""
        # Call on_draw for all components
        for comp_list in self.components.values():
            for component in comp_list:
                component.on_draw()

    def __repr__(self):
        return f"Name: {self.Name}; Gameobject(Position: {self.center_x, self.center_y};)"

class Transform:
    """Transform component"""
    def __init__(self, x: float = 0.0, y: float = 0.0, 
                 rotation: float = 0.0, scale: float = 1.0):
        
        self.position = arcade.Vec2(x, y)
        self.rotation = rotation
        self.scale = arcade.Vec2(scale, scale)
    def __init__(self, x: float = 0.0, y: float = 0.0, 
                 rotation: float = 0.0, scale: arcade.Vec2 = arcade.Vec2(0,0)):
        
        self.position = arcade.Vec2(x, y)
        self.rotation = rotation
        self.scale = scale