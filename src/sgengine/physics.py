import sgengine
import pygame
import random
from sgengine import Data2D


class Collider:
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
     