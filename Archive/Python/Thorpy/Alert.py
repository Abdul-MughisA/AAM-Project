"""Quick alert pop up example"""

import pygame
import thorpy

pygame.init()

pygame.display.set_caption("Main Menu")
screen = pygame.display.set_mode((500, 500), 0, 32)
thorpy.init(screen, thorpy.theme_human) #bind screen to gui elements and set theme

thorpy.Alert("Congratulations", "That was a nice click.\nNo, really, you performed well.").launch_alone()

pygame.quit()

