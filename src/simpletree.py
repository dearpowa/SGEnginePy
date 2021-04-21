from sgengine import Entity, SpriteRenderer, Data2D, Collider

class Tree(Entity, SpriteRenderer, Collider):
    def start(self):
        self.set_sprite("simpletree.png")
        self.sprite_pivot = Data2D(4, 8)
        
    def fixed_update(self, delta_time):
        self.drawing_order = self.position.y
        
    def provide_position(self):
        return self.position
    
    def provide_pivot(self):
        return Data2D(3, 0)
    
    def provide_size(self):
        return Data2D(6, 2)