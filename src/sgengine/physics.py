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
        virtual_collider.collider_tag = entity.collider_tag
        virtual_collider.collider_position = virtual_position
        virtual_collider.collider_size = entity.collider_size
        virtual_collider.collider_pivot_perc = entity.collider_pivot_perc

        #print(last_pos)
        is_valid = True
        for i in range(1, precision + 1):
            #print(i)
            virtual_position.x += round(how_much.x * fract, 1)
            virtual_position.y += round(how_much.y * fract, 1)
            for c in sgengine.current_scene.colliders_list():
                if virtual_collider.is_colliding(c):
                    is_valid = False
                    continue
            if not is_valid:
                continue
        
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
        if not hasattr(self, "_collider_tag"):
            self._collider_tag = random.random() * 100000
        
        return self._collider_tag

    @property
    def collider_position(self):
        if not hasattr(self, "_collider_position"):
            self._collider_position = Data2D(0, 0)
        return self._collider_position

    @collider_position.setter
    def collider_position(self, collider_position):
        self._collider_position = collider_position
    
    @property
    def collider_pivot(self):
        if not hasattr(self, "_collider_pivot"):
            self._collider_pivot = Data2D(0, 0)
        return self._collider_pivot

    @collider_pivot.setter
    def collider_pivot(self, collider_pivot):
        self._collider_pivot = collider_pivot

    @property
    def collider_pivot_perc(self):
        if self.collider_pivot != None and self.collider_size != None and self.collider_size.x != 0 and self.collider_size.y != 0:
            return Data2D(self.collider_pivot.x / self.collider_size.x, self.collider_pivot.y / self.collider_size.y)
        return None

    @collider_pivot_perc.setter
    def collider_pivot_perc(self, collider_pivot_perc):
        if collider_pivot_perc != None and self.collider_size != None and self.collider_size.x != 0 and self.collider_size.y != 0:
            self.collider_pivot = Data2D(collider_pivot_perc.x * self.collider_size.x, collider_pivot_perc.y * self.collider_size.y)
    
    @property
    def collider_size(self):
        if not hasattr(self, "_collider_size"):
            self._collider_size = Data2D(0, 0)
        return self._collider_size

    @collider_size.setter
    def collider_size(self, collider_size):
        current_pivot_perc = self.collider_pivot_perc
        self._collider_size = collider_size
        #Aggiunto per gestire il cambio di grandezze del collider
        #in modo da mantenere lo stesso pivot in percentuale alla grandezza
        self.collider_pivot_perc = current_pivot_perc

    def get_rect(self):
        return pygame.Rect(self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y, self.collider_size.x, self.collider_size.y)
    
    def is_colliding(self, other):
        rect1 = self.get_rect()
        rect2 = other.get_rect()

        if self.get_collider_tag() == other.get_collider_tag():
            return False
        
        return rect1.colliderect(rect2)
    
    def is_point_colliding(self, point):
        rect1 = pygame.Rect((self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y), (self.collider_size.x, self.collider_size.y))
        return rect1.collidepoint((point.x, point.y))
     