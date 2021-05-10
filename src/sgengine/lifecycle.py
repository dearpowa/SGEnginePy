import sgengine as sg
from sgengine import Data2D

class Scene:
    def __init__(self, tag):
        self.entity_list = []
        self.tag = tag
        
    def camera_list(self):
        camera_list = []
        for e in self.entity_list:
            if issubclass(type(e), sg.screen.Camera):
                camera_list.append(e)
        return camera_list
    
    def colliders_list(self):
        colliders_list = []
        for e in self.entity_list:
            if issubclass(type(e), sg.physics.Collider):
                colliders_list.append(e)
        return colliders_list

    def colliders2_list(self):
        colliders_list = []
        for e in self.entity_list:
            if issubclass(type(e), sg.physics.Collider2):
                colliders_list.append(e)
        return colliders_list
    
    def add_entities(self, *entities, start=False):
        for entity in entities:
            if issubclass(type(entity), Entity):
                self.entity_list.append(entity)
                if start:
                    entity.start()
        
class Entity:
    def __init__(self):
        self.position = Data2D(0,0)
        self.drawing_order = 0
        if sg.log_active:
            print("Entity created")
        
    def start(self):
        pass
        
    def update(self, events):
        pass
    
    #Accade 60 volte per frame (ipoteticamente)
    def fixed_update(self, delta_time):
        pass
    
    def current_scene(self):
        return sg.current_scene