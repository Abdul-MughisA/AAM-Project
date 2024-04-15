import pygame
import thorpy

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Main Menu")
screen = pygame.display.set_mode((500, 500), 0, 32)
thorpy.init(screen, thorpy.theme_human) #bind screen to gui elements and set theme


font = pygame.font.SysFont(None, 20)
    
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

def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def mainMenu():
    while True:
            screen.fill(MAROON)
            drawText("Main Menu", font, WHITE, screen, 20, 20)
            
            if pygame.time.get_ticks() > 3000:
                thorpy.Alert("Congratulations", "That was a nice click.\nNo, really, you performed well.").launch_alone()

            mx, my = pygame.mouse.get_pos()

            buttonOne = pygame.Rect(50, 100, 200, 50)
            buttonTwo = pygame.Rect(50, 200, 200, 50)
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
            pygame.draw.rect(screen, pressColourTwo, buttonTwo)

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
    while running:
        screen.fill((0, 0, 0))
        drawText("Game in Progress", font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)

def options():
    running = True
    while running:
        screen.fill((0, 0, 0))
        drawText("Options Menu", font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        pygame.display.update()
        mainClock.tick(60)             

mainMenu()
