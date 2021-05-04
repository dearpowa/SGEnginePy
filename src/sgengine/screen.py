import sgengine
import pygame
from sgengine import Data2D

class Camera(sgengine.lifecycle.Entity):
    def start(self):
        self.size = Data2D(128, 72)
        self.tag = sgengine.DEFAULT_CAMERA
        self.current_frame = None
        self.debug_collider = False
    
    def draw(self, screen):
        camera_rect = pygame.Rect(0, 0, self.size.x, self.size.y)

        entity_list = self.current_scene().entity_list[:]
        
        entity_list.sort(key=lambda e: e.drawing_order)
        
        if self.check_for_frame():
            flags = pygame.HWSURFACE
            self.current_frame = pygame.Surface((self.size.x, self.size.y), flags)
        self.current_frame.fill((255, 255, 255))

        for e in entity_list:
            if issubclass(type(e), SpriteRenderer):
                sprite_screen_pos = Data2D(e.position.x - self.position.x - e.sprite_pivot.x, e.position.y - self.position.y - e.sprite_pivot.x)
                sprite_to_render = e.sprite_data

                sprite_rect = pygame.Rect(sprite_screen_pos.x, sprite_screen_pos.y, sprite_to_render.get_width(), sprite_to_render.get_height())

                if not sprite_rect.colliderect(camera_rect):
                    continue
                
                if e.sprite_flipped.x or e.sprite_flipped.y:
                    sprite_to_render = pygame.transform.flip(sprite_to_render, e.sprite_flipped.x, e.sprite_flipped.y)

                if e.sprite_rotation != 0:
                    sprite_to_render = pygame.transform.rotate(sprite_to_render, e.sprite_rotation)

                self.current_frame.blit(sprite_to_render, (sprite_screen_pos.x, sprite_screen_pos.y))
        
        if self.debug_collider:
            for c in self.current_scene().colliders_list():
                collider = pygame.Surface((c.collider_size.x, c.collider_size.y))
                collider.fill((0, 255, 0))
                self.current_frame.blit(collider, (c.collider_position.x - self.position.x - c.collider_pivot.x, c.collider_position.y - self.position.y - c.collider_pivot.y))
        
        w, h = pygame.display.get_surface().get_size()
        self.current_frame = pygame.transform.scale(self.current_frame, (w, h))
        screen.blit(self.current_frame, (0,0))

    def check_for_frame(self):
        return self.current_frame == None or (self.current_frame.get_width() != self.size.x or self.current_frame.get_height() != self.size.y)

class SpriteRenderer:
    @property
    def sprite_data(self):
        if not hasattr(self, "_sprite_data"):
            self._sprite_data = None
        return self._sprite_data

    @sprite_data.setter
    def sprite_data(self, sprite_data):
        self._sprite_data = sprite_data
    
    @property
    def sprite_flipped(self):
        if not hasattr(self, "_sprite_flipped"):
            self._sprite_flipped = Data2D(False, False)
        return self._sprite_flipped

    @sprite_flipped.setter
    def sprite_flipped(self, sprite_flipped):
        self._sprite_flipped = sprite_flipped
    
    @property
    def sprite_pivot(self):
        if not hasattr(self, "_sprite_pivot"):
            self._sprite_pivot = Data2D(0, 0)
        return self._sprite_pivot

    @sprite_pivot.setter
    def sprite_pivot(self, sprite_pivot):
        self._sprite_pivot = sprite_pivot
    
    @property
    def sprite_rotation(self):
        if not hasattr(self, "_sprite_rotation"):
            self._sprite_rotation = 0
        return self._sprite_rotation

    @sprite_rotation.setter
    def sprite_rotation(self, sprite_rotation):
        self._sprite_rotation = sprite_rotation

    def set_sprite(self, sprite_path):
        self.sprite_data = sgengine.load_image(sprite_path)

class Animation:
    def __init__(self, frame_time, *frames):
        self.animation_frames = frames
        self.frame_time = frame_time
        self.last_time = current_time_ms()
        self.current_frame = 0
    
    def reset_timer(self):
        self.last_time = current_time_ms()
    
    def get_frame_at_time(self, time):
        while self.last_time < time:
            self.last_time += self.frame_time
            self.current_frame += 1
            
            if self.current_frame >= len(self.animation_frames):
                self.current_frame = 0
        
        return self.animation_frames[self.current_frame]
 