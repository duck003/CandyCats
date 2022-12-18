from pycat.core import Window, Sprite, Color, KeyCode
from pycat.experimental.ldtk_level_entities import get_levels_entities
from enum import Enum,auto
from pycat.experimental.ldtk_level_entities import (Entity, LevelData,
                                                    get_levels_entities)

ldtk_dir = "C:/Users/黃子晉/Desktop/Candycatr"
ldtk_file = ldtk_dir + "/LDTK.ldtk"
w = Window(width=1408, height=616)

class Level(Sprite):
    def on_create(self):
        self.image = "LDTK/png/Level_0.png"
        self.position = w.center
        level_data: list[LevelData] = get_levels_entities(ldtk_file)
        for ld in level_data:
            for e in ld.entities:
                self.create_entity(e)

    def create_entity(self, e: Entity):
        w.create_sprite(x=e.x, y=e.y, scale_x=e.width, scale_y=e.height,
                        opacity=100, tag=e.id, layer=2, color=Color.GREEN)

class Cat(Sprite):
    class Jstate(Enum):
        jump = auto()
        walk = auto()
    def on_create(self):
        self.layer = 4
        self.rotation_mode.RIGHT_LEFT
        self.position = w.center
        self.y = w.center.y - 72
        self.image = "catleft.png"
        self.scale = 0.15
        self.jumpstate = Cat.Jstate.walk
        self.uptime = 0
        self.half = 1
        self.storgey = 0
        self.fallsp  = -2

    def on_update(self, dt):
        land = self.get_touching_sprites_with_tag("Land")
        
        if w.is_key_pressed(KeyCode.LEFT):
            self.image = "catleft.png"
            self.move_forward(-1)
        elif w.is_key_pressed(KeyCode.RIGHT):
            self.image = "catright.png"
            self.move_forward(1)


        def jump(dt):
            if self.uptime < self.half:
                self.uptime += dt
                self.fallsp = 2
            elif self.uptime > self.half:
                print("w")
                self.fallsp = -4
                self.uptime = 0
                self.jumpstate = Cat.Jstate.walk

        if self.jumpstate is Cat.Jstate.walk:       
            if land: pass
            else:
                self.y += self.fallsp
            if w.is_key_down(KeyCode.UP):
                self.jumpstate = Cat.Jstate.jump

        if self.jumpstate is Cat.Jstate.jump:
            self.y += self.fallsp
            jump(dt)

        
        
level01 = w.create_sprite(Level)
cat = w.create_sprite(Cat)
w.run()