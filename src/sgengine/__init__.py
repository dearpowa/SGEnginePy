import pygame
import time
import random

DEFAULT_CAMERA = "def_c"
running = False
window = None
current_scene = None
clock = None
framerate = 60
target_framerate = 60
log_active = False
current_res = (0,0)
fullscreen = False

#stuff for running
def clear_screen():
    global window
    window.fill((255, 255, 255))

def update(events):
    global window, current_scene
    for entity in current_scene.entity_list:
        entity.update(events)
        
def fixed_update():
    global current_scene, clock, target_framerate
    
    physics.run_physics()
    clock.tick(framerate)
    t = pygame.time.get_ticks()
    time = clock.get_time()
    delta_time = target_framerate / (1000 / time)
    if log_active:
        print("Delta time: " + str(delta_time))
    
    for entity in current_scene.entity_list:
        entity.fixed_update(delta_time)

def draw():
    global window, current_scene
    #clear_screen()
    for camera in current_scene.camera_list():
        camera.draw(window)
    pygame.display.update()

def start(scene):
    global running, window, current_scene, clock
    pygame.init()
    clock = pygame.time.Clock()

    physics.init_physics()
    
    current_scene = scene
    
    res = (720, 400)
    
    change_resolution(res)
    pygame.display.set_caption("SGEnginePy v0.1")

    running = True
    
    if log_active:
        print("Start")

    try:
        for entity in current_scene.entity_list:
            entity.start()
    finally:
        pass
    
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
    global window, current_res
    current_res = res
    window = pygame.display.set_mode(current_res, flags=pygame.DOUBLEBUF)

def toggle_fullscreen():
    global window, current_res, fullscreen
    fullscreen = not fullscreen
    if fullscreen:
        window = pygame.display.set_mode(current_res, pygame.FULLSCREEN)
    else:
        window = pygame.display.set_mode(current_res)
        
def current_time_ms():
    return round(time.time() * 1000)

def load_image(image_path):
    return pygame.image.load(f"assets/{image_path}").convert_alpha()

def load_audio(audio_path):
    return pygame.mixer.Sound(f"assets/{audio_path}")


#Basic classes
class Data2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f'Data2D({self.x},{self.y})'