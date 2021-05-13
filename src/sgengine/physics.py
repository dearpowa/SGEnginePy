import sgengine as sg
import pygame
import random
from sgengine import Data2D
import math
import pymunk as pk

physics_space = None

def apply_gravity(entity: sg.lifecycle.Entity, delta_time):
    move_entity(entity, Data2D(0, 2), delta_time)

def move_entity(entity: sg.lifecycle.Entity, how_much: Data2D, delta_time, precision=5):
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
            for c in sg.current_scene.colliders_list():
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

def init_physics():
    global physics_space
    physics_space = pk.Space()


def set_gravity(gravity):
    if physics_space != None:
        physics_space.gravity = gravity.x, dgravity.y

def run_physics():
    
    for x in range(120):
        physics_space.step(1/120)
    for c in sg.current_scene.colliders2_list():
        c.update_scene_position()

class Collider:
    @property
    def collider_tag(self):
        if not hasattr(self, "_collider_tag"):
            self._collider_tag = random.random() * 100000
        
        return self._collider_tag
    
    @collider_tag.setter
    def collider_tag(self, tag):
        self._collider_tag = tag

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

        if self.collider_tag == other.collider_tag:
            return False
        
        return rect1.colliderect(rect2)
    
    def is_point_colliding(self, point):
        rect1 = pygame.Rect((self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y), (self.collider_size.x, self.collider_size.y))
        return rect1.collidepoint((point.x, point.y))

class Collider2:
    def collider_has_started(self):
        if not hasattr(self, "_collider_has_started"):
            self._collider_has_started = False
        return self._collider_has_started

    @property
    def collider_body(self):
        if not hasattr(self, "_collider_body"):
            self._collider_body = None
        return self._collider_body

    @collider_body.setter
    def collider_body(self, collider_body):
        #Quando cambio il body di un collider
        #devo anche rimuoverlo dallo spazio fisico
        if self.collider_body != None:
            physics_space.remove(self.collider_body)

        self._collider_body = collider_body
        if self.collider_body.body_type != pk.Body.KINEMATIC:
            physics_space.add(self.collider_body)


    @property
    def collider_shape(self):
        if not hasattr(self, "_collider_shape"):
            self._collider_shape = None
        return self._collider_shape

    @collider_shape.setter
    def collider_shape(self, collider_shape):
        #Quando cambio lo shape di un collider
        #devo anche rimuoverlo dallo spazio fisico
        if self.collider_shape != None:
            physics_space.remove(self.collider_shape)

        self._collider_shape = collider_shape
        physics_space.add(self.collider_shape)


    @property
    def collider_position(self):
        if not hasattr(self, "_collider_position"):
            self._collider_position = Data2D(0, 0)
        return self._collider_position

    @collider_position.setter
    def collider_position(self, collider_position):
        self._collider_position = collider_position
        self.update_body_position()

    @property
    def collider_pivot(self):
        if not hasattr(self, "_collider_pivot"):
            self._collider_pivot = Data2D(0, 0)
        return self._collider_pivot

    @collider_pivot.setter
    def collider_pivot(self, collider_pivot):
        self._collider_pivot = collider_pivot
        self.update_body_position()

    @property
    def collider_velocity(self):
        vel = Data2D(0, 0)
        if self.collider_body != None:
            vel.x, vel.y = self.collider_body.velocity
        return vel

    @collider_velocity.setter
    def collider_velocity(self, velocity):
        if self.collider_body != None:
            self.collider_body.velocity = velocity.x, velocity.y
    @property    
    def collider_size(self):
        if not hasattr(self, "_collider_size"):
            self._collider_size = Data2D(0, 0)
        return self._collider_size

    #Aggiorna la posizione del body nella simulazione fisica
    def update_body_position(self):
        if self.collider_body != None:
            self.collider_body.position = self.collider_position.x - self.collider_pivot.x, self.collider_position.y - self.collider_pivot.y
            physics_space.reindex_shapes_for_body(self.collider_body)

    #Aggiorna la posizione del collider nella scena
    def update_scene_position(self):
        if self.collider_position != None:
            self.collider_position.x, self.collider_position.y = self.collider_body.position[0] + self.collider_pivot.x, self.collider_body.position[1] + self.collider_pivot.y
class BoxCollider(Collider2):
    def start_collider(self, position, pivot, size, body_type):
        self._collider_has_started = True
        self.collider_body = pk.Body(body_type=body_type)
        self.resize(size)
        self.collider_shape.density = 1

        self.collider_position = position
        self.collider_pivot = pivot

    def resize(self, size):
        self._collider_size = size
        self.collider_shape = pk.Poly(self.collider_body, [(0, 0), (size.x, 0), (size.x, size.y), (0, size.y)])
