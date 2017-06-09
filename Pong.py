import pygame, sys, random
from pygame.locals import *


#<editor-fold desc="Essential Variables to run everything.">
# Set constants
windowWidth = 640
windowHeight = 480
mainClock = pygame.time.Clock()
FPSLimit = 60
#CPUdiff = 6

# Set some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# initialize pygame and creating some objects
pygame.init()
windowSurface = pygame.display.set_mode((windowWidth, windowHeight))
pong = pygame.Rect(windowWidth/2-5, windowHeight/2-5, 10, 10)
pongOL = pygame.Rect(windowWidth/2-7, windowHeight/2-7, 14, 14)
lPaddle = pygame.Rect(20, windowHeight/2-25, 10, 50)
rPaddle = pygame.Rect(windowWidth-20, windowHeight/2-25, 10, 50)

#set fonts up
TitleFont = pygame.font.SysFont('Arial', 128)
lFont = pygame.font.SysFont('Arial', 48)
mFont = pygame.font.SysFont('Arial', 24)
sFont = pygame.font.SysFont('Arial', 12)
#</editor-fold>

def Highlight(mouseOut, mouseIn, textRect, x,y, over = False):
    if textRect.collidepoint((x,y)):
        return mouseIn, True
    else:
        return mouseOut, False



# Settings Screen
def settings(diff):
    mouseClicked = False
    mousex = 0
    mousey = 0
    hard = False
    normal = False
    easy = False
    if diff == 9:
        hard = True
    elif diff == 6:
        normal = True
    else:
        easy = True

    # <editor-fold desc="Text boxes">
    TitleText = TitleFont.render('Settings', 48, WHITE)
    TitleRect = TitleText.get_rect()
    TitleRect.centerx = windowWidth / 2
    TitleRect.centery = windowHeight / 5

    mainMenuText = mFont.render('Main menu', 48, WHITE)
    mainMenuRect = mainMenuText.get_rect()
    mainMenuRect.centerx = windowWidth / 2
    mainMenuRect.centery = windowHeight - 50

    easyText = mFont.render("EASY", True, WHITE)
    easyRect = easyText.get_rect()
    easyRect.centerx = windowWidth / 2
    easyRect.centery = windowHeight - windowHeight / 4

    normalText = mFont.render("NORMAL", True, WHITE)
    normalRect = normalText.get_rect()
    normalRect.centerx = windowWidth / 2
    normalRect.centery = windowHeight - windowHeight / 3

    hardText = mFont.render("HARD", True, WHITE)
    hardRect = easyText.get_rect()
    hardRect.centerx = windowWidth / 2
    hardRect.centery = (windowHeight - windowHeight / 3) - 30

    groupTextBoxes = []
    groupTextBoxes.append(
            {
                'name': "Easy",
                'font': easyText,
                'ifin': mFont.render("EASY", True, WHITE, (20, 20, 20)),
                'rect': easyRect,
                'end result': mFont.render("EASY", True, WHITE),
                'checked': easy,
                'difficulty': True,
                'checkbox': pygame.Rect(easyRect.left - 30, easyRect.top, easyRect.height, easyRect.height)
            })
    groupTextBoxes.append(
            {
                'name': "Normal",
                'font': normalText,
                'ifin': mFont.render("NORMAL", True, WHITE, (20, 20, 20)),
                'rect': normalRect,
                'end result': mFont.render("NORMAL", True, WHITE),
                'checked': normal,
                'difficulty': True,
                'checkbox': pygame.Rect(normalRect.left - 30, normalRect.top, normalRect.height, normalRect.height)
            })
    groupTextBoxes.append(
            {
                'name': "Hard",
                'font': hardText,
                'ifin': mFont.render("HARD", True, WHITE, (20, 20, 20)),
                'rect': hardRect,
                'end result': mFont.render("HARD", True, WHITE),
                'checked': hard,
                'difficulty': True,
                'checkbox': pygame.Rect(hardRect.left - 30, hardRect.top, hardRect.height, hardRect.height)
            })
    groupTextBoxes.append(
            {
                'name': "MainMenu",
                'font': mainMenuText,
                'ifin': mFont.render("Main menu", True, WHITE, (20, 20, 20)),
                'rect': mainMenuRect,
                'end result': mFont.render("Main menu", True, WHITE),
                'checked': False,
                'difficulty': False,
                'checkbox': pygame.Rect(hardRect.top, hardRect.left - 30, hardRect.height, hardRect.height),
                'clicked': "mainMenu"
            })
    # </editor-fold>

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu(mousex, mousey)
            if event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            if event.type == MOUSEBUTTONUP:
                mouseClicked = False
            if event.type == MOUSEMOTION:
                mousex = event.pos[0]
                mousey = event.pos[1]
        windowSurface.fill(BLACK)
        windowSurface.blit(TitleText, TitleRect)


        for boxes in groupTextBoxes:
            boxes['end result'], over = Highlight(boxes['font'], boxes['ifin'], boxes['rect'], mousex, mousey)
            if over and mouseClicked and boxes['difficulty']:
                for checkboxes in groupTextBoxes:
                    checkboxes['checked'] = False
                boxes['checked'] = True
            if over and mouseClicked and not boxes['difficulty']:
                if boxes['name'] == 'MainMenu':
                    for name in groupTextBoxes:
                        if name['name'] == 'Easy' and name['checked']:
                            diff = 3
                        if name['name'] == 'Normal' and name['checked']:
                            diff = 6
                        if name['name'] == 'Hard' and name['checked']:
                            diff = 9
                    mainMenu(mousex, mousey, diff)

            windowSurface.blit(boxes['end result'], boxes['rect'])
            if boxes['checked'] and boxes['difficulty']:
                pygame.draw.rect(windowSurface, WHITE, boxes['checkbox'])
            elif boxes['difficulty']:
                pygame.draw.rect(windowSurface, (30, 30, 30), boxes['checkbox'])
        windowSurface.blit(mainMenuText, mainMenuRect)

        pygame.display.update()
        mainClock.tick(FPSLimit)

