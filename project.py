from pycat.core import Window, Sprite, Color, KeyCode, Scheduler, Label
from pycat.experimental.ldtk_level_entities import get_levels_entities
from enum import Enum,auto
from pycat.experimental.ldtk_level_entities import (Entity, LevelData,
                                                    get_levels_entities)
import random

ldtk_dir = "C:/Users/黃子晉/Desktop/Candycatr"
ldtk_file = ldtk_dir + "/LDTK.ldtk"
w = Window(width=1408, height=616,enforce_window_limits=False)

candylist = [
    "assets/blue.png",
    "assets/green.png",
    "assets/pink.png",
    "assets/purple.png",
    "assets/yellow.png"]

meal = 0

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
        JUMP = auto()
        WALK = auto()
        FALL = auto()
    class Estate(Enum):
        FLOATR = auto()
        POISON = auto()
        AIDKIT = auto()
        HUNGRY = auto()
        NORMAL = auto()
    def on_create(self):
        self.add_tag("box")
        self.width = cat.width
        self.height = 2
        self.color = Color.RED
        self.position = w.center
        self.jumpstate = Hitox.Jstate.WALK
        self.effectate = Hitox.Estate.NORMAL
        self.uptime = 0
        self.half = 1
        self.storgey = 0
        self.jumpsp  = -4
        self.opacity = 0
        self.gravtiy = 0.6
        self.eloading = 0
        self.effectime = 0
        self.lifetime = 4
        self.mycolor = self.color
        self.vhungry = 0

    def on_update(self, dt):
        land = self.get_touching_sprites_with_tag("Land")

#       MOVE___________________________________
        if w.is_key_pressed(KeyCode.LEFT):
            self.move_forward(-4)
        elif w.is_key_pressed(KeyCode.RIGHT):
            self.move_forward(4)
        
        if self.x > w.width:
            self.x = 1
        elif self.x < 0:
            self.x = w.width-1

#       JUMP___________________________________
        if self.effectate is not Hitox.Estate.FLOATR:
            if self.jumpstate is Hitox.Jstate.WALK:       
                if not land:
                    self.jumpstate = Hitox.Jstate.FALL
                if w.is_key_down(KeyCode.UP):
                    self.jumpsp = 12
                    self.jumpstate = Hitox.Jstate.JUMP

            elif self.jumpstate is Hitox.Jstate.JUMP:
                self.y += self.jumpsp            
                self.jumpsp -= self.gravtiy
                if self.jumpsp < 0:
                    self.jumpstate = Hitox.Jstate.FALL
            elif self.jumpstate is Hitox.Jstate.FALL: 
                self.jumpsp -= self.gravtiy
                self.y += self.jumpsp
                if land: 
                    self.jumpsp = 0
                    self.jumpstate = Hitox.Jstate.WALK
                    self.y = land[0].y + land[0].height/2

#       EFFECT_______________________________________
        if self.effectate is Hitox.Estate.FLOATR:
            self.effectime = 2
            self.floatr(dt)
        elif self.effectate is Hitox.Estate.POISON:
            self.lifetime -= dt
            life.text = "Life Timer:" + str(int(hitox.lifetime))
            self.color = Color.GREEN
            if self.lifetime < 0:
                print("YOU LOS NOW")
                w.close()
        elif self.effectate is Hitox.Estate.AIDKIT:
            self.color = self.mycolor
            self.lifetime += 9
            life.text = "Life Timer:" + str(int(hitox.lifetime))
            self.effectate = Hitox.Estate.NORMAL
        elif self.effectate is Hitox.Estate.HUNGRY:            
            if self.vhungry == 0:
                self.effectate = Hitox.Estate.NORMAL

    def floatr(self,dt):
        self.y += 2
        self.eloading += dt
        if self.eloading > self.effectime:
            self.effectate = Hitox.Estate.NORMAL
            self.eloading = 0
       

