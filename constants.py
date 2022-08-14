import os
import pygame

HEIGHT = 825
WIDTH = 825
FPS = 30

grid_x = 15
grid_y = 15
BOX_SIZE = HEIGHT/grid_x
item_size = int(BOX_SIZE / 2)

DIRPATH = os.path.dirname(os.path.realpath(__file__))
ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
FONTS_FOLDER = os.path.join(DIRPATH, 'assets/fonts/')
MAPS_FOLDER = os.path.join(DIRPATH, 'assets/maps/')
IMAGES_FOLDER = os.path.join(DIRPATH, 'assets/images/')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (122, 122, 122)
DARK_GREY = (61, 61, 61, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (61, 135, 4)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
ORANGE = (255, 90, 0)
PURPLE = (230, 230, 250)

def getTileIm(pathn):
    return pygame.transform.scale(
        pygame.image.load(
            os.path.join(IMAGES_FOLDER, pathn)
        ), (BOX_SIZE, BOX_SIZE)
    )
    
def getCharIm(pathn):
    return pygame.transform.scale(
        pygame.image.load(
            os.path.join(IMAGES_FOLDER, pathn)
        ), (BOX_SIZE/(3/2),BOX_SIZE*(4/3))
    )

images = {
    "tiles": {
        "overworld.txt": {
            "grass": getTileIm("grass.png"),
            "path": getTileIm("path.png"),
            "forest": getTileIm("forest.png"),
            "mountain": getTileIm("mountain.png"),
            "water": getTileIm("water.png"),
            "rick": getTileIm("rick.png"),
            "sand": getTileIm("sand.png"),
            "lava": getTileIm("lava.png"),
            "rick": getTileIm("rick.png"),
            "obsidian": getTileIm("obsidian.png"),
            "nether-portal": getTileIm("nether-portal.png"),
        },
        "nether.txt": {
            "lava": getTileIm("lava.png"),
            "netherack": getTileIm("netherack.png"),
            "obsidian": getTileIm("obsidian.png"),
            "nether-portal": getTileIm("nether-portal.png"),
            "rick": getTileIm("rick.png"),
        },    
    },  
    "players": {
        "dude-d": getCharIm("dude-d.png"),
        "dude-u": getCharIm("dude-u.png"),
        "dude-r": getCharIm("dude-r.png"),
        "dude-l": getCharIm("dude-l.png"),
    },
    "monsters": {
        "skeleton": getCharIm("skeleton.png"),
        "zombie": getCharIm("zombie.png"),
        "enderman": getCharIm("enderman.png"),
        "orc": getCharIm("skeleton.png"),
        
    }
}


