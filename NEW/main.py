import pygame
import sys
from os import path

# import all details from other files without having to specify the originating file every time
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        # initialises the game window
        pygame.init()
        pygame.mixer.init() # initialise sound
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    # loads in the text file
    def load_data(self):
        game_folder = path.dirname(__file__) # sets the map data
        img_folder = path.join(game_folder, '_Game Art')
        self.map = Map(path.join(game_folder, 'map2.txt'))
        self.player_img = pygame.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()


    def new(self):
        # creates all objects
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.run() # game runs every time it is called

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit():
        pygame.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()
            
            # key events for WASD and arrow keys
            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_LEFT or event.key == pygame.K_a:
            #         self.player.move(dx=-1)
            #     if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
            #         self.player.move(dx=1)
            #     if event.key == pygame.K_UP or event.key == pygame.K_w:
            #         self.player.move(dy=-1)
            #     if event.key == pygame.K_DOWN or event.key == pygame.K_s:
            #         self.player.move(dy=1)


    # draws the grey lines to show the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (0, y), (WIDTH, y))
        
    def draw(self):
        self.screen.fill(BGCOLOUR)
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        pygame.display.flip()
        
    def show_start_screen(self):
        pass

    def show_gameover_screen(self):
        pass

game = Game()
game.show_start_screen()
while True:
    game.new()
    game.show_gameover_screen()
