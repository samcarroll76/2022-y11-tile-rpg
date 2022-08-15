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
        pygame.display.set_caption('Monster Hunter \'86')
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

class Character: 
    
    def __init__(self, surf, row, col):
        self.surf = surf
        self.row = row
        self.col = col
        pass
    
    def printInfo(self):
        healthText = BUTTON_FONT.render(
            f'HP: {playerStats["health"]}', 1, BLACK)
        self.surf.blit(healthText, (self.col * box_size + (box_size/8), self.row * box_size - 2*(box_size/3)))

    def getCharIm(pathn):
        return pygame.transform.scale(
            pygame.image.load(
                os.path.join(IMAGES_FOLDER, pathn)
            ), (box_size/(3/2),box_size*(4/3))
        )
    
    pass

class Player(Character):
    
    playerStats = {
        "health": 20
    }
    # images = "players": {
    #     "dude-d": getCharIm("dude-d.png"),
    #     "dude-u": getCharIm("dude-u.png"),
    #     "dude-r": getCharIm("dude-r.png"),
    #     "dude-l": getCharIm("dude-l.png"),
    
    def __init__(self, row, col, surf, name, path):
        super().__init__(row, col, surf)
        self.name = name
        self.path = path
        
    def move(self, dir):
        if dir == "left":
            self.path = constants.images["players"]["dude-l"]
            if self.col -1 >= 0 and item_grid[self.row][self.col-1] == 0 and map_grid[self.row][self.col-1].passable:
                self.col -= 1
                self.checkActions(map_grid[self.row][self.col])
        elif dir == "right":
            self.path = constants.images["players"]["dude-r"]
            if self.col + 1 < grid_x and item_grid[self.row][self.col+1] == 0 and map_grid[self.row][self.col+1].passable:
                self.col += 1
                self.checkActions(map_grid[self.row][self.col])
        elif dir == "up":
            self.path = constants.images["players"]["dude-u"]
            if self.row - 1 >= 0 and item_grid[self.row-1][self.col] == 0 and map_grid[self.row-1][self.col].passable:
                self.row -= 1
                self.checkActions(map_grid[self.row][self.col])
        elif dir == "down":
            self.path = constants.images["players"]["dude-d"]
            if self.row + 1 < grid_y and item_grid[self.row + 1][self.col] == 0 and map_grid[self.row+1][self.col].passable:
                self.row += 1
                self.checkActions(map_grid[self.row][self.col])
    
    def draw(self):
        window.blit(self.path, (self.col * box_size + (box_size/4), self.row * box_size - (box_size/3)))
           
    pass

class Monster(Character):
    def __init__(self, row, col, name, color, path, surf):
        super().__init__(row, col, surf)
        self.name = name
        self.color = color
        self.path = path
        
    # def draw(self):
    # pygame.draw.rect(
    #   self.surf, 
    #   self.color, 
    #   pygame.Rect(
    #     self.col * box_size + (box_size/3), 
    #     self.row * box_size + (box_size/3), 
    #     item_size, item_size
    #   )
    # )
    # window.blit(self.path, (self.col * box_size + (box_size/4), self.row * box_size - (box_size/3),))
        
    pass

class Skeleton(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass

class Enderman(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass

class Map():
    
    def __init__(self, map_path, surf):
        self._map_path = map_path
        # self._map_width = map_width
        # self._map_height = map_height 
        self.surf = surf # pygame surface 
    
    def getMap(self):
        curMap = open(os.path.join(MAPS_FOLDER,selected_map), "r")

        # Read in the map file
        for line in curMap:
            line = line.strip().split(",")
            if line != ['']:
                
                # if len(line) >= 4:
                #     special = line[3].strip().split('|')
                # else:
                #     special = None
                    
                tile = Tile(r, c, BLACK, images["tiles"][selected_map][line[0]], eval(line[1]), line[2], window)
                # tile = Tile(r, c, colors[line[0]], images["tiles"][line[0]], eval(line[1]), line[2], window, special)
        
                if line[2] != "none":
                    item = line[2].split("|")
                    if item[0] == "monster":
                        monster = Monster(r, c, item[0], None, images["monsters"][item[1]], window)
                        temp_item_grid.append(monster)
                    elif item[0] == "player":
                        dude.row = r
                        dude.col = c
                        temp_item_grid.append(0)
                else:
                    temp_item_grid.append(0)

                temp_grid.append(tile)
                c += 1

                if c % grid_x == 0:
                    r += 1
                    c = 0
                    map_grid.append(temp_grid)
                    item_grid.append(temp_item_grid)
                    temp_grid = []
                    temp_item_grid = []

        curMap.close()
    
    pass

class Tile(Map):
    
    def __init__(self, row, col, tile_set, path, passable, item, surf):
        super().__init__(surf)
        self.col = col
        self.row = row
        self.tile_set = tile_set
        self.path = path
        self.passable = passable
        self.item = item
        
    def getTileIm(pathn):
        return pygame.transform.scale(
            pygame.image.load(
                os.path.join(IMAGES_FOLDER, pathn)
            ), (box_size, box_size)
    )
    

    def draw(self):
        pygame.draw.rect(
            self.surf, 
            self.tile_set, 
            pygame.Rect(self.col * (box_size), self.row * (box_size), box_size, box_size)
        )
        window.blit(self.path, (self.col * (box_size), self.row * (box_size)))
        
    pass

class SpecialTile(Tile):
    
    def __init__(self):
        super().__init__()
        
    pass

class TeleportTile(SpecialTile):
    
    def __init__(self):
        super().__init__()
        
    pass

class ChangeMapTile(Tile):
    
    def __init__(self):
        super().__init__()
        
    pass

game = Game()
game.start()