# v4

import pygame
import os
import json
import sys
import random
import math


class Game():
    def __init__(self):
        self.setup_pygame()

    def start(self):
        self.map = Map("overworld_1")
        self.player = Player("Danny", 3, 3)
        self.monsters = [
            Monster("jerry", 1, 12.5),
            Monster("jerry2", 10, 10)
        ]

        self.main_loop()

    def setup_pygame(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.window_size = (infoObject.current_w // 2,
                            infoObject.current_h // 2)

        self.scale_factor = 4

        Utils.load_fonts()

        self.window = pygame.display.set_mode(
            (self.window_size[0], self.window_size[1]), pygame.SCALED | pygame.RESIZABLE, 32)
        pygame.display.set_caption('Monster Hunter \'86')

        self.clock = pygame.time.Clock()

        self.running = True
        self.should_restart = False

    def update(self):

        self.map.update()
        self.player.update(self.map)
        for monster in self.monsters:
            monster.update(self.map, self.player.get_loc())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                self.window = pygame.display.set_mode(
                    event.size, pygame.SCALED | pygame.RESIZABLE, 32)
                self.window_size = event.size
                pygame.display.update()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_j:
                    self.player.attack_nearest(self.monsters)
                if event.key == pygame.K_l:
                    self.player.take_damage(50)
                if event.key == pygame.K_r and self.player.is_dead():
                    self.restart()

    def draw(self):
        self.map.draw(self.render_surface)
        self.player.draw(self.render_surface)
        for monster in self.monsters:
            monster.draw(self.render_surface)

        self.window.fill((50, 50, 50))
        self.window.blit(pygame.transform.scale(
            self.render_surface,
            self.map.get_scaled_pixel_size_tuple(self.scale_factor)
        ), (self.get_surf_point()))

        if self.player.is_dead():
            self.window.fill((255, 255, 255))
            die_text = Utils.SIZE_40_FONT.render(
                'YOU DIED! \n Restart the game to play again!', True, Utils.CLR_RED)
            textRect = die_text.get_rect()
            textRect.center = (self.window_size[0] // 2,
                               self.window_size[1] // 2)

            self.window.blit(die_text, textRect)

    def get_surf_point(self):
        return (
            Utils.limit(
                self.window_size[0]//2 -
                self.player.get_x() * self.scale_factor,
                self.window_size[0] - self.map.get_scaled_pixel_size_tuple(self.scale_factor)[0], 0),
            Utils.limit(
                self.window_size[1]//2 -
                self.player.get_y() * self.scale_factor,
                self.window_size[1] - self.map.get_scaled_pixel_size_tuple(self.scale_factor)[1], 0),
        )

    def main_loop(self):

        self.render_surface = pygame.Surface(
            self.map.get_pixel_size_tuple(), pygame.SRCALPHA, 32).convert_alpha()

        while self.running:

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(30)

        if (self.should_restart):
            self.should_restart = False
            self.running = True
            self.start()

    def restart(self):
        self.running = False
        self.should_restart = True

    def __repr__(self):
        return "Game<{}, {}, {}m>".format(self.map, self.player, len(self.enemies))


class Map():
    def __init__(self, name):
        self.name = name
        self.filepath = os.path.join(Utils.MAPS_FOLDER, self.name + ".tmj")
        self.map_data = json.load(open(self.filepath, "r"))
        self.map = []

        self.load_tilesets()
        self.load_map()

        print(self)

    def load_tilesets(self):
        self.tilesets = []
        for tileset in reversed(self.map_data["tilesets"]):
            self.tilesets.append(
                (tileset["firstgid"], Tileset(tileset["source"], self.filepath)))

    def get_pixel_width(self):
        return self.map_data["width"] * self.map_data["tilewidth"]

    def get_pixel_height(self):
        return self.map_data["height"] * self.map_data["tileheight"]

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
                    self.map[row][col].add_collide(
                        self.does_tile_collide(map_tile_id))

    def get_tileset_tuple_local(self, map_tile_id):
        for tileset_tuple in self.tilesets:
            if tileset_tuple[0] <= map_tile_id:
                print(tileset_tuple)
                return (map_tile_id - tileset_tuple[0], tileset_tuple[1])

    def get_tile_surface(self, map_tile_id):
        tileset_tuple = self.get_tileset_tuple_local(map_tile_id)
        if tileset_tuple:
            return tileset_tuple[1].get_tile_surface(tileset_tuple[0])

    def does_tile_collide(self, map_tile_id):
        tileset_tuple = self.get_tileset_tuple_local(map_tile_id)
        if tileset_tuple:
            return tileset_tuple[1].does_tile_collide(tileset_tuple[0])

    def update(self):
        pass

    def draw(self, surface):
        for row_tiles in self.map:
            for col_tile in row_tiles:
                col_tile.draw(
                    surface,
                    self.map_data["tilewidth"],
                    self.map_data["tileheight"]
                )

    def get_adjacent_collide_list(self, pixel_coords):
        row = int(pixel_coords[0] / self.map_data["tilewidth"])
        col = int(pixel_coords[1] / self.map_data["tileheight"])

        collide_list = []
        calc_range = 3
        for x_rel in range(-calc_range, calc_range, 1):
            for y_rel in range(-calc_range, calc_range, 1):
                x = row + x_rel
                y = col + y_rel
                if x >= 0 and x < self.map_data["width"]:
                    if y >= 0 and y < self.map_data["height"]:
                        if self.map[y][x].does_collide():
                            collide_list.append(pygame.Rect(
                                x * self.map_data["tilewidth"],
                                y * self.map_data["tileheight"],
                                self.map_data["tilewidth"],
                                self.map_data["tileheight"]
                            ))
        return collide_list

    def get_size_tuple(self):
        return (
            self.map_data["width"],
            self.map_data["height"]
        )

    def get_pixel_size_tuple(self):
        return (
            self.map_data["width"] * self.map_data["tilewidth"],
            self.map_data["height"] * self.map_data["tilewidth"]
        )

    def get_scaled_pixel_size_tuple(self, scale_factor):
        return (
            self.map_data["width"] * self.map_data["tilewidth"] * scale_factor,
            self.map_data["height"] * self.map_data["tilewidth"] * scale_factor
        )

    def __repr__(self) -> str:
        return "Map<{}, {}w, {}h>".format(self.name, self.map_data["width"], self.map_data["height"])


class Tile():
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.collide = False
        self.layers = []
        pass

    def add_layer(self, image_surface, layer_name):
        if image_surface == None:
            return

        self.layers.append(
            (image_surface, layer_name)
        )

    def add_collide(self, collide):
        self.collide = self.collide or collide

    def draw(self, surface, width, height):
        for layer in self.layers:
            surface.blit(
                layer[0],
                (self.col * width, self.row * height)
            )

    def does_collide(self):
        return self.collide

    def __repr__(self):
        return "Tile<r{}, c{}, {}l>".format(self.row, self.col, len(self.layers))


class Weapon():

    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        # self.image = image

    def get_damage(self):
        return self.damage


class Character():

    WEAPON_LIST = [
        Weapon("Hand", 5),
        Weapon("Stick", 7),
        Weapon("Stick v2", 9)
    ]

    def __init__(self, name, x, y) -> None:
        self.size = 10
        self.bounding_rect = pygame.Rect(
            x*16, y*16, self.size, self.size)
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        # self.width = 16
        # self.height = 16
        self.movement_speed = 2

        self.sight_range = 7 * self.bounding_rect.w
        self.cooldown_length = 1500
        self.last_attack = pygame.time.get_ticks()
        self.weapon_id = 0

        self.unique_colour = Utils.get_hexcolor(name + str(x) + str(y))

        self._collidelist = []

        print(self)

    def get_x(self):
        return self.bounding_rect.x

    def get_y(self):
        return self.bounding_rect.y

    def move_vector(self, map, shift_vector):
        if shift_vector.length() <= 0:
            return

        shift_vector.scale_to_length(self.movement_speed)

        new_pos = pygame.Rect(
            round(Utils.limit(self.bounding_rect.x + shift_vector.x,
                  0, map.get_pixel_width() - self.bounding_rect.w), 1),
            round(Utils.limit(self.bounding_rect.y + shift_vector.y,
                  0, map.get_pixel_height() - self.bounding_rect.h), 1),
            self.bounding_rect.w,
            self.bounding_rect.h
        )
        if (self.check_valid_move(map, new_pos)):
            self.bounding_rect = new_pos

    def move(self, shift, map):
        self.move_vector(map, pygame.math.Vector2(shift))

    def update(self, map):
        pass

    def check_valid_move(self, map, new_pos):
        self._collidelist = map.get_adjacent_collide_list(new_pos.center)
        return new_pos.collidelist(
            self._collidelist
        ) == -1

    def draw(self, surface):

        pygame.draw.rect(surface, self.unique_colour, self.bounding_rect)

        # for collide_block in self._collidelist:
        #     pygame.draw.rect(surface, pygame.Color(255,0,0,128), collide_block)

        # surface.blit(
        #     pygame.Rect(0,0,16,16),
        #     (self.bounding_rect.x * 16, self.bounding_rect.y * 16)
        # )
        pass

    def distance_to(self, other):
        dist_x = self.bounding_rect.x - other.bounding_rect.x
        dist_y = self.bounding_rect.y - other.bounding_rect.y
        return math.sqrt((dist_x ** 2 + dist_y ** 2)) 

    def cooldown_expired(self):
        if self.last_attack >= pygame.time.get_ticks() - 1500:
            return True
        return False

    def get_weapon(self):
        return self.WEAPON_LIST[self.weapon_id]

    def get_loc(self):
        return (self.bounding_rect.x, self.bounding_rect.y)

    def get_centre(self):
        return (self.bounding_rect.x + self.bounding_rect.w // 2, self.bounding_rect.y + self.bounding_rect.h//2)

    def attack_nearest(self, monsters):
        monster_dist = {}
        for monster in monsters:
            dist = self.distance_to(monster)
            monster_dist[monster] = dist
        print(monster_dist)
        closest_monster = min(monster_dist, key=monster_dist.get) 
        self.attack(closest_monster) 
         

    def attack(self, target):
        if self.distance_to(target) <= self.bounding_rect.w*2:
            # if self.cooldown_expired():
            target.take_damage(target, (self.get_weapon().get_damage()))

    def take_damage(self, target, damage):
        target.health = Utils.limit((target.health - damage), 0, target.max_health)
        print(target.health)
        self.is_dead()
        self.remove_monster()
        
    def remove_monster(self):
        if self.is_dead():
            print("dead")
        
        

    def is_dead(self):
        if self.health <= 0:
            return True
        return False

    def __repr__(self):
        return type(self).__name__ + "<{}, {}HP, LVL{}>".format(self.name, self.health, self.level)


class Player(Character):

    def __init__(self, name, x, y) -> None:
        super().__init__(name, x, y)
        pass

    def update(self, map):
        super().update(map)

        keys = pygame.key.get_pressed()

        move_vec = pygame.math.Vector2()
        if keys[pygame.K_LEFT]:
            move_vec.x -= 1
        if keys[pygame.K_RIGHT]:
            move_vec.x += 1
        if keys[pygame.K_UP]:
            move_vec.y -= 1
        if keys[pygame.K_DOWN]:
            move_vec.y += 1
        self.move_vector(map, move_vec)

    pass


class Monster(Character):
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        self.movement_speed *= 0.8
        
        self.current_vec = pygame.math.Vector2()
        self.last_dir_change = pygame.time.get_ticks()

    def auto_move(self, map, player_loc):
        vec_to_player = pygame.math.Vector2(
            player_loc[0] - self.bounding_rect.x,
            player_loc[1] - self.bounding_rect.y
        )

        if vec_to_player.length() <= 1:
            return

        if vec_to_player.length() <= self.sight_range:
            # head toward player
            self.move_vector(map, vec_to_player)
        else:
            # self.rand_move(map)
            pass

    # def rand_move(self, map):

    #     self.move_vector(map, self.current_vec)

    #     if self.last_dir_change >= pygame.time.get_ticks() - 500:
    #         return
        
    #     self.last_dir_change = pygame.time.get_ticks()

    #     possible_dir = [
    #         (-1, -1),
    #         (-1, 0),
    #         (-1, 1),
    #         (0, -1),
    #         (0, 1),
    #         (1, -1),
    #         (1, 0),
    #         (1, 1)
    #     ]
    #     index = random.randint(0,7)
    #     self.current_vec = pygame.math.Vector2(possible_dir[index])


    def update(self, map, player_loc):
        super().update(map)

        self.auto_move(map, player_loc)
        # self.rand_move(map)


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

    def get_tile_slice_rect(self, local_tile_id):
        return pygame.Rect(
            (local_tile_id %
             self.tileset_data["columns"]) * self.tileset_data["tilewidth"],
            (local_tile_id //
             self.tileset_data["columns"]) * self.tileset_data["tileheight"],
            self.tileset_data["tilewidth"],
            self.tileset_data["tileheight"]
        )

    def get_tile_surface(self, local_tile_id):
        tile_slice = self.get_tile_slice_rect(local_tile_id)
        # From https://www.pygame.org/wiki/Spritesheet
        rect = pygame.Rect(tile_slice)
        image = pygame.Surface(rect.size, pygame.SRCALPHA, 32).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        # if colorkey is not None:
        #     if colorkey is -1:
        #         colorkey = image.get_at((0,0))
        #     image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def does_tile_collide(self, local_tile_id):
        return self.tile_collisions[local_tile_id]

    def __repr__(self):
        return type(self).__name__ + "<{}, {}>".format(os.path.basename(self.filepath), os.path.basename(self.sheetpath))


class Utils():
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    MAPS_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/maps/')
    TILES_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/tilesets/')

    SIZE_40_FONT = None

    def load_fonts():
        Utils.SIZE_40_FONT = pygame.font.Font(
            pygame.font.get_default_font(), 40)

    CLR_RED = (255, 0, 0)
    CLR_BLUE = (0, 0, 255)
    CLR_GREEN = (0, 255, 0)

    def limit(n, min_n, max_n):
        return max(min(max_n, n), min_n)

    def get_randint_255():
        return random.randint(0, 255)

    def get_hexcolor(input):
        random.seed(input)
        return pygame.Color(Utils.get_randint_255(), Utils.get_randint_255(), Utils.get_randint_255())


game = Game()
game.start()
