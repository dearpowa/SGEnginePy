from sgengine import Data2D
from sgengine.lifecycle import Entity
from sgengine.screen import SpriteRenderer
from sgengine.physics import Collider
import pygame

class BG(Entity, SpriteRenderer, Collider):
    
    def start(self):
        self.sprite_data = pygame.Surface((1000, 70))
        self.sprite_data.fill((128, 128, 128))
        self.drawing_order = -100
        self.collider_size = Data2D(1000, 70)
        self.position = Data2D(-10, 100)
        self.collider_position = self.position