# Main Game Loop
def playGame(diff):
    # Resets objects
    pong.x = windowWidth / 2 - 5
    pong.y = windowHeight / 2 - 5
    lPaddle.top = windowHeight/2-25
    rPaddle.top = windowHeight/2-25

    # some essential game variables
    cSpeed = diff
    pSpeed = 6
    moveUP = False
    moveDOWN = False
    cScore = 0
    pScore = 0
    pStuck = 0

    # Background Objects
    tBorder = pygame.Rect(0, 0, windowWidth, 4)
    lBorder = pygame.Rect(0, 0, 4, windowHeight)
    rBorder = pygame.Rect(windowWidth - 4, 0, 4, windowHeight)
    bBorder = pygame.Rect(0, windowHeight - 4, windowWidth, 4)
    mLine = pygame.Rect(windowWidth / 2 - 2, 0, 4, windowHeight)
    background = [lBorder, rBorder, tBorder, bBorder, mLine]

    # Pong directions
    pongSpeed = 3
    pongUD = random.randint(-pongSpeed, pongSpeed)
    pongLorR = random.randint(0, 1)

    if pongLorR == 1:
        pongLeft = False
        pongRight = True
    else:
        pongLeft = True
        pongRight = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    mainMenu(CPUdiff=diff)
                if event.key == K_s:
                    moveUP = False
                    moveDOWN = True
                if event.key == K_w:
                    moveDOWN = False
                    moveUP = True
            if event.type == KEYUP:
                if event.key == K_s:
                    moveDOWN = False
                if event.key == K_w:
                    moveUP = False

        # Pong controller
        if lPaddle.colliderect(pong):
            pongLeft = False
            pongRight = True
            if (pong.y + 10) - lPaddle.y <= 15:
                pongUD = pongUD - (((pong.y + 10) - lPaddle.y)*0.5)/2
            if (pong.y + 10) - lPaddle.y >= 35:
                pongUD = pongUD - ((((pong.y + 10) - lPaddle.y)*0.5)-35)/2

        if rPaddle.colliderect(pong):
            pongLeft = True
            pongRight = False
            if (pong.y + 10) - rPaddle.y <= 15:
                pongUD = pongUD - (((pong.y + 10) - rPaddle.y)*0.5)/2
            if (pong.y + 10) - rPaddle.y >= 35:
                pongUD = pongUD - ((((pong.y + 10) - rPaddle.y)*0.5)-35)/2

        if pong.top < 4 + pongSpeed:
            pongUD = -pongUD
        if pong.top > windowHeight - (pong.height + pongSpeed + 4):
            pongUD = -pongUD
        pong.top += int(pongUD)


        if pongLeft:
            pong.left -= pongSpeed
        if pongRight:
            pong.left += pongSpeed

        # Set position of the outline for the pong
        pongOL.left = pong.x - 2
        pongOL.top = pong.y - 2

        # Paddle movement controls
        #if moveUP and lPaddle.centery > 0:
            #lPaddle.top -= pSpeed
        #if moveDOWN and lPaddle.centery < windowHeight:
            #lPaddle.top += pSpeed

        if pong.y - lPaddle.top - 20 < 0:
            lPaddle.top -= cSpeed
        if pong.y - rPaddle.top - 20 > 0:
            lPaddle.top += cSpeed

        if pong.y - rPaddle.top - 20 < 0:
            rPaddle.top -= cSpeed
        if pong.y - rPaddle.top - 20 > 0:
            rPaddle.top += cSpeed

        # Draw background(Border, middle line)
        windowSurface.fill(BLACK)
        for i in background:
            pygame.draw.rect(windowSurface, WHITE, i)

        pygame.draw.rect(windowSurface, WHITE, lPaddle)
        pygame.draw.ellipse(windowSurface, BLACK, pongOL, )
        pygame.draw.ellipse(windowSurface, WHITE, pong)
        pygame.draw.rect(windowSurface, WHITE, rPaddle)

        # Scoreboard system
        if pong.left < -6:
            cScore += 1
            pong.left = windowWidth/2-5
            pong.top = windowHeight/2-5
            pongUD = random.randint(-pongSpeed, pongSpeed)
        if pong.left > windowWidth+16:
            pScore += 1
            pong.left = windowWidth/2-5
            pong.top = windowHeight/2-5
            pongUD = random.randint(-pongSpeed, pongSpeed)

        text = lFont.render(str(pScore) + "         " + str(cScore), True, WHITE)
        scoreBoard = text.get_rect()
        scoreBoard.centery = 50
        scoreBoard.centerx = windowWidth/2

        #testRect = pygame.Rect(0, lPaddle.y, windowWidth/3, 1)
        #pygame.draw.rect(windowSurface,WHITE, testRect)

        windowSurface.blit(text, scoreBoard)

        # End of the loop, updates the rect in the game.
        pygame.display.update()
        mainClock.tick(FPSLimit)

