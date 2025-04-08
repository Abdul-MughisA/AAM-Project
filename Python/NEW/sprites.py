import pygame
import os
import sys
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 8 # Set layer; higher means higher precendence
        self.groups = game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Druid.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # When object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = True # Identify whether can be pressed

    # d variables set to 0 when they are unspecified
    def move(self, dx=0, dy=0): # only move if no collision
        if not self.collide_with_walls(dx, dy) and \
           not self.collide_with_stones(dx, dy) and \
           not self.collide_with_grass(dx, dy) and \
           not self.collide_with_waters(dx, dy):
            self.x += dx
            self.y += dy
            # Check for portal collision before flag collision:
            if self.collide_with_portal():
                elapsed_ms = pygame.time.get_ticks() - self.game.level_start_time # Calculate elapsed time
                # Directly show the end screen when hitting a portal.
                self.game.show_end_screen(self.game.total_score, elapsed_ms)
                self.game.running = False
                return
            if self.collide_with_flag():
                elapsed_ms = pygame.time.get_ticks() - self.game.level_start_time
                score = round(100000/(elapsed_ms/1000 + 20) + 100)
                self.game.total_score += score
                if self.game.level == 9:
                    self.game.show_end_screen(self.game.total_score, elapsed_ms)
                    pygame.quit()
                    sys.exit()
                else:
                    self.game.show_congrats_screen(score, elapsed_ms)
                    self.game.level += 1 # Increment when flag reaches
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
        # Check if water exists at that tile, nullifies water collision if log present
        for water in self.game.waters:
            if water.x == dest_x and water.y == dest_y:
                for log in self.game.logs:
                    if log.x == dest_x and log.y == dest_y:
                        return False
                return True
        return False

    def collide_with_portal(self, dx=0, dy=0):
        for portal in self.game.portals:
            if portal.x == self.x + dx and portal.y == self.y + dy:
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
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Wall.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False

class Stone(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 9
        self.groups = game.all_sprites, game.stones
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Tree.png")).convert_alpha()
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
        dest_x = self.x + dx
        dest_y = self.y + dy
        # Check if the destination tile has water.
        for water in self.game.waters:
            if water.x == dest_x and water.y == dest_y:
                # If water exists, check for a log on the same tile.
                for log in self.game.logs:
                    if log.x == dest_x and log.y == dest_y:
                        # A log covers the water; ignore water collision.
                        return False
                # No log is present; water collision applies.
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
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Exit Portal.png")).convert_alpha()
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
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grass.png")).convert_alpha()
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
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Log.png")).convert_alpha()
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
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Water.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

        # when object made, pass TILE as argument, not pixel
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False

class Portal(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = 4
        self.groups = game.all_sprites, game.portals
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # Load a Portal PNG (make sure "Portal.png" is in the same folder)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "Hut.png")).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        # set position according to tile size
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.selectable = False
