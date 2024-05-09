import pygame
import thorpy

pygame.init()

screen = pygame.display.set_mode((1200, 700))
thorpy.init(screen, thorpy.theme_human)

my_color = ((255,100,100), (150,30,30), "v") #light gray to dark gray vertical gradient
fuel = thorpy.Lifebar("Fuel (click to refuel)",
                  length=400,
                  bck_color=my_color,
                  font_color=(200,)*3,
                  auto_show_percentage=True) #try setting it to True
fuel.center_on(screen)

#we define below a way to refuel the bar
def refuel():
    fuel.set_value(1.)
fuel.children[-1].at_unclick = refuel
fuel.children[-1].hand_cursor = True

def before_gui(): #add here the things to do each frame before blitting gui elements
    screen.fill((200,)*3)
    current = fuel.get_value()
    fuel.set_value(current-0.01)
thorpy.call_before_gui(before_gui) #tells thorpy to call before_gui() before drawing gui.

fuel.get_updater().launch()
pygame.quit()

