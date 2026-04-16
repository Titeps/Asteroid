from random import randint

from if3_game.engine import Sprite, init, Game, Layer 

from version_invincibilité import Spaceship, Asteroid, RESOLUTION, Bullet

init(RESOLUTION, "Gne 😎")

main_layer = Layer()
spaceship = Spaceship((1000,450),3)
bg = Sprite("assets/purplish_galaxy.jpg")
main_layer.add(bg)
main_layer.add(spaceship)



for _ in range(3):
    x = randint(64,1936)
    y = randint(64,836)
    while x > 186 and x < 614 and  y > 136 and y < 464 : 
        x = randint(64,736)
        y = randint(64,536)
        
    speed = randint(-50,50),randint(-50,50)
    
    asteroid_position = (x,y)
    rotation_speed = randint(-20,20)
    asteroid = Asteroid(asteroid_position,speed,rotation_speed)

    asteroid.rotation = 33
    main_layer.add(asteroid)




game = Game()

game.add(main_layer)

game.debug = True

game.run()

