from sgengine import Data2D
from sgengine.lifecycle import Entity
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
        
        self.current_scene().add_entities(tree1, tree2, tree3, tree4, tree5)
        
        for camera in self.current_scene().camera_list():
            if camera.tag == sgengine.DEFAULT_CAMERA:
                camera.size = Data2D(160, 120)
                camera.debug_sprite_pivot = True
                camera.debug_collider = False
                camera.debug_collider_pivot = True
        
        sgengine.framerate = 30
        sgengine.target_framerate = 30
        sgengine.log_active = True
        sgengine.physics.physics_space.gravity = 0, 1000
        sgengine.change_resolution((800, 600))
        
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYUP and event.key == pygame.K_RETURN:
                sgengine.toggle_fullscreen()
            if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
                sgengine.running = False