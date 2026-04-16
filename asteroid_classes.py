from random import randint
from if3_game.engine import Sprite
from pyglet.window import key as keyboard
from math import sin , cos, radians, sqrt

RESOLUTION = (2000,900)

class SpaceObject(Sprite):
   
    def __init__(self, image, position, anchor, speed = (0,0), rotation_speed = 0):
        super().__init__(image, position, anchor= anchor, collision_shape= "circle")
        self.speed = speed
        self.rotation_speed = rotation_speed

    def update(self,dt):
        super().update(dt)
        mvt = (self.speed[0] * dt, self.speed[1] * dt)
        self.position = (self.position[0] + mvt[0], self.position[1] + mvt[1])

        self.rotation += self.rotation_speed * dt # .rotation est défini dans Cocos déjà.
        x,y = self.position
        
        if x < -self.width/2 :
            x = RESOLUTION[0] + self.width / 2 
        elif x > RESOLUTION[0] + self.width/2 :
            x = -self.width/2

        if y < -self.height / 2:
            y = RESOLUTION[1] + self.height / 2
        elif y > RESOLUTION[1] + self.height/2:
            y = - self.height / 2
            
        self.position = x,y



class Asteroid(SpaceObject):
   
    def __init__(self, position, speed, rotation_speed, level = 3):
        self.level = level
        image = "assets/asteroid128.png"
        anchor = (64,64)
        if self.level == 2:
            image = "assets/asteroid64.png"
            anchor = (32,32)
        elif self.level == 1:
            image = "assets/asteroid32.png"
            anchor = (16,16)
        super().__init__(image, position, anchor, speed,rotation_speed)
    
    def on_collision(self, other):
        if isinstance(other,Bullet):
            other.destroy()
            self.destroy()
        elif isinstance(other,Spaceship):
            self.destroy()
            

    def destroy(self):
        super().destroy()
        if self.level > 1:
            for _ in range(3):
                speed = randint(-30,70),randint(-50,50)
                rotation_speed = randint(-20,20)
                asteroid = Asteroid(self.position, speed,rotation_speed,self.level - 1)
                
                self.layer.add(asteroid)
            

class Spaceship(SpaceObject):
    
    def __init__(self, position, lives):
        super().__init__("assets/ship.png",position,(32,64))
        self.engine_on = False
        self.acceleration = 100 
        self.opacity = 200
        self.invicibility = False
        self.chrono = 0
        self.lives = lives
        #self.velocity_max = 100

    def update(self,dt):
        if self.engine_on: #comprends pas pq on précise pas == True
            angle =  radians( - self.rotation + 90) # - sens de rotation bc anticlockwise
            speed_change_x =cos(angle) * self.acceleration * dt
            speed_change_y = sin(angle) * self.acceleration * dt
            self.speed = self.speed[0] + speed_change_x, self.speed[1] + speed_change_y


        if self.invicibility == True:
            self.chrono += dt
            if self.chrono >= 4:
                self.opacity = 255
                self.invicibility = False
                self.chrono = 0

        super().update(dt)

    def on_key_press(self, key, _):
        if key == keyboard.RIGHT:
            self.rotation_speed = 130
        elif key == keyboard.LEFT:
            self.rotation_speed = -130
        if key == keyboard.SPACE:
            self.create_bullet()
         
        if key == keyboard.UP:
            self.engine_on = True

    def on_key_release(self, key, _):
        if key == keyboard.RIGHT or key == keyboard.LEFT:
           self.rotation_speed = 0
        if key == keyboard.UP:
            self.engine_on = False
        
    
    def create_bullet(self):
        angle =  radians( - self.rotation + 90)

        decalage = self.height / 2
        decalage_x = cos(angle) * decalage
        decalage_y = sin(angle) * decalage
        bullet_position = self.position[0] + decalage_x, self.position[1] + decalage_y

        bullet_velocity = 300 + sqrt(self.speed[0]**2 + +self.speed[1]**2)


        speed_x = cos(angle)* bullet_velocity
        speed_y= sin(angle) * bullet_velocity

        speed = speed_x,speed_y
        bullet = Bullet(bullet_position, speed, 4.5)
        self.layer.add(bullet)
        
    def on_collision(self, other):
        if isinstance (other,Asteroid):
            if self.lives > 0 :
                if self.invicibility == False :
                    self.opacity = 125
                    self.invicibility = True
                self.lives -= 1
                
            if self.lives == 0:
                self.destroy()
        
            

class Bullet(SpaceObject):

    def __init__(self, position, speed, life_time):
        super().__init__("assets/bullet.png", position , (8,8),speed)
        self.life_time = life_time
        self.chrono = 0.

    def update(self,dt ):
        super().update(dt)
        self.chrono += dt
        if self.chrono >= self.life_time:
            self.destroy() 



