# v4

from urllib.parse import MAX_CACHE_SIZE
import pygame
import os
import json
from pprint import pprint


class Game():
    def __init__(self):
        self.map = Map("overworld_1")
        self.player = Player("Danny")
        self.enemies = []

        print(self)
        pass

    def start(self):
        self.setup_pygame()
        self.main_loop()

    def setup_pygame(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.window_size = (infoObject.current_w // 2,
                            infoObject.current_h // 2)
        self.window = pygame.display.set_mode(
            (self.window_size[0], self.window_size[1]), 0, 32)
        pygame.display.set_caption('Monster Hunter \'86')
        self.clock = pygame.time.Clock()
        self.running = True

    def main_loop(self):
        while self.running:

            self.map.draw()
            self.player.draw()
            self.monsters.draw()

            pygame.display.update()
            self.clock.tick()

    def __repr__(self):
        return "Game<{}, {}, {}e>".format(self.map, self.player, len(self.enemies))


class Map():
    def __init__(self, name):
        self.name = name
        self.filepath = os.path.join(Utils.MAPS_FOLDER, self.name + ".tmj")
        self.load_tiles()

        print(self)

    def load_tiles(self):
        self.tiles = []
        self.map_data = json.load(open(self.filepath, "r"))

        # Create an empty Tile object for each map space
        for row in range(self.map_data["height"]):
            current_row = []
            for col in range(self.map_data["width"]):
                current_row.append(Tile(row, col))
            self.tiles.append(current_row)

        # Add in the actual tile layers to each Tile object
        for layer_num, layer_object in enumerate(self.map_data["layers"]):
            if layer_object["visible"]:
                for tile_id, tileset_num in enumerate(layer_object["data"]):
                    self.tiles[tile_id // layer_object["width"] + layer_object["y"]
                            ][tile_id % layer_object["width"] + layer_object["x"]].add_layer()

    def draw(self):
        for row_num, row_tiles in enumerate(self.tiles):
            for col_num, col_tile in enumerate(row_tiles):
                col_tile.draw()

    def __repr__(self) -> str:
        return "Map<{}, {}w, {}h>".format(self.name, self.map_data["width"], self.map_data["height"])


class Tile():
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.layers = 0
        pass

    def add_layer(self, tileset_id, layer_name)

    def draw(self):
        pass

    def __repr__(self):
        return "Tile<r{}, c{}, {}l>".format(self.row, self.col, self.layers)


class Player():
    def __init__(self, name) -> None:
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1

        print(self)
        pass

    def __repr__(self):
        return "Player<{}, {}HP, LVL{}>".format(self.name, self.health, self.level)

    pass


class Utils():
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    MAPS_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/maps/')
    TILES_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/tilesets/')


game = Game()
game.start()
