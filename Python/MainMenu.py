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
    
click = False

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
                    game()
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
            pass

    #end class
    trains = pygame.sprite.Group()
    train = Train(0, 0)
    trains.add(train)
    while running:
        screen.fill((255, 255, 255))
        drawText("Game in Progress", FontBahnschrift45, MAROON, screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                if event.key == K_DOWN:
                    train.moveDown()

        trains.draw(screen)
        trains.update()
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

mainMenu()
