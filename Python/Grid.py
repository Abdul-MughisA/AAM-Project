import pygame

mainClock = pygame.time.Clock()
from pygame.locals import *
pygame.init()
pygame.display.set_caption("Grid")
screen = pygame.display.set_mode((100, 100), 0, 16)

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



def game():
    while True:
    
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        pygame.display.update()
        mainClock.tick(60)

