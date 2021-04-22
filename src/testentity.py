import pygame
import sgengine
from pygame.locals import *
from sgengine import Entity, Data2D, SpriteRenderer, Collider

class TestEntity(Entity, SpriteRenderer, Collider):
    
    def start(self):
        self.movement_speed = 1
        self.inputH = Data2D(False, False)
        self.inputV = Data2D(False, False)
        self.movement = Data2D(0, 0)
        self.set_sprite("simpleguy_small.png")
        self.toggle = False
        self.set_sprite_pivot(Data2D(4, 8))
        #self.animation = sgengine.Animation(1000, 0, 90, 180, 270)
        self.virtual_pos = Data2D(0,0)
        self.set_collider_position(self.virtual_pos)
        self.set_collider_pivot(Data2D(3, -2))
        self.set_collider_size(Data2D(6, 1))
        
        #print(self.current_scene().tag)
    
    def update(self, events):
        
        #print(str(self.position.x) + " " + str(self.position.y))
        
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.inputH.x = True
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:                
                    self.inputH.y = True
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.inputV.x = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.inputV.y = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.inputH.x = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:                
                    self.inputH.y = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.inputV.x = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.inputV.y = False
        
        self.movement = Data2D(0,0)
        
        if self.inputH.x:
            self.movement.x = -1
        if self.inputH.y:
            self.movement.x = 1
        if self.inputH.x and self.inputH.y:
            self.movement.x = 0
            
        if self.inputV.x:
            self.movement.y = -1
        if self.inputV.y:
            self.movement.y = 1
        if self.inputV.x and self.inputV.y:
            self.movement.y = 0
        
        self.movement.x *= self.movement_speed
        self.movement.y *= self.movement_speed
        
        if self.movement.x > 0:
            self.get_sprite_flipped().x = False
        elif self.movement.x < 0:
            self.get_sprite_flipped().x = True
            
        #self.sprite_rotation = self.animation.get_frame_at_time(sgengine.current_time_ms())
        
        
    def fixed_update(self, delta_time):
        
        self.virtual_pos.x = self.position.x
        self.virtual_pos.y = self.position.y
        
        self.virtual_pos.x += self.movement.x * delta_time
        is_valid_pos_x = True

        for c in self.current_scene().colliders_list():
            #print("Self tag " + str(self.provide_tag()))
            if self.is_colliding(c):
                is_valid_pos_x = False
                #print("Other tag " + str(c.provide_tag()))
                break
            
        self.virtual_pos.y += self.movement.y * delta_time
        is_valid_pos_y = True
        
        for c in self.current_scene().colliders_list():
            #print("Self tag " + str(self.provide_tag()))
            if self.is_colliding(c):
                is_valid_pos_y = False
                #print("Other tag " + str(c.provide_tag()))
                break
        
        if is_valid_pos_x:
            self.position.x = self.virtual_pos.x
            
        if is_valid_pos_y:
            self.position.y = self.virtual_pos.y
        
        self.drawing_order = self.position.y
        
        for camera in self.current_scene().camera_list():
            if camera.tag == sgengine.DEFAULT_CAMERA:
                camera.position = Data2D(self.position.x - (camera.size.x / 2), self.position.y - (camera.size.y / 2))
        #print(str(self.position.x) + " " + str(self.position.y))
        
        
    #def draw(self, screen):
        #pygame.draw.rect(screen, "red", (self.position.x, self.position.y, 50, 50), 0)
        #screen.blit(self.sprite, (self.position.x, self.position.y))