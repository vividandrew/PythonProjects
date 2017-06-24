import noise, pygame, sys, math, random
from pygame.locals import *

windowWidth = 400
windowHeight = 400
xOffset = 0
yOffset = 0
zOffset = 0
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (70, 70, 255)
scale = 20
counter = 1
maxParticle = 200
FlowField = [0 for i in range(0, windowWidth/scale+1)]
particles = [maxParticle]
last_fps = 0
dblbuff = [pygame.Surface((windowWidth, windowHeight)), pygame.Surface((windowWidth, windowHeight))]     #Creates the two surfaces for double buffer
buff = 0



pygame.init()
# The overlay is to give some alpha to the ellipses drawn on the screen
windowOverlay = pygame.Surface((windowWidth, windowHeight), pygame.SRCALPHA)
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
# This sets the alpha and the colour which is white, making the screen lighter,
# Which sets the ellipses to go lighter as time goes
windowOverlay.fill((255, 255, 255, 2))
mainClock = pygame.time.Clock()

for x in range(0,windowWidth/scale+1):
    FlowField[x] = [0 for i in range(0, windowHeight/scale+1)]

for x in range(0, windowWidth/scale+1):
    for y in range(0, windowWidth/scale+1):
        FlowField[x][y] = [0 for i in range(0, 1)]


# This is each particle object which controls a lot of how it is posistion, speed and colour
class Particle():
    def __init__(self):
        self.pos = [random.randint(0, windowWidth), random.randint(0, windowHeight)]
        self.prevPos = self.pos
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.width = 4
        self.height = 4
        self.maxVel = 1
        self.mag = 0.05  # This controls how strong the acc has over the velocity. (acc is controlled by the FlowField)
                        # The weaker the mag the more curvy the particle will be, but required to decrease maxVel or it can get out of control
        self.colour = (BLACK)
        self.rect = pygame.Rect(self.pos, (self.width, self.height))

        self.Surf = pygame.Surface((self.width,self.height))
        self.Surf.set_alpha(5)

        self.buff = buff

    # this changes the position of the object, called every frame
    def update(self):
        #print self.vel
        self.vel[0] += self.acc[0]
        #limits the speed of the particle, stopping it from going too fast.
        if self.vel[0] > self.maxVel:
            self.vel[0] = self.maxVel
        if self.vel[0] < -self.maxVel:
            self.vel[0] = -self.maxVel

        self.vel[1] += self.acc[1]
        if self.vel[1] > self.maxVel:
            self.vel[1] = self.maxVel
            self.vel[1] += self.acc[1]
        if self.vel[1] < -self.maxVel:
            self.vel[1] = -self.maxVel
        self.__setPreviousPos(self.pos[0], self.pos[1])
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        self.acc[0] *= 0
        self.acc[1] *= 0

    def __setPreviousPos(self, x, y):
        self.prevPos = [x, y]
        #This was to get the previous posistion only controlled within the object.
        #this was to combat skipped pixels

    def applyForce(self, force):
        #print force
        self.acc[0] = force[0]/scale * self.mag
        self.acc[1] = force[1]/scale * self.mag
        #print self.acc



    def show(self, buff):
        #pygame.draw.ellipse(windowSurface, self.colour, self.rect)
        buff.blit(self.Surf,self.pos)
        #The line was to help with frame skipped pixels, but never gets that bad
        #pygame.draw.line(windowSurface, self.colour, self.pos, self.prevPos, self.width*3)

    def edge(self):
        if self.pos[0] < 0 - 10:
            self.pos[0] = windowWidth
            self.__setPreviousPos(self.pos[0],self.pos[1])
        if self.pos[0] > windowWidth + 10:
            self.pos[0] = 0
            self.__setPreviousPos(self.pos[0], self.pos[1])

        if self.pos[1] < 0 - 10:
            self.pos[1] = windowHeight
            self.__setPreviousPos(self.pos[0], self.pos[1])
        if self.pos[1] > windowHeight + 10:
            self.pos[1] = 0
            self.__setPreviousPos(self.pos[0], self.pos[1])

    def follow(self, FlowField):
        x = int(self.pos[0]/scale)
        y = int(self.pos[1]/scale)

        force = 0, 0
        for w in range(0, windowWidth/scale+1):
            for h in range(0, windowHeight/scale+1):
                if x == w and y == h:
                    force = FlowField[w][h]
                    self.applyForce(force)
        #print force

particles[0] = Particle()
for i in range(0, maxParticle-1):
    particles.append(Particle())

windowSurface.fill(WHITE)
dblbuff[0].fill(WHITE)
dblbuff[1].fill(WHITE)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    #windowSurface.fill(WHITE)
    counter += 1
    if counter > 0:
        #windowSurface.fill((25,25,255))
        xOffset = 3540
        for x in range(0, windowWidth/scale+1):
            yOffset = 1348
            for y in range(0, windowHeight/scale+1):
                r = noise.pnoise3(xOffset, yOffset, zOffset)
                #print r
                r *= 360
                #print(r)
                originx = x * scale
                originy = y * scale
                lx = originx + math.cos(math.radians(r)) * scale
                ly = originy + math.sin(math.radians(r)) * scale
                fx = math.cos(math.radians(r)) * scale
                fy = math.sin(math.radians(r)) * scale

                FlowField[x][y] = fx, fy

                #pygame.draw.line(windowSurface, BLUE, (originx, originy), (lx, ly), 1)
                yOffset += 0.2
            xOffset += 0.2
        zOffset += 0.001
        #counter = 0

    #Switches between the surface its displayed to
    if buff == 0:
        buff = 1
    else:
        buff = 0

    for x in range(0, len(particles)):
        particles[x].edge()
        particles[x].show(dblbuff[buff])        #Calls for a surface to draw the objects to.
        particles[x].update()
        particles[x].follow(FlowField)

    windowSurface.blit(dblbuff[buff], (0, 0))

    pygame.display.update()
    mainClock.tick()

    #This is commented out because its not needed, but it measures the fps
    if pygame.time.get_ticks() - last_fps > 1000:
        print "FPS: ", mainClock.get_fps()
        last_fps = pygame.time.get_ticks()