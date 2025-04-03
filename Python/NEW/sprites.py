import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 3
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = True

    # d variables set to 0 when they are unspecified
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy) and not self.collide_with_stones(dx, dy) and not self.collide_with_grass(dx, dy) and not self.collide_with_waters(dx, dy):
            self.x += dx
            self.y += dy
            if self.collide_with_flag():
                # Compute elapsed time and score
                elapsed_ms = pygame.time.get_ticks() - self.game.level_start_time
                score = round(100000/(elapsed_ms/1000 + 20) + 100)
                # Show congratulations screen between levels
                self.game.show_congrats_screen(score, elapsed_ms)
                self.game.level += 1
                self.game.load_data()
                self.game.new()

    # checks peeks ahead to walls, and does not move if wall found
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    
    def collide_with_stones(self, dx=0, dy=0):
        for stone in self.game.stones:
            if stone.x == self.x + dx and stone.y == self.y + dy:
                return True
        return False

    def collide_with_flag(self):
        for flag in self.game.flags:
            if flag.x == self.x and flag.y == self.y:
                return True
        return False
    
    def collide_with_grass(self, dx=0, dy=0):
        for grass in self.game.grass:
            if grass.x == self.x + dx and grass.y == self.y + dy:
                return True
        return False

    def collide_with_waters(self, dx=0, dy=0):
        # Determine the destination tile coordinate.
        dest_x = self.x + dx
        dest_y = self.y + dy
        # Check if water exists at that tile.
        for water in self.game.waters:
            if water.x == dest_x and water.y == dest_y:
                # If water exists, check if there's a log on the same tile.
                for log in self.game.logs:
                    if log.x == dest_x and log.y == dest_y:
                        # A log is covering the water, so ignore water collision.
                        return False
                # No log is present to cover the water: collision occurs.
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 5
        self.groups = game.all_sprites, game.walls
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False

class Stone(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 2
        self.groups = game.all_sprites, game.stones
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = True

    def move(self, dx=0, dy=0):
        if  not self.collide_with_walls(dx, dy) and \
            not self.collide_with_stones(dx, dy) and \
            not self.collide_with_player(dx, dy) and \
            not self.collide_with_flag(dx, dy) and \
            not self.collide_with_logs(dx, dy) and \
            not self.collide_with_waters(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
    
    def collide_with_stones(self, dx=0, dy=0):
        for stone in self.game.stones:
            if stone.x == self.x + dx and stone.y == self.y + dy:
                return True
        return False
    
    def collide_with_player(self, dx=0, dy=0):
        player = self.game.player
        if player.x == self.x + dx and player.y == self.y + dy:
            return True
        return False
    
    def collide_with_flag(self, dx=0, dy=0):
        for flag in self.game.flags:
            if flag.x == self.x + dx and flag.y == self.y + dy:
                return True
        return False
    
    def collide_with_logs(self, dx=0, dy=0):
        for log in self.game.logs:
            if log.x == self.x + dx and log.y == self.y + dy:
                return True
        return False

    def collide_with_waters(self, dx=0, dy=0):
        for water in self.game.waters:
            if water.x == self.x + dx and water.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Flag(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 4
        self.groups = game.all_sprites, game.flags
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False

class Grass(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 0
        self.groups = game.all_sprites, game.grass
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False

class Log(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 7
        self.groups = game.all_sprites, game.logs
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = True

    def move(self, dx=0, dy=0):
        # Force vertical movement
        dy = 0
        if not self.collide_with_walls(dx, dy) and \
            not self.collide_with_stones(dx, dy) and \
            not self.collide_with_player(dx, dy) and \
            not self.collide_with_flag(dx, dy):
            self.x += dx


    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def collide_with_stones(self, dx=0, dy=0):
        for stone in self.game.stones:
            if stone.x == self.x + dx and stone.y == self.y + dy:
                return True
        return False
    
    def collide_with_player(self, dx=0, dy=0):
        player = self.game.player
        if player.x == self.x + dx and player.y == self.y + dy:
            return True
        return False
    
    def collide_with_flag(self, dx=0, dy=0):
        for flag in self.game.flags:
            if flag.x == self.x + dx and flag.y == self.y + dy:
                return True
        return False
    
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE


class Water(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 6
        self.groups = game.all_sprites, game.waters
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(CYAN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False
