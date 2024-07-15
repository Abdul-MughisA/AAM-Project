import pygame

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Main Menu")
screen = pygame.display.set_mode((800, 600), 0, 32)

# FONTS
FontSystem10 = pygame.font.SysFont(None, 10)
FontBahnschrift45 = pygame.font.SysFont("Bahnschrift", 45)
FontSystem50 = pygame.font.SysFont(None, 50)

def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
#end def

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
LIME = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SILVER = (192, 192, 192)
GREY = (128, 128, 128)
MAROON = (128, 0, 0)
OLIVE = (128, 128, 0)
GREEN = (0, 128, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)

def mainMenu():
    while True:
            screen.fill(MAROON)
            drawText("Transport for Python", FontBahnschrift45, WHITE, screen, 200, 50)
            
            mx, my = pygame.mouse.get_pos()

            buttonOne = pygame.Rect(210, 200, 400, 100)
            buttonTwo = pygame.Rect(210, 400, 400, 100)
            pressColourOne = RED
            pressColourTwo = RED

            if buttonOne.collidepoint((mx, my)):
                pressColourOne = MAGENTA
                if click:
                    levels()
            if buttonTwo.collidepoint((mx, my)):
                pressColourTwo = MAGENTA
                if click:
                    options()

            pygame.draw.rect(screen, pressColourOne, buttonOne)
            drawText("Play!", FontBahnschrift45, WHITE, screen, 255, 225)
            pygame.draw.rect(screen, pressColourTwo, buttonTwo)
            drawText("Options", FontBahnschrift45, WHITE, screen, 255, 425)
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            pygame.display.update()
            mainClock.tick(60)

def levels():
    while True:
        drawText("Levels", FontBahnschrift45, WHITE, screen, 200, 50)

        mx, my = pygame.mouse.get_pos()
        buttonOne = pygame.Rect(210, 200, 400, 100)
        buttonTwo = pygame.Rect(210, 400, 400, 100)
        pressColourOne = RED
        pressColourTwo = RED

        if buttonOne.collidepoint((mx, my)):
            pressColourOne = MAGENTA
            if click:
                game()
        if buttonTwo.collidepoint((mx, my)):
            pressColourTwo = MAGENTA
            if click:
                game()

        pygame.draw.rect(screen, pressColourOne, buttonOne)
        drawText("Level 1", FontBahnschrift45, WHITE, screen, 255, 225)
        pygame.draw.rect(screen, pressColourTwo, buttonTwo)
        drawText("Level 2", FontBahnschrift45, WHITE, screen, 255, 425)
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        mainClock.tick(60)
#end def

def game():
    running = True
    class Train(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface([50, 50])
            self.image.fill(BLACK)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        #end constructor

        def moveDown(self):
            self.rect.y += 50
        
        def moveUp(self):
            self.rect.y -= 50

        def moveRight(self):
            self.rect.x += 50

        def moveLeft(self):
            self.rect.x -= 50

        def update(self):
            if self.rect.x < 0:
                self.rect.x = 0
            elif self.rect.y < 0:
                self.rect.y = 0
            elif self.rect.x > 750:
                self.rect.x = 750
            elif self.rect.y > 550:
                self.rect.y = 550

    #end class
    trains = pygame.sprite.Group()
    train = Train(0, 0)
    trains.add(train)

    class Tree(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.image = pygame.Surface([50, 50])
            self.image.fill(GREEN)
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        #end constructor

        def highlight(self):
            self.image.fill(OLIVE)
        #end def

        def update(self):
            self.image.fill(GREEN)
            if (self.rect.x % 50 != 0) and (not click):
                if self.rect.x % 50 <= 25:
                    self.rect.x -= self.rect.x % 50
                if self.rect.x % 50 > 25:
                    self.rect.x += (2 - self.rect.y % 50)
                if self.rect.y % 50 <= 25:
                    self.rect.y -= self.rect.y % 50
                if self.rect.y % 50 > 25:
                    self.rect.y += (1 - self.rect.y % 50)
        #end def
    #end class

    trees = pygame.sprite.Group()
    tree1 = Tree(50, 150)
    tree2 = Tree(200, 250)
    trees.add(tree1)
    trees.add(tree2)
    click = False
    while running:
        screen.fill((255, 255, 255))
        drawText("Game in Progress", FontBahnschrift45, MAROON, screen, 20, 20)

        mx, my = pygame.mouse.get_pos()

        for tree in trees:
            if tree.rect.collidepoint(mx, my):
                tree.highlight()
                if click:
                    # tree.kill() # kills the other tree upon hover
                    tree.rect.x = mx - 25
                    tree.rect.y = my - 25
        #next tree

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_DOWN:
                    train.moveDown()
                if event.key == K_UP:
                    train.moveUp()
                if event.key == K_LEFT:
                    train.moveLeft()
                if event.key == K_RIGHT:
                    train.moveRight()
            if event.type == MOUSEBUTTONDOWN:
                click = True
            if event.type == MOUSEBUTTONUP:
                click = False
        trains.draw(screen)
        trains.update()
        trees.draw(screen)
        trees.update()
        pygame.display.update()
        mainClock.tick(60)


def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        drawText("Options Menu", FontBahnschrift45, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)             

game()
