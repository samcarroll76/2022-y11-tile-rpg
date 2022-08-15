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
        self.map_data = json.load(open(self.filepath, "r"))

        self.load_tilesets()
        self.load_map()

        print(self)

    def load_map(self):
        self.map = []

        # Create an empty Tile object for each map space
        for row in range(self.map_data["height"]):
            current_row = []
            for col in range(self.map_data["width"]):
                current_row.append(Tile(row, col))
            self.map.append(current_row)

        # Add in the actual tile layers to each Tile object
        for layer_num, layer_object in enumerate(self.map_data["layers"]):
            if layer_object["visible"]:
                for tile_id, tileset_num in enumerate(layer_object["data"]):

                    row = tile_id // layer_object["width"] + layer_object["y"]
                    col = tile_id % layer_object["width"] + layer_object["x"]

                    self.map[row][col].add_layer(self.get_tile_image(tile_id))

    def load_tilesets(self):
        self.tilesets = []
        for tileset in self.map_data["tilesets"]:
            self.tilesets.append((tileset["firstgid"], Tileset(tileset["source"])))
            pass

    def get_tile_image(self, tile_id):

        pass

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
        self.layers = []
        pass

    def add_layer(self, image, layer_name):
        self.layers.append(
            (image, layer_name)
        )

    def draw(self):

        pass

    def __repr__(self):
        return "Tile<r{}, c{}, {}l>".format(self.row, self.col, len(self.layers))


class Character():
    def __init__(self, name) -> None:
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1

    def __repr__(self):
        return type(self).__name__ + "<{}, {}HP, LVL{}>".format(self.name, self.health, self.level)


class Player(Character):
    def __init__(self, name) -> None:
        super().__init__(name)

        print(self)
        pass

    pass


class Tileset():
    def __init__(self, tsx_path) -> None:
        self.filepath = tsx_path.replace(".tsx", ".tsj")
        self.tileset_data = json.load(open(self.filepath, "r"))

        # Get the image file using the same directory
        self.sheet = pygame.image.load(
            os.path.join(os.path.dirname(self.filepath),
                         self.tileset_data["image"])).convert()

        self.tile_collisions = []
        self.load_collisions()
        pass

    def load_collisions(self):
        for local_tile_id, tile_data in enumerate(self.tileset_data["tiles"]):
            added_collide = False
            for tile_property in tile_data["properties"]:
                if tile_property["name"] == "collide":
                    self.tile_collisions.append(tile_property["value"])
                    added_collide = True
            if not added_collide:
                self.tile_collisions.append(0)

    def get_tile_rect(self, local_tile_id):
        return pygame.Rect(
            (local_tile_id %
             self.tileset_data["columns"]) * self.tileset_data["tilewidth"],
            (local_tile_id //
             self.tileset_data["columns"]) * self.tileset_data["tileheight"],
            self.tileset_data["tilewidth"],
            self.tileset_data["tileheight"]
        )

    def get_tile_surface(self, rectangle):
        # From https://www.pygame.org/wiki/Spritesheet
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0,0))
        #     image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


class Utils():
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    MAPS_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/maps/')
    TILES_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/tilesets/')


game = Game()
game.start()
