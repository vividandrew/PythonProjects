import pygame, random, sys, time
from pygame.locals import *

#Set some constants
windowWidth = 1920
windowHeight = 1080
MaxRain = 2000
#N/A: FPSLimit = 60
rainDrops = []
fallSpeed = 0.7
wind_offset = random.randint(-1, 1)
counter = 0

#getting graphic image of a Sillohouet of a male, to following the darkish kind of background
Char = pygame.image.load('ManSil.png')
CharRect = pygame.Rect(windowWidth/3-200, windowHeight/2-300,400,1099)


#Initialize pygame and other necesary items
pygame.init()
pygame.display.set_caption("Raining Simulation")
mainClock = pygame.time.Clock()
windowDisplay = pygame.display.set_mode((windowWidth, windowHeight))
pygame.mixer.music.load('Background.mp3')
pygame.mixer.music.play(-1, 0.0)

#Set up rain objects
for i in range(MaxRain):
    z = random.randint(3, 10)
    rain = {'z': z, 'rect': pygame.Rect(random.randint(-1* (windowWidth/3), windowWidth+ (windowWidth/3)), 
                                                                random.randint(-1 * windowHeight, 0), z*0.2, z*3)}
    rainDrops.append(rain)

#Set up colours needed
rainColour = (55, 0, 255)
BackgroundColour = (10, 0, 10)

#MainGame loop
while True:
    
    #used later to find the difference in time length.
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

    #Set graphic in the background (ORIGIN, comment line 68, 71, 72, 73 and uncomment line 67 for better performance if thats an issue.)
    #windowDisplay.blit(Char, CharRect)
    count = 0
    #Set the rain to fall down and the character in the middle, (The cause of the performance issue.)
    for rain in rainDrops:
        count += 1
        if count == MaxRain/2:
            windowDisplay.blit(Char, CharRect)
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
    # Disabled on my computer, as towards the end after inserting a line of code, too many frames was no longer the issue.
    #must uncomment if resetting the origin back, as it may go too fast.
    #mainClock.tick(FPSLimit)