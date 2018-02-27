
#agents are collections of components
class Agent_Base():
    def __init__(self, components = {}):
        self.components = components

    def add_component(self, component):
        self.components[component.name] = component

    def get_component(self, id):
        if id in self.components:
            return self.components[id]
        else:
            print(id, ' is not in ', self)