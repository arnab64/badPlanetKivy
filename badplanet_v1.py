from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.vector import Vector
from kivy.clock import Clock
import pygame as pg
from pygame import mixer
from kivy.core.window import Window
import math
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos

class PongRocket(Widget):
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
    labelMainPosition = NumericProperty(0)

class PongFire(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if self.pos[0]!=-100 and self.pos[1]!=-100:
            self.pos = Vector(*self.velocity) + self.pos

class PongLightning(Widget):
    anglelightning = NumericProperty(0)

class PongGame(Widget):
    updateCounter = 0
    ball1 = ObjectProperty(None)
    spaceship2 = ObjectProperty(None)
    alienship3 = ObjectProperty(None)
    fire6 = ObjectProperty(None)
    shark7 = ObjectProperty(None)
    #rocket = ObjectProperty(None)
    #player1 = ObjectProperty(None)
    #player2 = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(PongGame, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

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

    def soundStage(self):
        mixer.music.load('assets/sounds/stageClear.wav')
        mixer.music.play(0)
        return

    def soundBounce(self):        
        mixer.music.load('assets/sounds/bounce.wav')
        mixer.music.play(0)
        return 

    def soundCoin(self):
        mixer.music.load('assets/sounds/coin.wav')
        mixer.music.play(0)
        return

    def soundBump(self):
        mixer.music.load('assets/sounds/bump.wav')
        mixer.music.play(0)
        return

    def soundLose(self):
        mixer.music.load('assets/sounds/lose.wav')
        mixer.music.play(0)
        return

    def soundStart(self):
        mixer.music.load('assets/sounds/start.wav')
        mixer.music.play(0)
        return
 
    def soundFire(self):
        mixer.music.load('assets/sounds/confuse.wav')
        mixer.music.play(0)
        return        

    def serve_ball(self, vel=(3, 1)):
        self.ball1.center = (self.center[0]-50,self.center[1]+50)
        self.ball1.velocity = vel
        self.soundStage()

    def start_rocket(self, vel=(-1, 2)):
        self.spaceship2.center = self.center
        self.spaceship2.velocity = vel
        self.spaceship2.anglerocket = 315
        self.spaceship2.health = 60

    def strikeLightning(self):
        self.soundLose()
        self.lightning5.pos = self.alienship3.pos
        self.lightning5.anglelightning = self.alienship3.angleenemy

    def hitExplode(self,id):
        self.soundStart()
        if id=="planet":
            self.fire6.pos = self.ball1.pos
            self.fire6.velocity = self.ball1.velocity
        elif id == "alienship":
            self.fire6.pos = self.alienship3.pos
            #self.fire6.velocity = self.alienship3.velocity

    def releaseShark(self):
        self.shark7.pos[0]=350
        self.shark7.pos[1]=250
        self.shark7.velocity = (3, 1)
        self.shark7.angleshark = 0
        self.shark7.labelMainSize = 25
        self.shark7.labelMainPosition = 100
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
        self.soundBump()
        '''disp = self.dictx[self.ball2.anglerocket]
        self.ball2.pos[0] = self.ball2.pos[0] + disp[0]
        self.ball2.pos[1] = self.ball2.pos[1] - disp[1]'''

    def shoot_bullet(self, vel=(-1, 2)):
        self.bullet4.center = self.spaceship2.center
        self.bullet4.velocity = vel
        self.bullet4.anglebullet = self.spaceship2.anglerocket
        self.soundBump()

    def throw_bomb(self, vel=(2, 3)):
        self.alienship3.center = self.center
        self.alienship3.velocity = vel

    def changeAngle(self, mode):
        if mode == 1:
            self.spaceship.anglerocket=180-self.spaceship2.anglerocket

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
        self.bullet4.distanceAlienshipToBullet = self.eucDistance(self.bullet4.pos[0],self.bullet4.pos[1],self.alienship3.pos[0],self.alienship3.pos[1])
        if self.bullet4.collisionAlienship > 0:
            self.bullet4.collisionAlienship-=1
            if self.bullet4.collisionAlienship!=0:
                self.alienship3.pos=(-100,-100)
                self.throw_bomb()

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
        if self.bullet4.collision == 0 and self.bullet4.distanceToPlanet<40:
            self.hitExplode("planet")
            self.bullet4.collision = 60
            self.spaceship2.score+=10

        if self.bullet4.collisionAlienship == 0 and self.bullet4.distanceAlienshipToBullet<30:
            self.soundCoin()
            #self.hitExplode("alienship")
            self.bullet4.collisionAlienship = 125
            self.spaceship2.score+=5

        # bounce ball off bottom or top
        if (self.ball1.y < self.y) or (self.ball1.top > self.top):
            self.ball1.velocity_y *= -1

        if (self.shark7.y < self.y) or (self.shark7.top > self.top):
            self.shark7.velocity_y *= -1

        '''if (self.ball2.y < self.y) or (self.ball2.top > self.top):
            self.ball2.velocity_y *= -1
        '''
        if (self.spaceship2.y < self.y):
            self.spaceship2.top = self.top+100
        if (self.spaceship2.top > self.top):
            self.spaceship2.top = 100
        #print("ball2y,ball2top,y,top",self.ball2.y,self.ball2.top,self.y,self.top)
            
        if (self.alienship3.y < self.y) or (self.alienship3.top > self.top):
            self.alienship3.velocity_y *= -1

        if self.spaceship2.anglerocket<0:
            self.spaceship2.anglerocket=self.spaceship2.anglerocket+360

        if self.spaceship2.x < self.x:
            self.spaceship2.velocity_x *= -1
        if self.spaceship2.x > self.width-100:
            self.spaceship2.velocity_x *= -1

        if self.ball1.x < self.x:
            self.ball1.velocity_x *= -1
        if self.ball1.x > self.width-100:
            self.ball1.velocity_x *= -1

        if self.alienship3.x < self.x:
            self.alienship3.velocity_x *= -1
        if self.alienship3.x > self.width-75:
            self.alienship3.velocity_x *= -1
        if self.spaceship2.health==0:
            self.shark7.labelMainSize = 50
            self.shark7.labelMainPosition = 500
            self.shark7.labelMainText = "GAME OVER!! \n You Scored "+str(self.spaceship2.score) 
            #self.disappearEverything()
            #App.get_running_app().stop()

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongApp(App):
    def build(self):
        pg.init()
        game = PongGame()
        game.start_rocket()
        game.serve_ball()
        game.throw_bomb()
        game.releaseShark()
        Clock.schedule_interval(game.update, 1.0 / 60.0)
        return game

if __name__ == '__main__':
    PongApp().run()
