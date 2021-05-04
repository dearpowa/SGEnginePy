import sgengine
import pygame
import random
from sgengine import Data2D


class Collider:
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
    def collider_size(self):
        if not hasattr(self, "_collider_size"):
            self._collider_size = Data2D(0, 0)
        return self._collider_size

    @collider_size.setter
    def collider_size(self, collider_size):
        self._collider_size = collider_size
    
    def is_colliding(self, other):
        rect1 = pygame.Rect((self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y), (self.collider_size.x, self.collider_size.y))
        rect2 = pygame.Rect((other.collider_position.x - other.collider_pivot.x, other.collider_position.y - other.collider_pivot.y), (other.collider_size.x, other.collider_size.y))

        if self.get_collider_tag() == other.get_collider_tag():
            return False
        
        return rect1.colliderect(rect2)
    
    def is_point_colliding(self, point):
        rect1 = pygame.Rect((self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y), (self.collider_size.x, self.collider_size.y))
        return rect1.collidepoint((point.x, point.y))
     