from sgengine import Entity, SpriteRenderer
import pygame

class BG(Entity, SpriteRenderer):
    
    def start(self):
        self.set_sprite_data(pygame.Surface((100, 100)))
        self.get_sprite_data().fill((128, 128, 128))
        self.drawing_order = -100