# main.py

import pygame
import sys
import os
import time

# import maps
# import characters

class Game:
    
    HEIGHT = 825
    WIDTH = 825
    FPS = 30
    
    grid_x = 15
    grid_y = 15
    box_size = HEIGHT/grid_x
    item_size = int(box_size / 2)
    
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    FONTS_FOLDER = os.path.join(DIRPATH, 'assets/fonts/')
    MAPS_FOLDER = os.path.join(DIRPATH, 'assets/maps/')
    IMAGES_FOLDER = os.path.join(DIRPATH, 'assets/images/')

    FONT_SIZE_50 = None
    
    CLR_WHITE = (255, 255, 255)
    CLR_BLACK = (0, 0, 0)
    CLR_GREY = (122, 122, 122)
    CLR_DARK_GREY = (61, 61, 61, 200)
    CLR_RED = (255, 0, 0)
    CLR_GREEN = (0, 255, 0)
    CLR_DARK_GREEN = (61, 135, 4)
    CLR_BLUE = (0, 0, 255)
    CLR_LIGHT_BLUE = (100, 100, 255)
    CLR_ORANGE = (255, 90, 0)
    CLR_PURPLE = (230, 230, 250)

    START = 0
    TIMING_LAST_MSG = 0

    def __init__(self):
        FONT_SIZE_50 = self.get_font('vectro.otf', 50)
        
        
        pass
    
    def start(self):
        START = time.time()
        TIMING_LAST_MSG = START
        self.init_pygame()
        
        
        
    def init_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption('Pygame Tile Based RPG Example')
        self.clock = pygame.time.Clock()
    
    def get_font(self, path, height_divisor):
        return pygame.font.Font(os.path.join(self.FONTS_FOLDER, path), int(self.HEIGHT/height_divisor))

    def t(self, msg):  # TIMING FUNCTION
        new = time.time()
        lstFrmTime = new - self.TIMING_LAST_MSG
        timeSinceStart = new - self.START
        print(f"\nLast: {(lstFrmTime):.3f} , Start: {(timeSinceStart):.3f} , FPS: {(1/lstFrmTime):.1f} -- {msg}")
        self.TIMING_LAST_MSG = new

    
    pass

game = Game()
game.start()