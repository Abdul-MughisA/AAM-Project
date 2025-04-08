import pygame
import sys
from os import path

# Import all details from other files without having to specify the originating file every time
from settings import *
from sprites import *

class Game:
    def __init__(self):
        # Initialises the game window
        self.running = True
        self.level = 1
        self.selected_sprite = None
        self.music_on = True
        self.total_score = 0
        pygame.init()
        pygame.mixer.init()  # Initialises sound

        # Load music file from current directory
        music_path = path.join(path.dirname(__file__), 'music.mp3')
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)  # loop infinitely

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        pygame.key.set_repeat(500, 100) # allows press and hold to work for keys

        # Load large images for floor, title and tutorial
        self.floor_image = pygame.image.load(path.join(path.dirname(__file__), "Floor.png")).convert_alpha()
        self.title_image = pygame.image.load(path.join(path.dirname(__file__), "Title.png")).convert_alpha()
        self.tutorial_image = pygame.image.load(path.join(path.dirname(__file__), "Tutorial.png")).convert_alpha()

        self.load_data()

    # Loads in data from the text map files
    def load_data(self):
        game_folder = path.dirname(__file__) # Sets the map data
        self.map_data = []  # map data stored in this variable
        # Copies data from map file into variable
        map_file = path.join(game_folder, f"map{self.level}.txt") # Opens map based on current level
        with open(map_file, 'rt') as f: # Opens file in text mode
            for line in f:
                self.map_data.append(line) # Appends data to the variable


    def new(self):
        self.level_start_time = pygame.time.get_ticks() # Record level start time
        # Create all objects
        self.all_sprites = pygame.sprite.LayeredUpdates() # Allow sprites to be layered
        self.walls = pygame.sprite.Group()
        self.stones = pygame.sprite.Group()
        self.flags = pygame.sprite.Group()
        self.grass = pygame.sprite.Group()
        self.logs = pygame.sprite.Group()
        self.waters = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        # Add elements to the screen as indicated by the map file
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
                if tile == 'S':
                    Portal(self, col, row)
        self.run() # Game runs every time it is called


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
                    self.pause_settings() # Show pause screen
                # Move only if a sprite is selected
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


    # Draws the grey lines to show the grid
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pygame.draw.line(self.screen, SILVER, (0, y), (WIDTH, y))
        
    def draw(self):
        # Draw background floor and grid
        for y in range(0, HEIGHT, TILESIZE):
            for x in range(0, WIDTH, TILESIZE):
                self.screen.blit(self.floor_image, (x, y))
        self.draw_grid()
        self.all_sprites.draw(self.screen)

        # Draw HUD at top displaying game stats
        hud_y = 20
        margin = 20
        level_text = "Level: " + str(self.level)
        elapsed_ms = pygame.time.get_ticks() - self.level_start_time
        time_text = "Time: {:.1f}s".format(elapsed_ms / 1000)
        level_score = round(100000 / (elapsed_ms / 1000 + 20) + 100) # Score calculation algorithm
        score_text = "Score: " + str(level_score)

        self.draw_text(level_text, 22, WHITE, margin, hud_y, align="left")
        self.draw_text(time_text, 22, WHITE, WIDTH / 2, hud_y, align="center")
        self.draw_text(score_text, 22, WHITE, WIDTH - margin, hud_y, align="right")
        
        # If a sprite is selected, show an overlay on it.
        if self.selected_sprite is not None:
            overlay = pygame.Surface((self.selected_sprite.rect.width, self.selected_sprite.rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 100))
            self.screen.blit(overlay, self.selected_sprite.rect)
        
        pygame.display.flip()
    
    # Checks whether the user has clicked on a button
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

    # Waits for a key to be pressed
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
    
    # Draws text on the screen and aligns to center unless specified otherwise
    def draw_text(self, text, size, colour, x, y, align="center"):
        font = pygame.font.Font(pygame.font.match_font('arial'), size)
        text_surface = font.render(text, True, colour)
        text_rect = text_surface.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        elif align == "left":
            text_rect.midleft = (x, y)
        elif align == "right":
            text_rect.midright = (x, y)
        self.screen.blit(text_surface, text_rect)

    # Shows the start screen with the title and play button
    def show_start_screen(self):
        # Draw the play button
        play_button = pygame.Rect(WIDTH / 2 - 10, HEIGHT / 2 + 89, 90, 40)
        while True:
            self.screen.fill(BLACK)
            title_rect = self.title_image.get_rect()
            title_rect.midtop = (WIDTH / 2, HEIGHT / 1000)
            self.screen.blit(self.title_image, title_rect)
            # Determine mouse position
            mous_pos = pygame.mouse.get_pos()
            if play_button.collidepoint(mous_pos):
                # Draws the box grey if the mouse is over it
                pygame.draw.rect(self.screen, GREY, play_button)
            else:
                # but draws a white box if not
                pygame.draw.rect(self.screen, WHITE, play_button)

            self.draw_text("Play", 22, BLACK, play_button.centerx, play_button.centery)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_button.collidepoint(event.pos):
                        # Show the tutorial screen right after the play button is pressed
                        self.show_tutorial_screen()
                        return True
            self.clock.tick(FPS)

    # Shows the game over screen when the player loses
    def show_gameover_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("Press any key to play again", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        pygame.display.flip()
        return self.wait_for_key()
    
    # Shows the congratulations screen when the player wins
    def show_congrats_screen(self, score, elapsed_ms):
        self.screen.fill(BLACK)
        self.draw_text("Congratulations!", 48, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("You completed the level!", 22, WHITE, WIDTH / 2, HEIGHT / 2)
        self.draw_text("Your score: " + str(score), 22, WHITE, WIDTH / 2, HEIGHT / 2 + 40)
        self.draw_text("Time taken: " + str(elapsed_ms//1000) + "s", 22, WHITE, WIDTH / 2, HEIGHT * 3/4)
        pygame.display.flip()
        return self.wait_for_key()
    
    # Shows the end screen with the final score and time taken
    def show_end_screen(self):
        self.screen.fill(BLACK)
        # Load and display the finale image
        finale_image = pygame.image.load(path.join(path.dirname(__file__), "Finale.png")).convert_alpha()
        finale_rect = finale_image.get_rect()
        finale_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(finale_image, finale_rect)
        
        # Display the total score (use self.total_score) below the finale image
        self.draw_text(self.total_score, 24, WHITE, WIDTH / 2, HEIGHT - 50, align="center")
        
        pygame.display.flip()
        self.wait_for_key()
        pygame.quit()
        sys.exit()
    
    # Shows the tutorial screen with instructions
    def show_tutorial_screen(self):
        self.screen.fill(BLACK)
        tutorial_rect = self.tutorial_image.get_rect()
        tutorial_rect.center = (WIDTH / 2, HEIGHT / 2)
        self.screen.blit(self.tutorial_image, tutorial_rect)
        pygame.display.flip()
        # Wait until a key is pressed before proceeding
        self.wait_for_key()

    # Shows the pause/settings screen
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
                    if event.key == pygame.K_ESCAPE: # Pause game when ESC is pressed
                        paused = False
                    elif event.key == pygame.K_m: # Toggle music when M pressed
                        # Toggle music on/off
                        if self.music_on:
                            pygame.mixer.music.pause()
                            self.music_on = False
                        else:
                            pygame.mixer.music.unpause()
                            self.music_on = True
        # Adjust the level_start_time so the paused period isn’t counted in score
        pause_duration = pygame.time.get_ticks() - pause_start
        self.level_start_time += pause_duration

game = Game()
while game.running:
    playing = game.show_start_screen()
    while playing and game.running:
        game.new()
pygame.quit()
