from pycat.core import Window, Sprite, Color, KeyCode, Scheduler, Label
from pycat.experimental.ldtk_level_entities import get_levels_entities
from enum import Enum,auto
from pycat.experimental.ldtk_level_entities import (Entity, LevelData,
                                                    get_levels_entities)
import random

ldtk_dir = "C:/Users/黃子晉/Desktop/Candycatr"
ldtk_file = ldtk_dir + "/LDTK.ldtk"
w = Window(width=1408, height=616)

candylist = [
    "assets/blue.png",
    "assets/green.png",
    "assets/pink.png",
    "assets/purple.png",
    "assets/yellow.png"]

meal = 0

class Scorer(Label):
    global meal
    def on_create(self):
        self.y = w.height
        self.x = 0
        self.layer = 4
        self.color = Color.WHITE
        self.font_size = 24
        self.text = "Candy eat:"+ str(meal)

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

class Hitox(Sprite):
    class Jstate(Enum):
        jump = auto()
        walk = auto()
        fall = auto()
    def on_create(self):
        self.add_tag("box")
        self.width = cat.width
        self.height = 2
        self.color = Color.RED
        self.position = w.center
        self.jumpstate = Hitox.Jstate.walk
        self.uptime = 0
        self.half = 1
        self.storgey = 0
        self.jumpsp  = -4
        self.opacity = 0
        self.gravtiy = 0.6

    def on_update(self, dt):
        land = self.get_touching_sprites_with_tag("Land")
        
        if w.is_key_pressed(KeyCode.LEFT):
            self.move_forward(-2)
        elif w.is_key_pressed(KeyCode.RIGHT):
            self.move_forward(2)


        if self.jumpstate is Hitox.Jstate.walk:       
            if not land:
                self.jumpstate = Hitox.Jstate.fall
            if w.is_key_down(KeyCode.UP):
                self.jumpsp = 12
                self.jumpstate = Hitox.Jstate.jump

        elif self.jumpstate is Hitox.Jstate.jump:
            self.y += self.jumpsp            
            self.jumpsp -= self.gravtiy
            if self.jumpsp < 0:
                self.jumpstate = Hitox.Jstate.fall
        elif self.jumpstate is Hitox.Jstate.fall: 
            self.jumpsp -= self.gravtiy
            self.y += self.jumpsp
            if land: 
                self.jumpsp = 0
                self.jumpstate = Hitox.Jstate.walk
                self.y = land[0].y + land[0].height/2

class Cat(Sprite):
    def on_create(self):
        self.add_tag("cat")
        self.layer = 4
        self.rotation_mode.RIGHT_LEFT
        self.position = w.center
        self.y = w.center.y - 72
        self.image = "catleft.png"
        self.scale = 0.15

    def on_update(self, dt):
        self.position = hitox.position
        self.y = self.y + self.height/2- hitox.height
        if w.is_key_pressed(KeyCode.LEFT):
            self.image = "catleft.png"
        elif w.is_key_pressed(KeyCode.RIGHT):
            self.image = "catright.png"

class Candy(Sprite):
    def on_create(self):
        z = random.randint(0,4)
        self.image = candylist[z]
        self.scale = 0.32
        self.goto_random_position()
        self.is_visible = False
    
    def on_update(self, dt):
        global meal
        if self.is_touching_any_sprite_with_tag("Land"):
            self.goto_random_position()
        else:
            self.is_visible = True
        if self.is_touching_any_sprite_with_tag("cat"):
            if self.image is candylist[0]:
                meal += 1
                scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[1]:
                meal += 1
                scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[2]:
                meal += 1
                scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[3]:
                meal += 1
                scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[4]:
                meal += 1
                scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            


def spawn_candy():
    w.create_sprite(Candy)
        
Scheduler.update(spawn_candy,2)

level01 = w.create_sprite(Level)
scorer = w.create_label(Scorer)
cat = w.create_sprite(Cat)
hitox = w.create_sprite(Hitox)
w.run()