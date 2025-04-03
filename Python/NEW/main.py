import pygame
import sys
from os import path

# import all details from other files without having to specify the originating file every time
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # initialises the game window
        self.running = True
        self.level = 1
        self.selected_sprite = None
        self.music_on = True
        pygame.init()
        pygame.mixer.init() # initialise sound

        # load music
        music_path = path.join(path.dirname(__file__), 'music.mp3')
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1) # loop infinitely

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100)
        self.load_data()

    # loads in the text file
    def load_data(self):
        game_folder = path.dirname(__file__) # sets the map data
        self.map_data = []  # map data stored in this variable
        # copies data from map file into variable
        map_file = path.join(game_folder, f"map{self.level}.txt")
        with open(map_file, 'rt') as f:
            for line in f:
                self.map_data.append(line)


    def new(self):
        self.level_start_time = pygame.time.get_ticks() # record level start time
        # creates all objects
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.walls = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.grass = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'A':
                    Stone(self, col, row)
                if tile == 'X':
                    Flag(self, col, row)
                if tile == ',':
                    Grass(self, col, row)
                if tile == 'L':
                    Log(self, col, row)
                if tile == 'W':
                    Water(self, col, row)
        self.run() # game runs every time it is called


    def run(self):
        self.clock.tick(FPS)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        self.all_sprites.update()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            
            # selects a sprite
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # cycles through all sprites
                for sprite in self.all_sprites:
                    if sprite.rect.collidepoint(mouse_pos) and getattr(sprite, 'selectable', True):
                        self.selected_sprite = sprite
                        # selects the first sprite in the cycle that happens to be clicked
                        break
            
            # moves the selected sprite
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_settings()
                if hasattr(self, 'selected_sprite') and self.selected_sprite is not None:
                    # key events for WASD and arrow keys
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.selected_sprite.move(dx=-1)
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.selected_sprite.move(dx=1)
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.selected_sprite.move(dy=-1)
                    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.selected_sprite.move(dy=1)


    # draws the grey lines to show the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (0, y), (WIDTH, y))
        
    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.all_sprites.draw(self.screen)

        # Draw level label
        self.draw_text("Level: " + str(self.level), 22, WHITE, 50, 10)

        # Calculate and display time elapsed with every level
        elapsed_ms = pygame.time.get_ticks() - self.level_start_time
        self.draw_text("Time: " + str(elapsed_ms) + "ms", 22, WHITE, 300, 10)

        # Calculate and display score based on time
        level_score = round(100000/(elapsed_ms/1000 + 20) + 100)
        self.draw_text("Score: " + str(level_score), 22, WHITE, 550, 10)

        if self.selected_sprite is not None:
            overlay = pygame.Surface((self.selected_sprite.rect.width, self.selected_sprite.rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, self.selected_sprite.rect)
        pygame.display.flip()
    
    def wait_for_click(self, button_rect):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        return True

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    self.running = False
                    return False
                if event.type == pygame.KEYDOWN:
                    return True
    
    def draw_text(self, text, size, colour, x, y):
        font = pygame.font.Font(pygame.font.match_font('arial'), size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    def show_start_screen(self):
        # draw the original play button
        play_button = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 2, 100, 50)
        while True:
            self.screen.fill(BLACK)
            self.draw_text(TITLE, 30, WHITE, WIDTH / 2, HEIGHT / 2 - 50)

            # determine mouse position
            mous_pos = pygame.mouse.get_pos()
            if play_button.collidepoint(mous_pos):
                # draws the box grey if the mouse is over it
                pygame.draw.rect(self.screen, GREY, play_button)
            else:
                # but draws a white box if not
                pygame.draw.rect(self.screen, WHITE, play_button)

            self.draw_text("Play", 22, BLACK, WIDTH / 2, HEIGHT / 2 + 10)
            pygame.display.flip()

            # this loop waits for the user to click the play button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        return True
            self.clock.tick(FPS)

    def show_gameover_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        return self.wait_for_key()
    
    def show_congrats_screen(self, score, elapsed_ms):
        self.screen.fill(BLACK)
        self.draw_text("Congratulations!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("You completed the level!", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Your score: " + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.draw_text("Time taken: " + str(elapsed_ms//1000) + "s", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        pygame.display.flip()
        return self.wait_for_key()
    
    def pause_settings(self):
        # Record when pause begins so we can adjust elapsed time later
        pause_start = pygame.time.get_ticks()
        paused = True
        while paused:
            self.clock.tick(FPS)
            self.screen.fill(BLACK)
            # Display a combined pause/settings menu
            self.draw_text("PAUSED / SETTINGS", 48, WHITE, WIDTH / 2, HEIGHT / 4)
            music_status = "ON" if self.music_on else "OFF"
            self.draw_text("Music: " + music_status, 30, WHITE, WIDTH / 2, HEIGHT / 2)
            self.draw_text("Press M to toggle music", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
            self.draw_text("Press ESC to resume", 22, WHITE, WIDTH / 2, HEIGHT / 2 + 80)
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = False
                    elif event.key == pygame.K_m:
                        # Toggle music on/off
                        if self.music_on:
                            pygame.mixer.music.pause()
                            self.music_on = False
                        else:
                            pygame.mixer.music.unpause()
                            self.music_on = True
        # Adjust the level_start_time so the paused period isn’t counted
        pause_duration = pygame.time.get_ticks() - pause_start
        self.level_start_time += pause_duration

game = Game()
while game.running:
    playing = game.show_start_screen()
    while playing and game.running:
        game.new()
        playing = game.show_gameover_screen()

pygame.quit()
