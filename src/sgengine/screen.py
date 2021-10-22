import sgengine
import pygame

class Camera(sgengine.lifecycle.Entity):
    def start(self):
        self.size = sgengine.Data2D(800, 600)
        self.tag = sgengine.DEFAULT_CAMERA
        self.current_frame = None
        self.debug_collider = False
        self.debug_sprite_pivot = False
        self.debug_collider_pivot = False
    
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
                sprite_screen_pos = sgengine.Data2D(e.position.x - self.position.x - e.sprite_pivot.x, e.position.y - self.position.y - e.sprite_pivot.y)
                sprite_to_render = e.sprite_data

                sprite_rect = pygame.Rect(sprite_screen_pos.x, sprite_screen_pos.y, sprite_to_render.get_width(), sprite_to_render.get_height())

                if not sprite_rect.colliderect(camera_rect):
                    continue
                
                if e.sprite_flipped.x or e.sprite_flipped.y:
                    sprite_to_render = pygame.transform.flip(sprite_to_render, e.sprite_flipped.x, e.sprite_flipped.y)

                if e.sprite_rotation != 0:
                    sprite_to_render = pygame.transform.rotate(sprite_to_render, e.sprite_rotation)

                if e.sprite_colorkey != None:
                    sprite_to_render.set_colorkey(e.sprite_colorkey)

                self.current_frame.blit(sprite_to_render, (sprite_screen_pos.x, sprite_screen_pos.y))

                if self.debug_sprite_pivot:
                    sprite_pivot_pos = sgengine.Data2D(e.position.x - self.position.x, e.position.y - self.position.y)
                    pygame.draw.circle(self.current_frame, (255, 255, 0), (sprite_pivot_pos.x, sprite_pivot_pos.y), 1)

            if hasattr(e, "text") and e.text != None and hasattr(e, "rect") and e.rect != None:
                self.current_frame.blit(e.text, e.rect)
        if self.debug_collider:
            for c in self.current_scene().colliders_list():
                collider = pygame.Surface((c.collider_size.x, c.collider_size.y))
                collider.fill((0, 255, 0))
                self.current_frame.blit(collider, (c.collider_position.x - self.position.x - c.collider_pivot.x, c.collider_position.y - self.position.y - c.collider_pivot.y))
                if self.debug_collider_pivot:
                    collider_pivot_pos = sgengine.Data2D(c.collider_position.x - self.position.x, c.collider_position.y - self.position.y)
                    pygame.draw.circle(self.current_frame, (255, 128, 0), (collider_pivot_pos.x, collider_pivot_pos.y), 1)
        
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
        
        #Aggiunto per gestione color key
        if self.sprite_colorkey != None:
            self._sprite_data.set_colorkey(self.sprite_colorkey)

        return self._sprite_data

    @sprite_data.setter
    def sprite_data(self, sprite_data):
        sprite_pivot_perc_temp = self.sprite_pivot_perc
        self._sprite_data = sprite_data
        #Aggiunto in modo che al cambio dello sprite
        #il pivot rimanaga lo "stesso" in percentuale alle grandezze
        #diverse
        if self.sprite_data != None:
            self.sprite_pivot_perc = sprite_pivot_perc_temp
    
    @property
    def sprite_flipped(self):
        if not hasattr(self, "_sprite_flipped"):
            self._sprite_flipped = sgengine.Data2D(False, False)
        return self._sprite_flipped

    @sprite_flipped.setter
    def sprite_flipped(self, sprite_flipped):
        self._sprite_flipped = sprite_flipped
    
    @property
    def sprite_pivot(self):
        if not hasattr(self, "_sprite_pivot"):
            self._sprite_pivot = sgengine.Data2D(0, 0)
        return self._sprite_pivot

    @sprite_pivot.setter
    def sprite_pivot(self, sprite_pivot):
        self._sprite_pivot = sprite_pivot

    @property
    def sprite_pivot_perc(self):
        if self.sprite_data != None:
            pivot_perc = sgengine.Data2D(self.sprite_pivot.x / self.sprite_data.get_width(), self._sprite_pivot.y / self.sprite_data.get_height())
            return pivot_perc
        return None

    @sprite_pivot_perc.setter
    def sprite_pivot_perc(self, sprite_pivot_perc):
        if self.sprite_data != None and sprite_pivot_perc != None:
            self.sprite_pivot = sgengine.Data2D(sprite_pivot_perc.x * self.sprite_data.get_width(), sprite_pivot_perc.y * self.sprite_data.get_height())

    @property
    def sprite_rotation(self):
        if not hasattr(self, "_sprite_rotation"):
            self._sprite_rotation = 0
        return self._sprite_rotation

    @sprite_rotation.setter
    def sprite_rotation(self, sprite_rotation):
        self._sprite_rotation = sprite_rotation

    @property
    def sprite_colorkey(self):
        if not hasattr(self, "_sprite_colorkey"):
            self._sprite_colorkey = None
        return self._sprite_colorkey
    
    @sprite_colorkey.setter
    def sprite_colorkey(self, sprite_colorkey):
        self._sprite_colorkey = sprite_colorkey

    def set_sprite(self, sprite_path):
        self.sprite_data = sgengine.load_image(sprite_path)

    def sprite_resize(self, resize_to):
        if self.sprite_data != None:
            self.sprite_data = pygame.transform.scale(self.sprite_data, (resize_to.x, resize_to.y))

class Animation:
    def __init__(self, frame_time, *frames):
        self.animation_frames = frames
        self.frame_time = frame_time
        self.last_time = sgengine.current_time_ms()
        self.current_frame = 0
    
    def reset_timer(self):
        self.last_time = sgengine.current_time_ms()
    
    def get_frame_at_time(self, time):
        while self.last_time < time:
            self.last_time += self.frame_time
            self.current_frame += 1
            
            if self.current_frame >= len(self.animation_frames):
                self.current_frame = 0
        
        return self.animation_frames[self.current_frame]