class Cat(Sprite):
    def on_create(self):
        self.add_tag("cat")
        self.layer = 4
        self.rotation_mode.RIGHT_LEFT
        self.position = w.center
        self.y = w.center.y - 72
        self.image = "catleft.png"
        self.scale = 0.15
        self.mycolor = self.color 

    def on_update(self, dt):
        self.position = hitox.position
        self.y = self.y + self.height/2- hitox.height
        if w.is_key_pressed(KeyCode.LEFT):
            self.image = "catleft.png"
        elif w.is_key_pressed(KeyCode.RIGHT):
            self.image = "catright.png"

        if hitox.effectate is Hitox.Estate.POISON:
            self.color = Color.GREEN
        elif hitox.effectate is Hitox.Estate.AIDKIT:
            self.color = self.mycolor
            

class TooHightr(Sprite):
    def on_create(self):
        self.image = "assets/up.png"
        self.layer = 2
        self.scale = 0.36
        self.is_visible = False
        self.y = w.height - self.height/2
    def on_update(self, dt):
        self.x = cat.x
        if hitox.y > w.height:
            self.is_visible = True
        else:
            self.is_visible = False

class Scorer(Label):
    global meal
    def on_create(self):
        self.font_size = 24
        self.text = "Candy eat:"+ str(meal)
        self.y = self.content_height
        self.x = 0
        self.layer = 4
        self.color = Color.WHITE

scorer = w.create_label(Scorer)

class Candy(Sprite):
    global scorer
    def on_create(self):
        z = random.randint(0,4)
        self.layer = 4
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
                hitox.effectate = Hitox.Estate.FLOATR
                if hitox.vhungry != 0:
                    hitox.vhungry -= 1
                    hungyr.text = "How hungry:"+ str(hitox.vhungry)
                elif hitox.vhungry == 0:
                    meal += 1
                    scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[1]:
                hitox.effectate = Hitox.Estate.POISON
                if hitox.vhungry != 0:
                    hitox.vhungry -= 4
                    hungyr.text = "How hungry:"+ str(hitox.vhungry)
                elif hitox.vhungry == 0:
                    meal += 4
                    scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[2]:
                hitox.effectate = Hitox.Estate.AIDKIT
                if hitox.vhungry != 0:
                    hitox.vhungry -= 1
                    hungyr.text = "How hungry:"+ str(hitox.vhungry)
                elif hitox.vhungry == 0:
                    meal += 1
                    scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            if self.image is candylist[3]:
                hitox.effectate = Hitox.Estate.HUNGRY
                hitox.vhungry += 5
                hungyr.text = "How hungry:"+ str(hitox.vhungry)
                self.delete()
            if self.image is candylist[4]:
                if hitox.vhungry != 0:
                    hitox.vhungry -= 2
                    hungyr.text = "How hungry:"+ str(hitox.vhungry)
                elif hitox.vhungry == 0:
                    meal += 2
                    scorer.text = "Candy eat:"+ str(meal)
                self.delete()
            


def spawn_candy():
    w.create_sprite(Candy)
        
Scheduler.update(spawn_candy,2)

level01 = w.create_sprite(Level)
cat = w.create_sprite(Cat)
up = w.create_sprite(TooHightr)
hitox = w.create_sprite(Hitox)



class Life(Label):
    def on_create(self):
        self.font_size = 24
        self.text = "Life Timer:" + str(int(hitox.lifetime))
        self.y = self.content_height+scorer.content_height
        self.x = 0
        self.layer = 4
        self.color = Color.WHITE
        

life = w.create_label(Life)

class Hungyr(Label):
    global meal
    def on_create(self):
        self.font_size = 24
        self.text = "How hungry:"+ str()
        self.y = self.content_height+scorer.content_height+life.content_height
        self.x = 0
        self.layer = 4
        self.color = Color.WHITE
        self.text = "How hungry:"+ str(hitox.vhungry)

hungyr = w.create_label(Hungyr)

w.run()