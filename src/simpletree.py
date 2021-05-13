from sgengine import Data2D
from sgengine.lifecycle import Entity
from sgengine.screen import SpriteRenderer
from sgengine.physics import Collider

class Tree(Entity, SpriteRenderer, Collider):
    def start(self):
        self.set_sprite("simpletree.png")
        self.sprite_pivot_perc = Data2D(0.5, 1)
        self.collider_position = self.position
        #self.collider_pivot = Data2D(3, 0)
        self.collider_size = Data2D(6, 2)
        self.collider_pivot_perc = Data2D(0.5, 1)
        
    def fixed_update(self, delta_time):
        self.drawing_order = self.position.y