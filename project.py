from pycat.core import Window, Sprite, Color, KeyCode
from pycat.experimental.ldtk_level_entities import get_levels_entities
from enum import Enum,auto
 
w = Window()

class Cat(Sprite):
    class Jstate(Enum):
        jump = auto()
        walk = auto()
    def on_create(self):
        self.rotation_mode.RIGHT_LEFT
        self.position = w.center
        self.image = "catleft.png"
        self.scale = 0.25
        self.jump = Cat.Jstate.walk
        self.jumptime = 0
        self.total = 16
        self.storgey = 0
    def on_update(self, dt):
        if w.is_key_pressed(KeyCode.A):
            self.image = "catleft.png"
            self.move_forward(-11)
        elif w.is_key_pressed(KeyCode.D):
            self.image = "catright.png"
            self.move_forward(11)
        if w.is_key_pressed(KeyCode.W):
            self.storgey = self.y
            self.jump = Cat.Jstate.jump
        if  self.jump == Cat.Jstate.jump:
            self.jump()
            self.jumptime += dt 
            if self.jumptime > self.total:
                self.jump = Cat.Jstate.walk
                self.jumptime = 0
    def jump(self):
        pass
    def fall(self):
        pass

cat = w.create_sprite(Cat)
w.run()