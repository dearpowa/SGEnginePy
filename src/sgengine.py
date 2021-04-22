import pygame, time, random

DEFAULT_CAMERA = "def_c"
running = False
screen = None
current_scene = None
clock = None
framerate = 60
target_framerate = 60
log_active = False
current_res = (0,0)
fullscreen = False

#stuff for running
def clear_screen():
    global screen
    screen.fill((255, 255, 255))

def update(events):
    global screen, current_scene
    for entity in current_scene.entity_list:
        entity.update(events)
        
def fixed_update():
    global current_scene, clock, target_framerate
    
    clock.tick(framerate)
    t = pygame.time.get_ticks()
    time = clock.get_time()
    delta_time = target_framerate / (1000 / time)
    if log_active:
        print("Delta time: " + str(delta_time))
    
    for entity in current_scene.entity_list:
        entity.fixed_update(delta_time)

def draw():
    global screen, current_scene
    clear_screen()
    for camera in current_scene.camera_list():
        camera.draw(screen)
    pygame.display.update()

def start(scene):
    global running, screen, current_scene, clock
    pygame.init()
    clock = pygame.time.Clock()
    
    current_scene = scene
    
    res = (720, 400)
    
    change_resolution(res)
    pygame.display.set_caption("SGEnginePy v0.1")

    running = True
    
    if log_active:
        print("Start")
    for entity in current_scene.entity_list:
        entity.start()
    
    while running:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                
        try:
            update(events)
            fixed_update()
            draw()
        finally:
            pass
        if log_active:
            print("Fps: " + str(clock.get_fps()))
            #print("Res: " + str(res))

    pygame.quit()
    if log_active:
        print("Ended")
    
def change_resolution(res):
    global screen, current_res
    current_res = res
    screen = pygame.display.set_mode(current_res)

