from sgengine import Entity, SpriteRenderer, Data2D

class Tree(Entity, SpriteRenderer):
    def start(self):
        self.set_sprite("simpletree.png")
        self.sprite_pivot = Data2D(4, 8)
        
    def fixed_update(self, delta_time):
        self.drawing_order = self.position.y