#Python 3.6

import pygame, random, sys, time
from pygame.locals import *

#Set some constants
windowWidth = 600
windowHeight = 600
MaxRain = 1000
FPSLimit = 60
rainDrops = []
fallSpeed = 0.7
wind_offset = random.randint(-1, 1)
counter = 0

#Initialize pygame and other necesary items
pygame.init()
pygame.display.set_caption("Raining Simulation")
mainClock = pygame.time.Clock()
windowDisplay = pygame.display.set_mode((windowWidth, windowHeight))

#Set up rain objects
for i in range(MaxRain):
    z = random.randint(3, 10)
    rain = {'z': z, 'rect': pygame.Rect(random.randint(-1* (windowWidth/3), windowWidth+ (windowWidth/3)), 
                                                                random.randint(-1 * windowHeight, 0), z*0.2, z*3)}
    rainDrops.append(rain)

#Set up colours needed
rainColour = (55, 0, 255)
BackgroundColour = (10, 0, 10)

#Main loop
while True:
    
    #used later to find the difference in time length. to control fps
    start = time.time()
    
    #Checks for selective events to just quit the game.
    for events in pygame.event.get():
        if events.type == QUIT:
            pygame.quit()
            sys.exit()
        if events.type == KEYDOWN:
            if events.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    #Resets the rain back to the top of the screen in a random posistion 
    #as to not have a set screen/image imprinted after watching it so long    
    for rain in rainDrops:
        if rain['rect'].top > windowHeight:
            rain['rect'].top = random.randint(-1 * windowHeight, 0)
            rain['rect'].left = random.randint(-1 * (windowWidth/3), windowWidth+ (windowWidth/3))
            rain['z'] = random.randint(2, 10)
            rain['rect'].width = rain['z']*0.2
            rain['rect'].height = rain['z']*3
    
    #Sets the window background
    windowDisplay.fill(BackgroundColour)
    
    #Set the rain to fall down and the character in the middle, (The cause of the performance issue.)
    for rain in rainDrops:
        rain['rect'].top += fallSpeed*rain['rect'].height
        rain['rect'].left += wind_offset*rain['z']
        pygame.draw.rect(windowDisplay, rainColour, rain['rect'])

    #a little weird clock that eventually changes the wind offset every 10 seconds
    diff = time.time() - start
    counter += diff
    if counter >= 10:
        wind_offset = random.randint(-10, 10) * 0.1
        counter = 0


    pygame.display.update()
    mainClock.tick(FPSLimit)
