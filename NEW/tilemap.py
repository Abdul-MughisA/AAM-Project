import pygame
from settings import *

class Map:
    def __init__(self, filename):
        self.data = []  # map data stored in this variable
        # copies data from map file into variable
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())
        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        # "move" creates a new rectangle 
        return entity.rect.move(self.camera.topleft)
    
    # adjusting the sprite
    def update(self, target):
        x = -target.rect.x + int(WIDTH/2)
        y = -target.rect.y + int(HEIGHT/2)

        # limit scrolling to map size
        x = min(0, x) # sets x to whichever is smaller
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)
