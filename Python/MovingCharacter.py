import pygame
import random
import time

pygame.init()

# COLORS
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

size = (800, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Escapism")

done = False
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 20)

def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

class Player(pygame.sprite.Sprite):
    def __init__(self, plX, plY):
        super().__init__()
        self.image = pygame.image.load("Python/GameArt/Main.png")
        self.rect = self.image.get_rect()
        self.rect.x = plX
        self.rect.y = plY
        self.speedX = 0
        self.speedY = 0

    def update(self):
        self.rect.x += self.speedX
        self.rect.y += self.speedY
        if self.rect.x > 760:
            self.rect.x = 760
        if self.rect.x < 20:
            self.rect.x = 20
        if self.rect.y > 560:
            self.rect.y = 560
        if self.rect.y < 20:
            self.rect.y = 20
        

    def setSpeedX(self, speed):
        self.speedX = speed

    def setSpeedY(self, speed):
        self.speedY = speed

    def getPlayerX(self):
        return self.rect.x
    
    def getPlayerY(self):
        return self.rect.y

class Object(pygame.sprite.Sprite):
    def __init__(self, obX, obY):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = obX
        self.rect.y = obY

    def getObjectX(self):
        return self.rect.x
    
    def getObjectY(self):
        return self.rect.y      

sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()

player = Player(0, 0)
sprites.add(player)
smallBox = Object(random.randint(20, 760), random.randint(20, 560))
objects.add(smallBox)
# anotherBox = Object(random.randint(20, 760), random.randint(20, 560))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.setSpeedX(-6)
            elif event.key == pygame.K_RIGHT:
                player.setSpeedX(6)
            elif event.key == pygame.K_UP:
                player.setSpeedY(-6)
            elif event.key == pygame.K_DOWN:
                player.setSpeedY(6)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.setSpeedX(0)
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.setSpeedY(0)

    screen.fill(GREY)

    msElapsed = pygame.time.get_ticks()
    secondsElapsed = msElapsed // 1000
    if secondsElapsed >= 10:
        drawText("TIME'S UP!", font, BLACK, screen, 0, 0)
        # done = True
    elif secondsElapsed % 2 == 0:
        drawText(str(secondsElapsed), font, RED, screen, 0, 0)
    else:
        drawText(str(secondsElapsed), font, BLACK, screen, 0, 0)

    sprites.draw(screen)
    objects.draw(screen)
    sprites.update()
    objects.update()
    # objects.add(anotherBox)

    for allsprites in sprites:
        hit = pygame.sprite.spritecollide(allsprites, objects, True)
        if hit:
            print(hit)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
