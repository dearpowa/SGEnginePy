from sgengine import Entity, SpriteRenderer, Data2D, Collider

class Tree(Entity, SpriteRenderer, Collider):
    def start(self):
        self.set_sprite("simpletree.png")
        self.set_sprite_pivot(Data2D(4, 8))
        self.set_collider_position(self.position)
        self.set_collider_pivot(Data2D(3, 0))
        self.set_collider_size(Data2D(6, 2))
        
    def fixed_update(self, delta_time):
        self.drawing_order = self.position.y