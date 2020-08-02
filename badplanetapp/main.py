import math
import os
os.environ['KIVY_AUDIO'] = 'sdl2'
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.lang import Builder

Builder.load_file('BadPlanet.kv')
#declare the planet. Corresponding layout can be found in pong.kv

class PongPlanet(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

#declare the Spaceship, controlled by player
class PongSpaceship(Widget):
    score = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    anglerocket = NumericProperty(0)
    health = NumericProperty(1)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongBullet(Widget):
    anglebullet = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    distanceToPlanet = NumericProperty(0)
    collision = NumericProperty(0)
    collisionAlienship = NumericProperty(0)
    distanceAlienshipToBullet = NumericProperty(0)
    distanceToBullet = NumericProperty(0)

    def move(self):
        #velocity_x = math.ceil(math.degrees(math.sin(self.anglebullet)))
        velocity_x = math.sin(self.anglebullet)
        velocity_y = math.cos(self.anglebullet)

        if self.pos[0]==-100 and self.pos[1]==-100:
            return

        self.dictx = { 
            0: (-6,0),
            15: (-5,1),
            30: (-4,2),
            45: (-3,3),
            60: (-2,4),
            75: (-1,5),
            90: (0,6),
            105: (1,5),
            120: (2,4),
            135: (3,3),
            150: (4,2),
            165: (5,1),
            180: (6,0),
            195: (5,-1),
            210: (4,-2),
            225: (3,-3),
            240: (2,-4),
            255: (1,-5),
            270: (0,-6),
            285: (-1,-5),
            300: (-2,-4),
            315: (-3,-3),
            330: (-4,-2),
            345: (-5,-1),
            360: (-6,0)
        }
        disp = self.dictx[self.anglebullet]
        self.pos[0] = self.pos[0] + 2*disp[0]
        self.pos[1] = self.pos[1] - 2*disp[1]

class PongAlienship(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    anglerocket = NumericProperty(0)
    distanceToSpaceship = NumericProperty(0)
    collision = NumericProperty(0)
    angleenemy = NumericProperty(0)

    def move(self):
        self.pos[0] = self.velocity[0] + self.pos[0]
        self.pos[1] = self.velocity[1] + self.pos[1]
        #self.pos = Vector(*self.velocity) + self.pos

class PongShark(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    rotcenter_x = NumericProperty(0)
    rotcenter_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    angleshark = NumericProperty(0)
    distanceToSpaceship = NumericProperty(0)
    #labelMainText = Property('Hello world')
    labelMainText = ObjectProperty(None, allownone=True)
    labelMainSize = NumericProperty(0)
    labelMainPosition = ObjectProperty(None, allownone=True)

class PongFire(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if self.pos[0]!=-100 and self.pos[1]!=-100:
            self.pos = Vector(*self.velocity) + self.pos

class PongLightning(Widget):
    anglelightning = NumericProperty(0)

class BadPlanetGame(Widget):
    updateCounter = 0
    ball1 = ObjectProperty(None)
    spaceship2 = ObjectProperty(None)
    alienship3 = ObjectProperty(None)
    fire6 = ObjectProperty(None)
    shark7 = ObjectProperty(None)
    debugstring = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super(BadPlanetGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def soundConfuse(self): 
        if self.s_confuse: 
            self.s_confuse.play()

    def soundCoin(self): 
        if self.s_coin: 
            self.s_coin.play()

    def soundLose(self): 
        if self.s_lose: 
            self.s_lose.play()

    def soundFire(self): 
        if self.s_fire: 
            self.s_fire.play()

    def soundBump(self): 
        if self.s_bump: 
            self.s_bump.play()

    def soundJump(self): 
        if self.s_jump: 
            self.s_jump.play()

    def loadAllSounds(self):
        #self.s_clear = SoundLoader.load('assets/sounds/stageClear.wav') 
        self.s_confuse = SoundLoader.load('assets/sounds/confuse.wav') 
        self.s_lose = SoundLoader.load('assets/sounds/lose.wav') 
        self.s_coin = SoundLoader.load('assets/sounds/coin.wav') 
        self.s_fire = SoundLoader.load('assets/sounds/fire.wav') 
        self.s_bump = SoundLoader.load('assets/sounds/bump.wav') 
        self.s_jump = SoundLoader.load('assets/sounds/jump.wav') 

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket+15)%360
        elif keycode[1] == 'right':
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket-15)%360
        elif keycode[1] == 'spacebar':
            self.shoot_bullet()
        elif keycode[1] == "up":
            self.boost_rocket()
        elif keycode[1] == "e":
            App.get_running_app().stop()
        return True

    def moveShark(self,uc):
        xdiff = math.sin(self.shark7.angleshark)
        ydiff = math.cos(self.shark7.angleshark)
        self.shark7.pos[0]=self.shark7.pos[0]+xdiff
        self.shark7.pos[1]=self.shark7.pos[1]+ydiff

    def serve_ball(self, vel=(3, 1)):
        self.ball1.center = (self.center[0]-50,self.center[1]+50)
        self.ball1.velocity = vel

    def start_rocket(self, vel=(-1, 2)):
        #self.soundCoin()
        self.spaceship2.center = self.center
        self.spaceship2.velocity = vel
        self.spaceship2.anglerocket = 270
        self.spaceship2.health = 60

    def strikeLightning(self):
        self.soundLose()
        self.lightning5.pos = self.alienship3.pos
        self.lightning5.anglelightning = self.alienship3.angleenemy

    def hitExplode(self,id):
        self.soundCoin()
        if id=="planet":
            self.fire6.pos = self.ball1.pos
            self.fire6.velocity = self.ball1.velocity
        elif id == "alienship":
            self.fire6.pos = self.alienship3.pos
            #self.fire6.velocity = self.alienship3.velocity

    def releaseShark(self):
        self.shark7.pos[0]=100
        self.shark7.pos[1]=400
        self.shark7.velocity = (1, 1)
        self.shark7.angleshark = 0
        self.shark7.labelMainSize = 40
        self.shark7.labelMainPosition = 30
        self.shark7.labelMainText = "Bad Planet!"

    def boost_rocket(self):
        self.dictx = { 
            0: (-6,0),
            15: (-5,-1),
            30: (-4,-2),
            45: (-3,-3),
            60: (-2,-4),
            75: (-1,-5),
            90: (0,-6),
            105: (1,-5),
            120: (2,-4),
            135: (3,-3),
            150: (4,-2),
            165: (5,-1),
            180: (6,0),
            195: (5,1),
            210: (4,2),
            225: (3,3),
            240: (2,4),
            255: (1,5),
            270: (0,6),
            285: (-1,5),
            300: (-2,4),
            315: (-3,3),
            330: (-4,2),
            345: (-5,1),
            360: (-6,0)
        }
        self.spaceship2.velocity = self.dictx[self.spaceship2.anglerocket]
        #self.spaceship2.velocity = (self.dictx[self.spaceship2.anglerocket][0],self.dictx[self.spaceship2.anglerocket][0])
        #self.soundBump()
        '''disp = self.dictx[self.ball2.anglerocket]
        self.ball2.pos[0] = self.ball2.pos[0] + disp[0]
        self.ball2.pos[1] = self.ball2.pos[1] - disp[1]'''

    def shoot_bullet(self, vel=(-1, 2)):
        self.soundBump()
        self.bullet4.center = self.spaceship2.center
        self.bullet4.velocity = vel
        self.bullet4.anglebullet = self.spaceship2.anglerocket 

    def start_alienship(self, vel=(2, 3)):
        self.alienship3.center = self.center
        self.alienship3.velocity = vel

    def eucDistance(self,p,q,r,s):
        distc = math.sqrt((p-r)*(p-r)+(q-s)*(q-s))
        #print("distc",distc)
        return distc

    def disappearEverything(self):
        self.shark7.pos=(-100,100)
        self.ball1.pos=(-100,100)
        self.spaceship2.pos=(-100,100)
        self.alienship3.pos=(-100,100)

    def collisionEngine(self):
        #compute distance between spaceship and alienship
        enemyDistanceToSpaceship = self.eucDistance(self.spaceship2.pos[0],self.spaceship2.pos[1],self.alienship3.pos[0],self.alienship3.pos[1])
        if enemyDistanceToSpaceship<75 and self.alienship3.collision==0:
            self.alienship3.collision = 60
            self.spaceship2.health-=10
            self.strikeLightning()
            self.alienship3.velocity_x *= -1
            self.alienship3.velocity_y *= -1
            self.spaceship2.velocity_x *= -1
            self.spaceship2.velocity_y *= -1

        if self.alienship3.collision > 0:
            self.alienship3.collision-=1
            if self.alienship3.collision==0:
                self.lightning5.pos=(-100,-100)
                
        #compute distance between bullet and planet
        self.bullet4.distanceToPlanet = self.eucDistance(self.bullet4.center[0],self.bullet4.center[1],self.ball1.center[0],self.ball1.center[1])
        if self.bullet4.collision > 0:
            self.bullet4.collision-=1
            if self.bullet4.collision==0:
                self.fire6.pos=(-100,-100)

        #compute distance between bullet and alienship
        self.bullet4.distanceAlienshipToBullet = self.eucDistance(self.bullet4.center[0],self.bullet4.center[1],self.alienship3.center[0],self.alienship3.center[1])
        if self.bullet4.collisionAlienship > 0:
            self.bullet4.collisionAlienship-=1
            if self.bullet4.collisionAlienship!=0:
                self.alienship3.pos=(-100,-100)
                self.start_alienship()

        #ninjaDistance = self.eucDistance(self.shark7.pos[0],self.shark7.pos[1],self.spaceship2.pos[0],self.spaceship2.pos[1])

        #print("self.bomb3.distanceToSpaceship",self.bomb3.distanceToSpaceship)

    def update(self, dt):
        self.ball1.move()
        self.spaceship2.move()
        self.alienship3.move()
        self.bullet4.move()
        self.fire6.move()
        self.collisionEngine()

        self.alienship3.angleenemy = (self.alienship3.angleenemy+1)%360
        self.updateCounter=self.updateCounter+1
        if self.updateCounter==25:
            self.updateCounter = 0
            self.shark7.angleshark = (self.shark7.angleshark+1)%360 
        self.moveShark(self.updateCounter)
        '''if self.bomb3.collision == 0 and self.bomb3.distanceToSpaceship<30:
            self.bomb3.collision = 60'''
        if self.bullet4.collision == 0 and self.bullet4.distanceToPlanet<100:
            self.hitExplode("planet")
            self.bullet4.collision = 60
            self.spaceship2.score+=10

        if self.bullet4.collisionAlienship == 0 and self.bullet4.distanceAlienshipToBullet<100:
            self.soundCoin()
            #self.hitExplode("alienship")
            self.bullet4.collisionAlienship = 120
            self.spaceship2.score+=5

        # bounce ball off bottom or top
        if (self.ball1.y < self.y) or (self.ball1.top > self.top):
            self.ball1.velocity_y *= -1

        if (self.shark7.y < self.y) or (self.shark7.top > self.top):
            self.shark7.velocity_y *= -1

        '''if (self.ball2.y < self.y) or (self.ball2.top > self.top):
            self.ball2.velocity_y *= -1'''
        
        '''if (self.spaceship2.y < 200):
            self.spaceship2.y = self.top
        if (self.spaceship2.top > self.top-200):
            self.spaceship2.top = 0'''

        if (self.spaceship2.y < self.y):
            self.spaceship2.y = self.top
        if (self.spaceship2.y > self.top):
            self.spaceship2.y = 250

        if self.spaceship2.anglerocket<0:
            self.spaceship2.anglerocket=self.spaceship2.anglerocket+360

        if self.spaceship2.x < self.x:
            self.spaceship2.velocity_x *= -1
        if self.spaceship2.x > self.width-250:
            self.spaceship2.velocity_x *= -1

        #print("ball2y,ball2top,y,top",self.ball2.y,self.ball2.top,self.y,self.top)
            
        if (self.alienship3.y < self.y) or (self.alienship3.top > self.top):
            self.alienship3.velocity_y *= -1

        if self.ball1.x < self.x:
            self.ball1.velocity_x *= -1
        if self.ball1.x > self.width-250:
            self.ball1.velocity_x *= -1

        if self.alienship3.x < self.x:
            self.alienship3.velocity_x *= -1
        if self.alienship3.x > self.width-200:
            self.alienship3.velocity_x *= -1
        if self.spaceship2.health==0:
            self.shark7.labelMainSize = 40
            self.shark7.labelMainPosition = self.center
            self.shark7.labelMainText = "GAME OVER!! \n You Scored "+str(self.spaceship2.score) 
            #self.disappearEverything()
            #App.get_running_app().stop()

    def on_touch_down(self, touch):
        self.debugstring = touch
        if touch.sx < 0.4:
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket+15)%360
        elif touch.sx > 0.6:
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket-15)%360
        elif touch.sx >= 0.4 and touch.sx <= 0.6:
             self.shoot_bullet()

class BadPlanetApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.game = BadPlanetGame()
        self.game.loadAllSounds()
        self.game.serve_ball()
        self.game.start_alienship()
        self.game.start_rocket()
        self.game.debugstring = "no debug!"
        widths = [400,100,400]
        #self.game.releaseShark()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        #main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.game)
        buttons = [ "Fire","End","Move",]
        wh_layout = GridLayout(cols=3, row_force_default=True, row_default_height=100, pos_hint={'center_y':.5}, size_hint=(0.75, None))            
        for label in buttons:
            button = Button(
                text=label,
                width = widths.pop(0),
            )
            button.bind(on_press=self.on_button_press)
            wh_layout.add_widget(button)
        main_layout.add_widget(wh_layout)
        return main_layout

    def on_button_press(self, instance):
        button_text = instance.text
        if button_text == "Fire":
            self.game.soundFire()
            self.game.shoot_bullet()
        elif button_text == "End":
            #App.get_running_app().stop()
            self.game.spaceship2.health=0
        elif button_text == "Move":
            self.game.boost_rocket()

    def on_touch_down(self, touch):
        self.game.debugstring = touch
        print("touched",touch)


if __name__ == '__main__':
    BadPlanetApp().run()
