import pygame
import sgengine

class TestEntity(sgengine.lifecycle.Entity, sgengine.screen.SpriteRenderer, sgengine.physics.Collider):
    
    def start(self):
        self.movement_speed = 10
        self.inputH = sgengine.Data2D(False, False)
        self.inputV = sgengine.Data2D(False, False)
        self.movement = sgengine.Data2D(0, 0)
        self.set_sprite("simpleguy_small.png")
        self.sprite_resize(sgengine.Data2D(80, 80))
        self.toggle = False
        #self.sprite_pivot = Data2D(0, 8)
        self.sprite_pivot_perc = sgengine.Data2D(0.5, 1)
        #self.animation = sgengine.Animation(1000, 0, 90, 180, 270)
        self.collider_position = self.position
        #self.collider_pivot = Data2D(3, -2)
        self.collider_size = sgengine.Data2D(6, 2)
        self.collider_pivot_perc = sgengine.Data2D(0.5, 1)
        self.audio1 = sgengine.load_audio("shoot2.wav")
        self.play_audio = False
        self.played = False
        self.is_big = False
        
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
                if event.key == pygame.K_SPACE:
                    self.play_audio = True
                    self.toggle_resize()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.inputH.x = False
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:                
                    self.inputH.y = False
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.inputV.x = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.inputV.y = False
                if event.key == pygame.K_SPACE:
                    self.play_audio = False
                    self.played = False
        
        self.movement = sgengine.Data2D(0,0)
        
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
            self.sprite_flipped.x = False
        elif self.movement.x < 0:
            self.sprite_flipped.x = True

        if self.play_audio and not self.played:
            self.audio1.play()
            self.played = True
            
        #self.sprite_rotation = self.animation.get_frame_at_time(sgengine.current_time_ms())
        
        
    def fixed_update(self, delta_time):
        #print(self.position)
        sgengine.physics.apply_gravity(self, delta_time, True)
        sgengine.physics.move_entity(self, sgengine.Data2D(self.movement.x, 0), delta_time)
        #print(self.position)
        for camera in self.current_scene().camera_list():
            if camera.tag == sgengine.DEFAULT_CAMERA:
                camera.position = sgengine.Data2D(self.position.x - (camera.size.x / 2), self.position.y - (camera.size.y / 2))
        

    def toggle_resize(self):
        self.is_big = not self.is_big
        if self.is_big:
            self.sprite_resize(sgengine.Data2D(16, 16))
            self.collider_size = sgengine.Data2D(12, 4)
        else:
            self.sprite_resize(sgengine.Data2D(8, 8))
            self.collider_size = sgengine.Data2D(6, 2)
    #def draw(self, screen):
        #pygame.draw.rect(screen, "red", (self.position.x, self.position.y, 50, 50), 0)
        #screen.blit(self.sprite, (self.position.x, self.position.y))