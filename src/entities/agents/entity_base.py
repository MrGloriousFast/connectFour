
#agents are collections of components
class Agent_Base():
    def __init__(self, components = {}):
        self.components = components

    def add_component(self, component):
        self.components[component.name] = component