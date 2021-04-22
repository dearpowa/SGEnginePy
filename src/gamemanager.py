from sgengine import Entity, Data2D
from simpletree import Tree
import sgengine
import pygame

class GameManager(Entity):
    def start(self):
        self.tree_list = []
        
        tree1 = Tree()
        tree2 = Tree()
        tree3 = Tree()
        tree4 = Tree()
        tree5 = Tree()
        
        tree1.position = Data2D(33, 33)
        tree2.position = Data2D(33, 10)
        tree3.position = Data2D(22, 10)
        tree4.position = Data2D(15, 33)
        tree5.position = Data2D(50, 80)
        
        self.current_scene().add_entity(tree1)
        self.current_scene().add_entity(tree2)
        self.current_scene().add_entity(tree3)
        self.current_scene().add_entity(tree4)
        self.current_scene().add_entity(tree5)
        
        for camera in self.current_scene().camera_list():
            if camera.tag == sgengine.DEFAULT_CAMERA:
                camera.size = Data2D(80, 60)
        
        sgengine.framerate = 60
        sgengine.target_framerate = 45
        sgengine.log_active = True
        sgengine.change_resolution((800, 600))
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                sgengine.toggle_fullscreen()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                sgengine.running = False