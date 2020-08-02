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

class PongBanner(Widget):
    direction = NumericProperty(0)
    def move(self):
        self.pos[0] = self.pos[0] + self.direction

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
        #velocity_x = math.sin(self.anglebullet)
        #velocity_y = math.cos(self.anglebullet)

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
    rotcenter_x = NumericProperty(0)
    rotcenter_y = NumericProperty(0)
    xCurrent = NumericProperty(0)
    angleShark = NumericProperty(0)
    distanceToSpaceship = NumericProperty(0)
    #labelMainText = Property('Hello world')
    labelMainText = ObjectProperty(None, allownone=True)
    labelMainSize = NumericProperty(0)
    labelMainPosition = ObjectProperty(None, allownone=True)

    '''def move(self):
        if self.pos[0]==self.xCurrent:
            return
        else:
            if self.pos[0]>self.xCurrent:
                self.pos[0] = self.pos[0]-2
            else:
                self.pos[0] = self.pos[0]+2'''
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos
    
    def setXPosition(self,xpos,ypos):
        self.pos[0]=xpos
        self.pos[1]=200

class PongMissile(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    rotcenter_x = NumericProperty(0)
    rotcenter_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    angleMissile = NumericProperty(225)
    activeStatus = NumericProperty(0)
    startPosMissile = (0,0)
    endPosMissile = (0,0)
    distanceToAlienship = NumericProperty(0)
    distanceToPlanet = NumericProperty(0) 
    distanceToSpaceship = NumericProperty(0) 
    distanceToAlienship = NumericProperty(0)
    collisionPlanet = NumericProperty(0)
    collisionAlienship = NumericProperty(0)
    collisionSpaceship = NumericProperty(0)

    def move(self):
        if self.activeStatus == 1:
            self.pos = Vector(*self.velocity) + self.pos
        else:
            return

    def computeAngle(self):
        a,b,c,d = self.startPosMissile[0],self.startPosMissile[1],self.endPosMissile[0],self.endPosMissile[1]
        print("abcd",a,b,c,d)
        numx = self.endPosMissile[1]-self.startPosMissile[1]
        denomx = self.endPosMissile[0]-self.startPosMissile[0]
        if numx==0:
            self.velocity_y = 2
        elif denomx==0:
            self.velocity_y = 0 
        else:
            xfac=4/numx
            ydiff=int(xfac*denomx)
            if ydiff<0:
                ydiff*=-1
            self.velocity_y = ydiff
            if xfac>0:
                self.velocity_x = 4
            else:
                self.velocity_x = -4
        
'''
    def computeBulletAngle(self):
        #theta = math.atan((self.trajectoryEnd[1]-self.trajectoryStart[1])/(self.trajectoryEnd[0]-self.trajectoryStart[0]))
        pointStart = self.trajectory[0]
        pointEnd = self.trajectory[1]
        theta = math.atan((pointStart[1]-pointEnd[1])/(pointStart[0]-pointEnd[0]))
        if theta<0:
            actualDegree = math.degrees(theta)+180
        else:
            actualDegree = math.degrees(theta)
        #return self.getNearestAngle(actualDegree)
        nearest = self.getNearestAngle(actualDegree)
        #print("theta/actualDegree/nearestDegree",theta,actualDegree,nearest)
        return nearest

    def computeAnglexaxis(self,a,b,c,d):
        theta = math.atan((b-d)/(a-c))
        actualDegree = math.degrees(theta)        
        return self.getNearestAngle(actualDegree)
'''

class PongFire(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        if self.pos[0]!=-100 and self.pos[1]!=-100:
            self.pos = Vector(*self.velocity) + self.pos

class PongExplosion(Widget):
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
    explosion9 = ObjectProperty(None)
    banner10 = ObjectProperty(None)
    debugstring = ObjectProperty(None, allownone=True)
    labelSize = 16

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

    def soundCrash(self): 
        if self.s_crash: 
            self.s_crash.play()

    def soundJump(self): 
        if self.s_jump: 
            self.s_jump.play()

    def soundMissileLaunch(self): 
        if self.s_missileLaunch: 
            self.s_missileLaunch.play()

    def loadAllSounds(self):
        #self.s_clear = SoundLoader.load('assets/sounds/stageClear.wav') 
        self.s_confuse = SoundLoader.load('assets/sounds/confuse.wav') 
        self.s_lose = SoundLoader.load('assets/sounds/lose.wav') 
        self.s_coin = SoundLoader.load('assets/sounds/coin.wav') 
        self.s_fire = SoundLoader.load('assets/sounds/fire.wav') 
        self.s_bump = SoundLoader.load('assets/sounds/bump.wav') 
        self.s_jump = SoundLoader.load('assets/sounds/jump.wav')
        self.s_crash = SoundLoader.load('assets/sounds/crash.wav') 
        self.s_missileLaunch = SoundLoader.load('assets/sounds/missile.wav') 

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket-15)%360
        elif keycode[1] == 'right':
            self.spaceship2.anglerocket = (self.spaceship2.anglerocket+15)%360
        elif keycode[1] == 'spacebar':
            self.shoot_bullet()
        elif keycode[1] == "up":
            self.assignVelocityElement("rocket")
        elif keycode[1] == "e":
            App.get_running_app().stop()
        return True

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
            self.fire6.velocity = self.alienship3.velocity
        elif id=="spaceship":
            self.fire6.pos = self.spaceship2.pos
            self.fire6.velocity = self.spaceship2.velocity           
            #self.fire6.velocity = self.alienship3.velocity

    def missileExplode(self,id):
        self.soundConfuse()
        if id=="planet":
            self.explosion9.pos = self.ball1.pos
            self.explosion9.velocity = self.ball1.velocity
        elif id == "alienship":
            self.explosion9.pos = self.alienship3.pos
            self.explosion9.velocity = self.alienship3.velocity

    def releaseShark(self):
        self.shark7.pos[0]=100
        self.shark7.pos[1]=105
        self.shark7.velocity = (1, 1)
        self.shark7.angleshark = 0
        self.shark7.labelMainSize = 40
        self.shark7.labelMainPosition = 30
        self.shark7.labelMainText = "Bad Planet!"

    def assignVelocityElement(self,element):
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
        if element=="rocket":
            self.spaceship2.velocity = self.dictx[self.spaceship2.anglerocket]
        elif element=="missile":
            self.missile8.velocity = self.dictx[(self.missile8.angleMissile+90)%360]
        elif element=="bullet":
            self.bullet4.velocity = self.dictx[self.bullet4.anglebullet]
        #self.spaceship2.velocity = (self.dictx[self.spaceship2.anglerocket][0],self.dictx[self.spaceship2.anglerocket][0])
        #self.soundBump()
        '''disp = self.dictx[self.ball2.anglerocket]
        self.ball2.pos[0] = self.ball2.pos[0] + disp[0]
        self.ball2.pos[1] = self.ball2.pos[1] - disp[1]'''

    def shoot_bullet(self, vel=(-1, 2)):
        self.soundBump()
        self.bullet4.center = self.spaceship2.center
        #self.bullet4.velocity = vel
        self.bullet4.anglebullet = self.spaceship2.anglerocket
        self.assignVelocityElement("bullet")

    def fireMissile(self):
        self.soundMissileLaunch()
        self.missile8.center = self.shark7.center
        self.missile8.pos[1] = 200

    def start_alienship(self, vel=(2, 3)):
        self.alienship3.center = self.center
        self.alienship3.velocity = vel

    def start_explosion(self, vel = (0,0)):
        self.explosion9.pos = (-100,-100)
        self.explosion9.velocity = vel    

    def showBanner(self):
        #self.banner10.pos = (300,300)
        self.banner10.velocity = 1    

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

        self.missile8.distanceToPlanet = self.eucDistance(self.missile8.center[0],self.missile8.center[1],self.ball1.center[0],self.ball1.center[1])
        if self.missile8.collisionPlanet>0:
            self.missile8.collisionPlanet-=1
            if self.missile8.collisionPlanet==0:
                self.explosion9.pos=(-100,-100)

        self.missile8.distanceToSpaceship = self.eucDistance(self.missile8.center[0],self.missile8.center[1],self.spaceship2.center[0],self.spaceship2.center[1])
        if self.missile8.collisionSpaceship>0:
            self.missile8.collisionSpaceship-=1
        
        self.missile8.distanceToAlienship = self.eucDistance(self.missile8.center[0],self.missile8.center[1],self.alienship3.center[0],self.alienship3.center[1])
        if self.missile8.collisionAlienship>0:
            self.missile8.collisionAlienship-=1
            if self.missile8.collisionAlienship==0:
                self.explosion9.pos=(-100,-100)


        #ninjaDistance = self.eucDistance(self.shark7.pos[0],self.shark7.pos[1],self.spaceship2.pos[0],self.spaceship2.pos[1])

        #print("self.bomb3.distanceToSpaceship",self.bomb3.distanceToSpaceship)

    def update(self, dt):
        self.ball1.move()
        self.spaceship2.move()
        self.alienship3.move()
        self.bullet4.move()
        self.fire6.move()
        self.explosion9.move()
        self.banner10.move()
        #self.shark7.move()
        self.missile8.move()
        self.collisionEngine()
        self.alienship3.angleenemy = (self.alienship3.angleenemy+1)%360        

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

        #handling the missile 
        if self.missile8.activeStatus==1:
            if (self.missile8.y < self.y-200) or (self.missile8.top > self.top):
                self.missile8.activeStatus = 0
                self.missile8.x = -100
                self.missile8.y = -100
            if (self.missile8.x < self.x) or (self.missile8.x > self.width-200):
                self.missile8.activeStatus = 0
                self.missile8.x = -100
                self.missile8.y = -100
            if self.missile8.distanceToPlanet<100 and self.missile8.collisionPlanet==0:
                self.missile8.collisionPlanet=60
                self.missileExplode("planet")
                self.spaceship2.score+=10
            if self.missile8.distanceToSpaceship<100 and self.missile8.collisionSpaceship==0:
                self.soundCrash()
                self.spaceship2.velocity_y *= -1
                self.spaceship2.velocity_x *= -1
                self.missile8.collisionSpaceship=60
                self.spaceship2.health-=10
            if self.missile8.distanceToAlienship<100 and self.missile8.collisionAlienship==0:
                self.missile8.collisionAlienship=60
                self.alienship3.velocity_y *= -1
                self.alienship3.velocity_x *= -1
                self.missileExplode("alienship")
                self.spaceship2.score+=5

            if self.spaceship2.health<=0:
                self.debugstring = "GAME OVER. You scored " + str(self.spaceship2.score)
                self.labelSize = 30
            else:
                self.debugstring = "SCORE : "+ str(self.spaceship2.score)+" / HEALTH : " + str(self.spaceship2.health)

        #the badPlanet banner
        if self.banner10.x==0 or self.banner10.x > self.width-200:
            self.banner10.direction*-1

    def on_touch_down(self, touch):
        #self.debugstring = str(self.missile8.startPosMissile)+str(self.missile8.endPosMissile)
        #self.debugstring = str(int(touch.x))+", "+str(int(touch.y))+", /ironmanpos="+str(self.shark7.pos)
        # + " /Angle = " + str(self.missile8.angleMissile)
        if touch.sy>0.2:
            if touch.sx < 0.4:
                self.spaceship2.anglerocket = (self.spaceship2.anglerocket+15)%360
            elif touch.sx > 0.6:
                self.spaceship2.anglerocket = (self.spaceship2.anglerocket-15)%360
            elif touch.sx >= 0.4 and touch.sx <= 0.6:
                self.shoot_bullet()
        else:
            if touch.sx < 0.4:
                self.missile8.angleMissile=(self.missile8.angleMissile+15)%360
            elif touch.sx > 0.6:
                self.missile8.angleMissile=(self.missile8.angleMissile-15)%360
            self.assignVelocityElement("missile")
            self.missile8.activeStatus=1
            self.fireMissile()

    def on_touch_move(self, touch):
        #self.debugstring = str("angle: ")+ str(touch)
        #print('The touch is', touch)
        self.shark7.center[0] = touch.x

    #def on_touch_up(self, touch):
        #self.fireMissile()
        #self.debugstring = str(int(touch.x))+","+str(int(touch.y)) 
        #+ " / Angle = " + str(self.missile8.angleMissile)
        #self.debugstring = str(self.missile8.startPosMissile)+str(self.missile8.endPosMissile)
        #self.missile8.endPosMissile = (int(touch.sx),int(touch.sy))
        #self.missile8.computeAngle()
        #self.assignVelocityElement("missile")
        #self.missile8.activeStatus = 1
        
class BadPlanetApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")
        self.game = BadPlanetGame()
        self.game.loadAllSounds()
        self.game.serve_ball()
        self.game.start_alienship()
        self.game.showBanner()
        self.game.start_rocket()
        self.game.start_explosion()
        self.game.debugstring = "Welcome to BadPlanet!!"
        widths = [250,250,250,250]
        #self.game.releaseShark()
        Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        #main_layout = BoxLayout(orientation="vertical")
        main_layout.add_widget(self.game)
        buttons = ["angle-15","angle+15","End","Move"]
        wh_layout = GridLayout(cols=4, row_force_default=True, row_default_height=100, pos_hint={'center_y':.5}, size_hint=(1, None))            
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
        if button_text == "angle-15":
            self.game.missile8.angleMissile=(self.game.missile8.angleMissile+15)%360
            self.game.shark7.angleShark = self.game.missile8.angleMissile
        elif button_text == "End":
            #App.get_running_app().stop()
            self.game.spaceship2.health=0
        elif button_text == "Move":
            self.game.assignVelocityElement("rocket")
        elif button_text == "angle+15":
            self.game.missile8.angleMissile=(self.game.missile8.angleMissile-15)%360
            self.game.shark7.angleShark = self.game.missile8.angleMissile

    def on_touch_down(self, touch):
        self.game.debugstring = touch
        print("touched",touch)


if __name__ == '__main__':
    BadPlanetApp().run()