def toggle_fullscreen():
    global screen, current_res, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        screen = pygame.display.set_mode(current_res, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(current_res)
        
def current_time_ms():
    return round(time.time() * 1000)

def load_image(image_path):
    return pygame.image.load("assets/" + image_path).convert_alpha()

#basic classes
class Data2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Data2D({self.x},{self.y})'

class Scene:
    def __init__(self, tag):
        self.entity_list = []
        self.tag = tag
        
    def camera_list(self):
        camera_list = []
        for e in self.entity_list:
            if issubclass(type(e), Camera):
                camera_list.append(e)
        return camera_list
    
    def colliders_list(self):
        colliders_list = []
        for e in self.entity_list:
            if issubclass(type(e), Collider):
                colliders_list.append(e)
        return colliders_list
    
    def add_entity(self, entity):
        if issubclass(type(entity), Entity):
            self.entity_list.append(entity)
            return True
        else:
            return False
        
    def add_entity_and_start(self, entity):
        if self.add_entity(entity):
            entity.start()
            return True
        else:
            return False
        
        
class Entity:
    def __init__(self):
        self.position = Data2D(0,0)
        self.drawing_order = 0
        super(Entity, self).__init__()
        if log_active:
            print("Entity created")
        
    def start(self):
        pass
        
    def update(self, events):
        pass
    
    #Accade 60 volte per frame (ipoteticamente)
    def fixed_update(self, delta_time):
        pass
    
    def current_scene(self):
        global current_scene
        return current_scene
    
class Camera(Entity):
    def start(self):
        self.size = Data2D(128, 72)
        self.tag = DEFAULT_CAMERA
        self.current_frame = None
        self.debug_collider = False
        
    def update(self, events):
        pass
    
    def draw(self, screen):
        entity_list = self.current_scene().entity_list[:]
        
        entity_list.sort(key=lambda e: e.drawing_order)
        
        flags = pygame.SRCALPHA|pygame.HWSURFACE
        self.current_frame = pygame.Surface((self.size.x, self.size.y), flags)
        self.current_frame = self.current_frame.convert_alpha()
        
        for e in entity_list:
            if issubclass(type(e), SpriteRenderer):
                self.current_frame.blit(pygame.transform.rotate(pygame.transform.flip(e.get_sprite_data(), e.get_sprite_flipped().x, e.get_sprite_flipped().y), e.get_sprite_rotation()), (e.position.x - self.position.x - e.get_sprite_pivot().x, e.position.y - self.position.y - e.get_sprite_pivot().x))
        
        if self.debug_collider:
            for c in self.current_scene().colliders_list():
                collider = pygame.Surface((c.get_collider_size().x, c.get_collider_size().y))
                collider.fill((0, 255, 0))
                self.current_frame.blit(collider, (c.get_collider_position().x - self.position.x - c.get_collider_pivot().x, c.get_collider_position().y - self.position.y - c.get_collider_pivot().y))
        
        w, h = pygame.display.get_surface().get_size()
        self.current_frame = pygame.transform.scale(self.current_frame, (w, h))
        screen.blit(self.current_frame, (0,0))

class SpriteRenderer:
    def set_sprite_data(self, sprite_data):
        self.sprite_data = sprite_data
            
    def get_sprite_data(self):
        if not hasattr(self, "sprite_data"):
            self.sprite_data = None
        return self.sprite_data
    
    def set_spite_flipped(self, sprite_flipped):
        self.sprite_flipped = sprite_flipped
    
    def get_sprite_flipped(self):
        if not hasattr(self, "sprite_flipped"):
            self.sprite_flipped = Data2D(False, False)
        return self.sprite_flipped
    
    def set_sprite_pivot(self, sprite_pivot):
        self.sprite_pivot = sprite_pivot
    
    def get_sprite_pivot(self):
        if not hasattr(self, "sprite_pivot"):
            self.sprite_pivot = Data2D(0, 0)
        return self.sprite_pivot
    
    def set_sprite_rotation(self, sprite_rotation):
        self.sprite_rotation = sprite_rotation
    
    def get_sprite_rotation(self):
        if not hasattr(self, "sprite_rotation"):
            self.sprite_rotation = 0
        return self.sprite_rotation
    
    def set_sprite(self, sprite_path):
        self.sprite_data = load_image(sprite_path)


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
    
class Collider:
    def get_collider_tag(self):
        if not hasattr(self, "tag"):
            self.tag = random.random() * 100000
        
        return self.tag
    
    def set_collider_position(self, collider_position):
        self.collider_position = collider_position
    
    def get_collider_position(self):
        if not hasattr(self, "collider_position"):
            self.collider_position = Data2D(0, 0)
        return self.collider_position
    
    def set_collider_pivot(self, collider_pivot):
        self.collider_pivot = collider_pivot
    
    def get_collider_pivot(self):
        if not hasattr(self, "collider_pivot"):
            self.collider_pivot = Data2D(0, 0)
        return self.collider_pivot
    
    def set_collider_size(self, collider_size):
        self.collider_size = collider_size
    
    def get_collider_size(self):
        if not hasattr(self, "collider_size"):
            self.collider_size = Data2D(0, 0)
        return self.collider_size
    
    def is_colliding(self, other):
        rect1 = pygame.Rect((self.get_collider_position().x - self.get_collider_pivot().x, self.get_collider_position().y - self.get_collider_pivot().y), (self.get_collider_size().x, self.get_collider_size().y))
        rect2 = pygame.Rect((other.get_collider_position().x - other.get_collider_pivot().x, other.get_collider_position().y - other.get_collider_pivot().y), (other.get_collider_size().x, other.get_collider_size().y))
        
        if self.get_collider_tag() == other.get_collider_tag():
            return False
        
        return rect1.colliderect(rect2)
    
    def is_point_colliding(self, point):
        rect1 = pygame.Rect((self.get_collider_position().x - self.get_collider_pivot().x, self.get_collider_position().y - self.get_collider_pivot().y), (self.get_collider_size().x, self.get_collider_size().y))
        return rect1.collidepoint((point.x, point.y))
        
        
class Tilemap(Entity, SpriteRenderer):
    def __init__():
        pass