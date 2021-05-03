import sgengine
import pygame
import random
from sgengine import Data2D
import math


def move_entity(entity: sgengine.lifecycle.Entity, how_much: Data2D, delta_time, precision=5):
    if issubclass(type(entity), Collider):
        fract = delta_time / precision
        last_pos = Data2D(entity.position.x, entity.position.y)
        virtual_position = Data2D(entity.position.x, entity.position.y)
        virtual_collider = Collider()
        virtual_collider.set_collider_tag(entity.get_collider_tag())
        virtual_collider.set_collider_position(virtual_position)
        virtual_collider.set_collider_size(entity.get_collider_size())
        virtual_collider.set_collider_pivot(entity.get_collider_pivot())

        #print(last_pos)
        is_valid = True
        for i in range(1, precision + 1):
            #print(i)
            virtual_position.x += round(how_much.x * fract, 1)
            virtual_position.y += round(how_much.y * fract, 1)
            for c in sgengine.current_scene.colliders_list():
                if virtual_collider.is_colliding(c):
                    is_valid = False
        
        if is_valid:
            entity.position.x = virtual_position.x
            entity.position.y = virtual_position.y
    else:
        entity.position.x += how_much.x * delta_time
        entity.position.y += how_much.y * delta_time
    #print(entity.position)

class Collider:
    def set_collider_tag(self, tag):
        self.tag = tag

    def get_collider_tag(self):
        if not hasattr(self, "tag"):
            self.tag = random.random() * 100000
        
        return self.tag
    
    def set_collider_position(self, collider_position):
        self.collider_position = collider_position
    
    def get_collider_position(self):
        if not hasattr(self, "collider_position"):
            self.collider_position = Data2D(0, 0)
        return self.collider_position
    
    def set_collider_pivot(self, collider_pivot):
        self.collider_pivot = collider_pivot
    
    def get_collider_pivot(self):
        if not hasattr(self, "collider_pivot"):
            self.collider_pivot = Data2D(0, 0)
        return self.collider_pivot
    
    def set_collider_size(self, collider_size):
        self.collider_size = collider_size
    
    def get_collider_size(self):
        if not hasattr(self, "collider_size"):
            self.collider_size = Data2D(0, 0)
        return self.collider_size
    
    def is_colliding(self, other):
        rect1 = pygame.Rect((self.get_collider_position().x - self.get_collider_pivot().x, self.get_collider_position().y - self.get_collider_pivot().y), (self.get_collider_size().x, self.get_collider_size().y))
        rect2 = pygame.Rect((other.get_collider_position().x - other.get_collider_pivot().x, other.get_collider_position().y - other.get_collider_pivot().y), (other.get_collider_size().x, other.get_collider_size().y))
        
        if self.get_collider_tag() == other.get_collider_tag():
            return False
        
        return rect1.colliderect(rect2)
    
    def is_point_colliding(self, point):
        rect1 = pygame.Rect((self.get_collider_position().x - self.get_collider_pivot().x, self.get_collider_position().y - self.get_collider_pivot().y), (self.get_collider_size().x, self.get_collider_size().y))
        return rect1.collidepoint((point.x, point.y))
     