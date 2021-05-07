import sgengine as sg
import pygame

class BG(sg.lifecycle.Entity,
            sg.screen.SpriteRenderer, 
            sg.physics.Collider):
    
    def start(self):
        self.sprite_data = pygame.Surface((100, 10))
        self.sprite_data.fill((128, 128, 128))
        self.drawing_order = -100
        self.position = sg.Data2D(0, 100)
        self.collider_position = self.position
        self.collider_size = sg.Data2D(100, 10)
