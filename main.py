# v4

import pygame
import os
import json
import sys

class Game():
    def __init__(self):
        self.setup_pygame()

    def start(self):
        self.map = Map("overworld_1")
        self.player = Player("Danny")
        self.monsters = []

        self.main_loop()

    def setup_pygame(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.window_size = (infoObject.current_w // 2,
                            infoObject.current_h // 2)
        self.window = pygame.display.set_mode(
            (self.window_size[0], self.window_size[1]), pygame.RESIZABLE, 32)
        pygame.display.set_caption('Monster Hunter \'86')
        self.clock = pygame.time.Clock()
        self.running = True

    def main_loop(self):
        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_LEFT or event.key == ord('a'):
                #         dude.move("left")
                #     if event.key == pygame.K_RIGHT or event.key == ord('d'):
                #         dude.move("right")
                #     if event.key == pygame.K_UP or event.key == ord('w'):
                #         dude.move("up")
                #     if event.key == pygame.K_DOWN or event.key == ord('s'):
                #         dude.move("down")

            self.map.draw(self.window)
            # self.player.draw(self.window)
            # for monster in self.monsters:
            #     monster.draw(self.window)
            pygame.display.update()
            self.clock.tick(30)

    def __repr__(self):
        return "Game<{}, {}, {}m>".format(self.map, self.player, len(self.enemies))


class Map():
    def __init__(self, name):
        self.name = name
        self.filepath = os.path.join(Utils.MAPS_FOLDER, self.name + ".tmj")
        self.map_data = json.load(open(self.filepath, "r"))

        self.load_tilesets()
        self.load_map()

        print(self)

    def load_tilesets(self):
        self.tilesets = []
        for tileset in reversed(self.map_data["tilesets"]):
            self.tilesets.append(
                (tileset["firstgid"], Tileset(tileset["source"], self.filepath)))

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
                for tileset_num, map_tile_id in enumerate(layer_object["data"]):

                    row = tileset_num // layer_object["width"] + \
                        layer_object["y"]
                    col = tileset_num % layer_object["width"] + \
                        layer_object["x"]

                    self.map[row][col].add_layer(
                        self.get_tile_surface(map_tile_id), layer_object["name"])

    def get_tile_surface(self, map_tile_id):
        for tileset_tuple in self.tilesets:
            if tileset_tuple[0] <= map_tile_id:
                local_tile_id = map_tile_id - tileset_tuple[0]
                return tileset_tuple[1].get_tile_surface(local_tile_id)

    def draw(self, window):
        for row_tiles in self.map:
            for col_tile in row_tiles:
                col_tile.draw(
                    window,
                    self.map_data["tilewidth"],
                    self.map_data["tileheight"]
                )

    def __repr__(self) -> str:
        return "Map<{}, {}w, {}h>".format(self.name, self.map_data["width"], self.map_data["height"])


class Tile():
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.layers = []
        pass

    def add_layer(self, image_surface, layer_name):
        if image_surface == None:
            return

        self.layers.append(
            (image_surface, layer_name)
        )

    def draw(self, window, width, height):
        for layer in self.layers:
            window.blit(
                layer[0],
                (self.col * width, self.row * height)
            )
        pass

    def __repr__(self):
        return "Tile<r{}, c{}, {}l>".format(self.row, self.col, len(self.layers))


class Character():
    def __init__(self, name) -> None:
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1

    def draw(self):
        pass

    def __repr__(self):
        return type(self).__name__ + "<{}, {}HP, LVL{}>".format(self.name, self.health, self.level)


class Player(Character):
    def __init__(self, name) -> None:
        super().__init__(name)

        print(self)
        pass

    pass


class Tileset():
    def __init__(self, tsx_path, map_path) -> None:
        self.filepath = os.path.join(os.path.dirname(
            map_path), tsx_path.replace(".tsx", ".tsj"))
        self.tileset_data = json.load(open(self.filepath, "r"))

        # Get the image file using the same directory
        self.sheetpath = os.path.join(os.path.dirname(
            self.filepath), self.tileset_data["image"])
        self.sheet = pygame.image.load(self.sheetpath).convert_alpha()


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

    def get_tile_surface(self, local_tile_id):
        tile_slice = self.get_tile_rect(local_tile_id)
        # From https://www.pygame.org/wiki/Spritesheet
        rect = pygame.Rect(tile_slice)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0,0))
        #     image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def __repr__(self):
        return type(self).__name__ + "<{}, {}>".format(os.path.basename(self.filepath), os.path.basename(self.sheetpath))


class Utils():
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    MAPS_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/maps/')
    TILES_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/tilesets/')


game = Game()
game.start()
