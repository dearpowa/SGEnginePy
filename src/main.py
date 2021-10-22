import sgengine
from sgengine.lifecycle import Scene
from sgengine.screen import Camera
from testentity import TestEntity
from gamemanager import GameManager
from bgtest import BG

entity = TestEntity()
scene = Scene("scena 1")
camera = Camera()
scene.add_entities(entity, camera)

sgengine.start(scene)