# Main Menu Screen
def mainMenu(mx = 0, my = 0, CPUdiff = 6):
    mouseClicked = False
    mousex = mx
    mousey = my
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEMOTION:
                mousex = event.pos[0]
                mousey = event.pos[1]
            if event.type == MOUSEBUTTONDOWN:
                mouseClicked = True
            if event.type == MOUSEBUTTONUP:
                mouseClicked = False

        # <editor-fold desc="Text boxes">
        titleText = TitleFont.render("PONG", True, WHITE)
        titleRect = titleText.get_rect()
        titleRect.centerx = windowWidth/2
        titleRect.centery = 128

        startText = lFont.render("START", True, WHITE)
        startRect = startText.get_rect()
        startRect.centerx = windowWidth/2
        startRect.centery = windowHeight/2 + 10

        settingText = mFont.render("Settings", True, WHITE)
        settingRect = settingText.get_rect()
        settingRect.centerx = windowWidth/2
        settingRect.centery = windowHeight/2 + 58

        quitText = mFont.render("Quit", True, WHITE)
        quitRect = quitText.get_rect()
        quitRect.centerx = windowWidth/2
        quitRect.centery = windowHeight - windowHeight/3 + 10

        groupTextBoxes = []
        groupTextBoxes.append(
        {
            'font': startText,
            'ifin': lFont.render("START", True, WHITE, (20, 20, 20)),
            'rect': startRect,
            'end result': lFont.render("START", True, WHITE, (20, 20, 20)),
            'clicked': "playGame"
        })
        groupTextBoxes.append(
        {
            'font': settingText,
            'ifin': mFont.render("Settings", True, WHITE, (20, 20, 20)),
            'rect': settingRect,
            'end result': lFont.render("Settings", True, WHITE),
            'clicked': "Settings"
        })
        groupTextBoxes.append(
        {
            'font': quitText,
            'ifin':mFont.render("Quit", True, WHITE, (20, 20, 20)),
            'rect': quitRect,
            'end result': lFont.render("Quit", True, WHITE),
            'clicked': "Quit"
        })
        #</editor-fold>

        for boxes in groupTextBoxes:
            #This returns the font which has a background of (20, 20, 20) indicating it as highlighted. also returns
            #a bool of either True or False, so the right box is clicked for the following if statement
            boxes['end result'], over = Highlight(boxes['font'], boxes['ifin'], boxes['rect'], mousex, mousey)
            if mouseClicked and over:
                if boxes['clicked'] == "playGame":
                    playGame(CPUdiff)
                if boxes['clicked'] == "Settings":
                    settings(CPUdiff)
                if boxes['clicked'] == "Quit":
                    pygame.quit()
                    sys.exit()

        windowSurface.fill(BLACK)

        # Draw text boxes.
        windowSurface.blit(titleText, titleRect)
        for boxes in groupTextBoxes:
            windowSurface.blit(boxes['end result'], boxes['rect'])

        pygame.display.update()
        mainClock.tick(FPSLimit)

mainMenu()
