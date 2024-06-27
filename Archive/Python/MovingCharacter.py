import pygame
import random
import datetime
import thorpy

scoreObj = 0
scoreCoin = 0

# Sets all the colours
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

pygame.init()

size = (800, 600)
screen = pygame.display.set_mode(size)

thorpy.init(screen, thorpy.theme_human)

pygame.display.set_caption("Escapism")

done = False
clock = pygame.time.Clock()

# Sets the font that all text items use
font = pygame.font.SysFont(None, 20)

# Sets an easy function to draw text quickly
def drawText(text, font, colour, surface, x, y):
    textobj = font.render(text, 1, colour)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Create player class
class Player(pygame.sprite.Sprite):
    def __init__(self, plX, plY):
        super().__init__()
        # Loads player to display as art loaded
        self.image = pygame.image.load("Python/GameArt/PlayerAlt.png")
        self.rect = self.image.get_rect()
        self.rect.x = plX
        self.rect.y = plY
        self.speedX = 0
        self.speedY = 0

    # Ensures that the player does not go off the end
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
        
    # Getter and setter methods
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
    

class Coin(pygame.sprite.Sprite):
    def __init__(self, obX, obY):
        super().__init__()
        self.image = pygame.Surface([10, 10])
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.x = obX
        self.rect.y = obY

    def update(self):
        # Draws a circle on the screen
        if msElapsed % 1000 > 0 and msElapsed % 1000 < 250:
            pygame.draw.circle(screen, YELLOW, (self.rect.x + 5, self.rect.y + 5), 5)
        if msElapsed % 1000 >= 250 and msElapsed % 1000 < 500:
            pygame.draw.circle(screen, YELLOW, (self.rect.x + 5, self.rect.y + 5), 4)
        if msElapsed % 1000 >= 500 and msElapsed % 1000 < 750:
            pygame.draw.circle(screen, YELLOW, (self.rect.x + 5, self.rect.y + 5), 3)
        if msElapsed % 1000 >= 750:
            pygame.draw.circle(screen, YELLOW, (self.rect.x + 5, self.rect.y + 5), 4)

# Creates sprite groups to control at once
sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()
coins = pygame.sprite.Group()

# Creates instances of classes and adds them to groups
player = Player(0, 0)
sprites.add(player)
# Puts the box in a random location within range
smallBox = Object(random.randint(20, 760), random.randint(20, 560))
objects.add(smallBox)
for _ in range(0, 30):
    coin = Coin(random.randint(20, 760), random.randint(20, 560))
    coins.add(coin)
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
            elif event.key == pygame.K_a:
                alert = thorpy.Alert("Congratulations", "That was a nice click.\nNo, really, you performed well.")
                alert.generate_shadow(fast=False)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.setSpeedX(0)
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player.setSpeedY(0)

    screen.fill(GREY)

    # Calculates time since game started
    msElapsed = pygame.time.get_ticks()
    secondsElapsed = msElapsed // 1000
    # Displays time elapsed in the top corner
    if secondsElapsed >= 30:
        drawText("TIME'S UP!", font, BLACK, screen, 10, 10)
        done = True
    # Changes colour of numbers (between red and black) in top corner indicating time elapsed
    elif secondsElapsed >= 25:
        if secondsElapsed % 2 == 0:
            drawText(str(secondsElapsed), font, RED, screen, 10, 10)
            pygame.draw.rect(screen, RED, [0, 0, 800*((30000-msElapsed) / 30000), 5], 0)
        else:
            drawText(str(secondsElapsed), font, WHITE, screen, 10, 10)
            pygame.draw.rect(screen, WHITE, [0, 0, 800*((30000-msElapsed) / 30000), 5], 0)
    else:
        drawText(str(secondsElapsed), font, BLACK, screen, 10, 10)
        pygame.draw.rect(screen, GREEN, [0, 0, 800*((30000-msElapsed) / 30000), 5], 0)



    sprites.draw(screen)
    objects.draw(screen)
    coins.draw(screen)
    sprites.update()
    objects.update()
    coins.update()
    # objects.add(anotherBox)

    # Checks collisions between sprites and objects, and then removes the objects
    for allsprites in sprites:
        hitObj = pygame.sprite.spritecollide(allsprites, objects, True)
        hitCoin = pygame.sprite.spritecollide(allsprites, coins, True)
        if hitObj:
            scoreObj += 1
            print("OBJECT HIT: " + str(scoreObj))
        if hitCoin:
            scoreCoin += 1
            print("COIN COLLECTED: " + str(scoreCoin))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"{timestamp}.txt"
with open(filename, 'w') as file:
    file.write(f'{msElapsed}\n')
