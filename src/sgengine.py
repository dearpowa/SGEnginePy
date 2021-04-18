import pygame

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
        

#basic classes
class Data2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
                self.current_frame.blit(pygame.transform.flip(e.sprite_data, e.sprite_flipped.x, e.sprite_flipped.y), (e.position.x - self.position.x - e.sprite_pivot.x, e.position.y - self.position.y - e.sprite_pivot.x))
        
        w, h = pygame.display.get_surface().get_size()
        self.current_frame = pygame.transform.scale(self.current_frame, (w, h))
        screen.blit(self.current_frame, (0,0))

class SpriteRenderer:
    def __init__(self):
        self.sprite_data = None
        self.sprite_flipped = Data2D(False, False)
        self.sprite_pivot = Data2D(0,0)
        print("Sprite renderer created")
    
    def set_sprite(self, sprite_path):
        self.sprite_data = pygame.image.load("assets/" + sprite_path).convert_alpha()

        