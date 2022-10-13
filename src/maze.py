import math
import numpy
import pygame as pg
from pygame import Surface
from pygame.sprite import Sprite

from vector import Vector
import game as gm

class Maze(Sprite):
    ## TILE STATES
    # 0 = wall (the only non-traversable tile)
    # 1 = empty
    # 2 = food pellet
    # 3 = power pellet
    # 4 = ghost house entrance

    ## MAZE DIMENSIONS
    # maze is 28x31 tiles (each tile having a state as described above)
    # each tile is 3*(8x8) = 24x24 pixels

    FRESH_MAZE = (
        '0000000000000000000000000000'
        '0222222222222002222222222220'
        '0200002000002002000002000020'
        '0300002000002002000002000030'
        '0200002000002002000002000020'
        '0222222222222222222222222220'
        '0200002002000000002002000020'
        '0200002002000000002002000020'
        '0222222002222002222002222220'
        '0000002000001001000002000000'
        '0000002000001001000002000000'
        '0000002001111111111002000000'
        '0000002001000440001002000000'
        '0000002001011111101002000000'
        '1111112111011111101112111111'
        '0000002001011111101002000000'
        '0000002001000000001002000000'
        '0000002001111111111002000000'
        '0000002001000000001002000000'
        '0000002001000000001002000000'
        '0222222222222002222222222220'
        '0200002000002002000002000020'
        '0200002000002002000002000020'
        '0322002222222112222222002230'
        '0002002002000000002002002000'
        '0002002002000000002002002000'
        '0222222002222002222002222220'
        '0200000000002002000000000020'
        '0200000000002002000000000020'
        '0222222222222222222222222220'
        '0000000000000000000000000000'
    )

    WIDTH, HEIGHT = 28, 31
    TILE_SIZE = 24 # 24x24 square

    # Converts a pixel-scaled Vector into a tile-scaled Vector.
    @staticmethod
    def pixel2tile(px_vec: Vector):
        return px_vec/Maze.TILE_SIZE
    
    # Converts a tile-scaled Vector into a pixel-scaled Vector.
    @staticmethod
    def tile2pixel(tile_vec: Vector):
        return tile_vec*Maze.TILE_SIZE
    
    # Returns the center pixel of a tile.
    @staticmethod
    def tile2pixelctr(tile_vec: Vector):
        return tile_vec*Maze.TILE_SIZE + Vector(12, 12)

    # Converts a tile vector into its position in the maze string.
    @staticmethod
    def tile2strpos(tile_vec: Vector):
        x, y = math.floor(tile_vec.x), math.floor(tile_vec.y)
        return x + Maze.WIDTH*y

    def __init__(self, game):
        self.game = game
        self.surface: Surface = game.screen # TODO: switch out to dedicated playfield component?
        self.maze = Maze.FRESH_MAZE
        self.image = pg.image.load(gm.Game.PROJECT_DIR + '/resources/sprites/maze.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = numpy.subtract(self.surface.get_rect().center, self.rect.center)

        # sprites
        self.food_pellet = pg.surface.Surface(size=(6, 6))
        self.food_pellet.fill((255, 183, 174))
        # TODO
        # self.power_pellet = pg.image.load(gm.Game.PROJECT_DIR + '/resources/sprites/power_pellet.png')
    
    # Returns the state of a tile. Refer to top of this class for states.
    def get_tile_state(self, tile_vec: Vector):
        strpos = Maze.tile2strpos(tile_vec)
        return int(self.maze[strpos])
    
    # Change tile state, set other game states.
    def consume_tile(self, tile_vec: Vector):
        state = self.get_tile_state(tile_vec)
        strpos = Maze.tile2strpos(tile_vec)

        if state == 0: # (why are we eating a wall?)
            raise ValueError('tried to consume a wall!')
        elif state == 2: # food pellet
            self.maze[strpos] = 1
            # TODO: change score, counters
        elif state == 3: # power pellet
            self.maze[strpos] = 1
            # TODO: change score, counters, flee state

    def reset(self):
        self.maze = Maze.FRESH_MAZE
    
    def blit_relative(self, surface: Surface, rect: pg.Rect):
        r = rect.copy()
        r.center = (rect.center[0] + self.rect.left, rect.center[1] + self.rect.top)
        self.surface.blit(surface, r)

    def draw(self):
        # draw maze walls
        self.surface.blit(self.image, self.rect)
        for y in range(Maze.HEIGHT):
            for x in range(Maze.WIDTH):
                state = self.get_tile_state(Vector(x, y))
                if state in [0, 1, 4]: continue # skip non-consumables

                tile_ctr = Maze.tile2pixelctr(Vector(x, y))

                if state == 2: # food pellet
                    rect = self.food_pellet.get_rect()
                    rect.center = (tile_ctr.x, tile_ctr.y)
                    self.blit_relative(self.food_pellet, rect)
                elif state == 3:
                    pass # TODO: power pellet

    def update(self):
        self.draw()