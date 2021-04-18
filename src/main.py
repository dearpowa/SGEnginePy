import sgengine
from sgengine import Scene, Camera
from testentity import TestEntity
from gamemanager import GameManager
from bgtest import BG

entity = TestEntity()
gm = GameManager()
scene = Scene("scena 1")
camera = Camera()
scene.add_entity(entity)
scene.add_entity(camera)
scene.add_entity(gm)
scene.add_entity(BG())

sgengine.start(scene)