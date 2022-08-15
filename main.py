# main.py

import pygame
import sys
import os
import time

# import maps
import characters

class Game:
    
    HEIGHT = 825
    WIDTH = 825
    FPS = 30
    
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
        
    
    curPlayerIm = images["players"]["dude-d"]
    
    map_grid = []
    item_grid = []
    temp_grid = []
    temp_item_grid = []
    r = 0
    c = 0
    

    def __init__(self):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self._player_loc = (0, 0)
        box_size = self.HEIGHT/self.grid_x
        item_size = int(box_size / 2)
        
        FONT_SIZE_50 = self.get_font('vectro.otf', 50)
        
        pass
    
    def start(self):
        START = time.time()
        TIMING_LAST_MSG = START
        self.init_pygame()
        dude = characters.Player(self.player_loc[0], self.player_loc[1], self.colors["dude"], self.curPlayerIm, self.window)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        dude.move("left")
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        dude.move("right")
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        dude.move("up")
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        dude.move("down")

            for r in range(self.grid_y):
                for c in range(self.grid_x):
                    self.map_grid[r][c].draw()
                    if self.item_grid[r][c] != 0:
                        self.item_grid[r][c].draw()
            dude.draw()
            
            dude.printInfo()
            # update the rest of the screen
            pygame.display.update()
            self.clock.tick(self.FPS)
                
    def clear_term():
        os.system('cls||clear')
    
        
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