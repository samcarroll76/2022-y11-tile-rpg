# v4

# Final Commit

from curses import COLOR_WHITE
import pygame
import os
import json
import sys
import random
import math

# Main Game class hiolding and intinitalising methods and main draw and update methods 
class Game():
    def __init__(self):
        self.setup_pygame()
        
    # Creates the map, player and monster objects before running the main loop.
    def start(self):
        self.map = Map("Overworld_1")
        self.player = Player("Danny", 4, 4)
        self.monsters = [
            Monster("jerry", 9, 4),
            Monster("bill", 4, 9),
            Monster("bert", 13, 0.5),
            Monster("jeff", 15, 9),
            Monster("mike", 9, 15),
        ]

        self.main_loop()

    # Inititialises pygame and sets up a lot of key attributes used to make pygame function.
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
        
    # updates the map, the player and all the monsters as well as checks the pygame event 
    # queue for any new events since last iteration 
    def update(self):

        self.map.update()
        self.player.update(self.map)
        for monster in self.monsters:
            monster.update(self.map, self.player.get_loc())

        for event in pygame.event.get():
            if self.player.auto_attack_enabled(self.monsters):
                        self.player.take_damage(self.player, 1)
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
                    self.player.take_damage(self.player,50)
                if event.key == pygame.K_r and self.player.is_dead():
                    self.restart()

    # draws all needed images and surfaces onto their respective planes such 
    # as the map onto the window surface and the player onto the map surface.
    # also draws all the text used in the game.
    def draw(self):
        self.map.draw(self.render_surface)
        self.player.draw(self.render_surface)
        for monster in self.monsters:
            if monster.is_dead() == False:
                monster.draw(self.render_surface)

        self.window.fill((50, 50, 50))
        self.window.blit(pygame.transform.scale(
            self.render_surface,
            self.map.get_scaled_pixel_size_tuple(self.scale_factor)
        ), (self.get_surf_point()))
        
        self.draw_health()

        if self.player.is_dead():
            self.window.fill((255, 255, 255))
            die_text = Utils.WINDOW_SCALED_FONT.render(
                'YOU DIED!!! -- Press "r" to restart the game and play again!', True, Utils.CLR_RED)
            textRect = die_text.get_rect()
            textRect.center = (self.window_size[0] // 2,
                               self.window_size[1] // 2)
            
            

            self.window.blit(die_text, textRect)
            
    # renders a new peice of text for the player health and then draws it to the screen.
    def draw_health(self):
        health_text = Utils.WINDOW_SCALED_FONT.render(
                f'Player Health: {self.player.health:.1f}', True, Utils.CLR_BLACK)
        health_text_rect = health_text.get_rect()
        health_text_rect.center = (self.window_size[0]//6,
                               self.window_size[1] // 8)
        self.window.blit(health_text, health_text_rect)

    # Gets the point at which the map needs to be drawn onto the window surface, specifically so that 
    # the player always remians in the middle of the window when moving around not on a border.
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

    # the main loop which calls all the previous methods in the right order 
    # as well as scaling the render-surface so the map appears larger.
    def main_loop(self):

        self.render_surface = pygame.Surface(
            self.map.get_pixel_size_tuple(), pygame.SRCALPHA, 32).convert_alpha()

        while self.running:

            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(40)

        if (self.should_restart):
            self.should_restart = False
            self.running = True
            self.start()

    # Determines if the game should restart based on its current state
    def restart(self):
        self.running = False
        self.should_restart = True

    # A representation magic method to specify how this class 
    # should be displayed if someone were ever to try to print it.
    def __repr__(self):
        return "Game<{}, {}, {}m>".format(self.map, self.player, len(self.enemies))


# The map class which loads in all the tile_ids and their layout from the Overworld_1.tmj map file
class Map():
    
    # init methods which sets out varibale to be used through the whole class
    def __init__(self, name):
        self.name = name
        self.filepath = os.path.join(Utils.MAPS_FOLDER, self.name + ".tmj")
        self.map_data = json.load(open(self.filepath, "r"))
        self.map = []

        self.load_tilesets()
        self.load_map()

        # print(self)
    # loads the tilsets consisting of the ids and corresponding places on the sprite sheet.
    def load_tilesets(self):
        self.tilesets = []
        for tileset in reversed(self.map_data["tilesets"]):
            self.tilesets.append(
                (tileset["firstgid"], Tileset(tileset["source"], self.filepath)))

    # Gets the pixel width of the map by multiplying the number of columns of 
    # tiles by the tilewidth
    def get_pixel_width(self):
        return self.map_data["width"] * self.map_data["tilewidth"]

    # gets the pixel height of the map by mulitplying the number of rows by the tileheight
    def get_pixel_height(self):
        return self.map_data["height"] * self.map_data["tileheight"]

    # loads the map into a 2 dimensional array from the 1 dimensional array provided by Tiled software
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

    # gets the shifted tileset tuple based on the amount of blank tiles stored before real tiles are indexed
    def get_tileset_tuple_local(self, map_tile_id):
        for tileset_tuple in self.tilesets:
            if tileset_tuple[0] <= map_tile_id:
                # print(tileset_tuple)
                return (map_tile_id - tileset_tuple[0], tileset_tuple[1])

    # determines which layer the tile needs to be put on
    def get_tile_surface(self, map_tile_id):
        tileset_tuple = self.get_tileset_tuple_local(map_tile_id)
        if tileset_tuple:
            return tileset_tuple[1].get_tile_surface(tileset_tuple[0])

    # checks if the tile has a collsion property of 1 on any of its layers
    def does_tile_collide(self, map_tile_id):
        tileset_tuple = self.get_tileset_tuple_local(map_tile_id)
        if tileset_tuple:
            return tileset_tuple[1].does_tile_collide(tileset_tuple[0])

    def update(self):
        pass

    # iterates through the 2 dimesnional array created earlier and 
    # draws each tile onto the specified surface
    def draw(self, surface):
        for row_tiles in self.map:
            for col_tile in row_tiles:
                col_tile.draw(
                    surface,
                    self.map_data["tilewidth"],
                    self.map_data["tileheight"]
                )

    # Checks to see if any of the 49 tiles surrounding the player in a square 
    # have collsions and creates a list with these tiles for later use.
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

    # Returns a tuple of the width and height of the map in terms of rows and columns of tiles
    def get_size_tuple(self):
        return (
            self.map_data["width"],
            self.map_data["height"]
        )

    # gets a tuple of the width and height of the map in pixels 
    # using the rows and columns and the tilewidths and heights
    def get_pixel_size_tuple(self):
        return (
            self.map_data["width"] * self.map_data["tilewidth"],
            self.map_data["height"] * self.map_data["tilewidth"]
        )

    # gets a indentical to the one directly above but scaled up by a preset scale factor 
    def get_scaled_pixel_size_tuple(self, scale_factor):
        return (
            self.map_data["width"] * self.map_data["tilewidth"] * scale_factor,
            self.map_data["height"] * self.map_data["tilewidth"] * scale_factor
        )

    # A represenation magic method specifiying the format for the map 
    # object to be displayed if it is ever tried to be printed
    def __repr__(self) -> str:
        return "Map<{}, {}w, {}h>".format(self.name, self.map_data["width"], self.map_data["height"])

# the tile class used for displaying all the tiles in their separate layers
class Tile():
    def __init__(self, row, col) -> None:
        self.row = row
        self.col = col
        self.collide = False
        self.layers = []
        pass

    # adds a layer to the layers list only if there is some 
    # sort of image surface to make a layer.
    def add_layer(self, image_surface, layer_name):
        if image_surface == None:
            return

        self.layers.append(
            (image_surface, layer_name)
        )

    # defines the collide variable as the parsed collide parameter
    def add_collide(self, collide):
        self.collide = self.collide or collide

    # draws each layer onto a specified surface from the layers list
    def draw(self, surface, width, height):
        for layer in self.layers:
            surface.blit(
                layer[0],
                (self.col * width, self.row * height)
            )

    # returns the collide variable determined earlier for use in collsion logic
    def does_collide(self):
        return self.collide

    # a representation magic method to specify a format in which the tile object can be displayed/printed
    def __repr__(self):
        return "Tile<r{}, c{}, {}l>".format(self.row, self.col, len(self.layers))

# the weapon class for handlding weapon data
class Weapon():
    # assigns important attributes of each weapon to variables
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage
        # self.image = image

    # returns the damage of the weapon object
    def get_damage(self):
        return self.damage


# The character class used for both monsters and the player
class Character():

    # a list of weapon objects
    WEAPON_LIST = [
        Weapon("Hand", 3),
        Weapon("Stick", 6),
        Weapon("Stick v2", 9),
        Weapon("Paper Sword", 12),
        Weapon("Steel Lance", 15),
        Weapon("Herecules Rapier", 20)
    ]
    dead_monsters = []

    # initialises many variable that will be needed througout the class
    def __init__(self, name, x, y) -> None:
        self.size = 10
        self.bounding_rect = pygame.Rect(
            x*16 - self.size/2, y*16 - self.size/2, self.size, self.size)
        self.name = name
        self.max_health = 100
        self.health = self.max_health
        self.level = 1
        # self.width = 16
        # self.height = 16
        self.movement_speed = 2
        self.sight_range = 6 * self.bounding_rect.w
        self.attack_range = self.bounding_rect.w * 3
        self.cooldown_length = 1500
        self.last_attack = pygame.time.get_ticks()
        self.weapon_id = 5

        self.unique_colour = Utils.get_hexcolor(name + str(x) + str(y))

        self._collidelist = []

        # print(self)
    
    # returns the x value of the top left corner of the charcter bounding rectangle
    def get_x(self):
        return self.bounding_rect.x

    # returns the y value of the top left corner of the charcter bounding rectangle
    def get_y(self):
        return self.bounding_rect.y
    
    # Method that takes the shift vector parsed in my the player or a monster and normalises
    # it so that they dont move faster than the movement speed. Also sets the new position for the bounding rectangle
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

    # Calls the move vector method to move self by a certain shift factor
    def move(self, shift, map):
        self.move_vector(map, pygame.math.Vector2(shift))

    # Update Stub
    def update(self, map):
        pass

    # checks if the new position determined by the move vector method will 
    # cause the character to collide with an adjacent tile.
    def check_valid_move(self, map, new_pos):
        self._collidelist = map.get_adjacent_collide_list(new_pos.center)
        return new_pos.collidelist(
            self._collidelist
        ) == -1

    # draws the unqiuely coloured rectangkle for the character based on its x and y coordinates
    def draw(self, surface):

        pygame.draw.rect(surface, self.unique_colour, self.bounding_rect)

        # for collide_block in self._collidelist:
        #     pygame.draw.rect(surface, pygame.Color(255,0,0,128), collide_block)

        # surface.blit(
        #     pygame.Rect(0,0,16,16),
        #     (self.bounding_rect.x * 16, self.bounding_rect.y * 16)
        # )
        pass

    # a function that returns the distance from self to another object using pythagoras
    def distance_to(self, other):
        dist_x = self.bounding_rect.x - other.bounding_rect.x
        dist_y = self.bounding_rect.y - other.bounding_rect.y
        return math.sqrt((dist_x ** 2 + dist_y ** 2)) 

    # unused cooldown timer for attacking
    # def cooldown_expired(self):
    #     if self.last_attack >= pygame.time.get_ticks() - 1500:
    #         return True
    #     return False

    # chooses the weapon using the assigned weapon id as an index
    def get_weapon(self):
        return self.WEAPON_LIST[self.weapon_id]

    # gets a tuple of the characters location
    def get_loc(self):
        return (self.bounding_rect.x, self.bounding_rect.y)

    # gets the centre of the bounding rect for player in tuple form
    def get_centre(self):
        return (self.bounding_rect.x + self.bounding_rect.w // 2, self.bounding_rect.y + self.bounding_rect.h//2)
    
    # returns the monster which is the closest to the player utilising the distance_to() function
    def get_nearest(self, monsters):
        monster_dist = {}
        for monster in monsters:
            dist = self.distance_to(monster)
            monster_dist[monster] = dist
        return min(monster_dist, key=monster_dist.get) 
        
    # calls the attack function on the nearest monster object
    def attack_nearest(self, monsters):
        self.attack(self.get_nearest(monsters)) 
        
    # determines the damage multiplier based on the players current level
    def get_damage_multiplier(self):
        return 1 + (self.level*3)*0.01
    
    # determines the total damage of the weapon and damage multiplier combined
    def get_total_damage(self):
        return self.get_weapon().get_damage()*self.get_damage_multiplier()
    
    # checks to see if the target for attack is in range of the player
    def attack(self, target):
        if self.distance_to(target) <= self.attack_range:
            # if self.cooldown_expired():
            target.take_damage(target, (self.get_weapon().get_damage()))

    # checks to see if the character is dead
    def is_dead(self):
        if self.health <= 0:
            return True
        return False
    
    # loops through the dead monsters list and increments level for each dead/killed monster
    def level_up(self):
        for _ in self.dead_monsters:
            self.level += 1

    # inflicts damage on a character specified by target by subtracting 
    # the total damage from the character's health
    def take_damage(self, target, damage):
        target.health = Utils.limit((target.health - damage), 0, target.max_health)
        if target.is_dead() and target not in self.dead_monsters:
            Character.dead_monsters.append(target)
            # print(self.dead_monsters)
            self.level_up()
        
    # checks to see if the player is within 25 pixels of the nearest monster retruns true if so.
    # used for inflicting damage on the player if they stand too close to a monster
    def auto_attack_enabled(self, monsters):
        if self.distance_to(self.get_nearest(monsters)) <= 25:
            return True
        return False
        

    # a representation magic method which specifies the format for the printing of the character object
    def __repr__(self):
        return type(self).__name__ + "<{}, {}HP, LVL{}>".format(self.name, self.health, self.level)

# the player subclass of character
class Player(Character):
    # inherits the values of name, x, and y from its parent class character
    def __init__(self, name, x, y) -> None:
        super().__init__(name, x, y)
            
    # a method used to update the maps as well as the the players movement and actions such as healing 
    def update(self, map):
        super().update(map)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_h] and self.health <= self.max_health:
            self.health += 0.1
        else:
            move_vec = pygame.math.Vector2()
            if keys[pygame.K_a]:
                move_vec.x -= 1
            if keys[pygame.K_d]:
                move_vec.x += 1
            if keys[pygame.K_w]:
                move_vec.y -= 1
            if keys[pygame.K_s]:
                move_vec.y += 1
            self.move_vector(map, move_vec)
    

# the monster subclass of character
class Monster(Character):
    
    # inherits the name, x, and y variable from its parent class character. 
    # also assigns some variable used only for monster
    def __init__(self, name, x, y):
        super().__init__(name, x, y)
        
        self.movement_speed *= 0.5
        self.current_vec = pygame.math.Vector2()
        self.last_dir_change = pygame.time.get_ticks()


    # automatically moves towards the player based on its player_loc and if the 
    # player is out of sight range of the monster it calls the rnad_move function
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
            self.rand_move(map)
            pass

    # the move method which is used when there is no player in range of the monster object. 
    # Picks a random bearing and moves that way for half a second
    def rand_move(self, map):

        self.move_vector(map, self.current_vec)

        if self.last_dir_change >= pygame.time.get_ticks() - 500:
            return
        
        self.last_dir_change = pygame.time.get_ticks()

        possible_dir = [
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
        ]
        index = random.randint(0,7)
        self.current_vec = pygame.math.Vector2(possible_dir[index])

    # updates the mpa as well as calls the automove method
    def update(self, map, player_loc):
        super().update(map)
        
        # if self.Distanceto(Player) <= 50:
        #     self.take_damage(Player)
            
        
        # if self.is_dead():
        #     self.x = 1000
        #     self.y = 1000
        #     return
        
        self.auto_move(map, player_loc)
        

# tile set class used for interpreting the .tsx and .tsj files produced by Tiled.
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

    # checks the tile properties for each tile in the tileset 
    # to see which one have a collision property. if so, it appends it to a coliding tiles list
    def load_collisions(self):
        for local_tile_id, tile_data in enumerate(self.tileset_data["tiles"]):
            added_collide = False
            for tile_property in tile_data["properties"]:
                if tile_property["name"] == "collide":
                    self.tile_collisions.append(tile_property["value"])
                    added_collide = True
            if not added_collide:
                self.tile_collisions.append(0)

    # Determines the size and location of the slice that needs to be taken from the sprite sheet.
    def get_tile_slice_rect(self, local_tile_id):
        return pygame.Rect(
            (local_tile_id %
             self.tileset_data["columns"]) * self.tileset_data["tilewidth"],
            (local_tile_id //
             self.tileset_data["columns"]) * self.tileset_data["tileheight"],
            self.tileset_data["tilewidth"],
            self.tileset_data["tileheight"]
        )

    # gets the surface on which the spritesheet in first blitted on.
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

    # checks to see if the tile id corresponds to a coliding tile in the tile colisions list
    def does_tile_collide(self, local_tile_id):
        return self.tile_collisions[local_tile_id]

    # a represenatation magic method that specifies the format
    # in which the tileset object should be displayed/printed
    def __repr__(self):
        return type(self).__name__ + "<{}, {}>".format(os.path.basename(self.filepath), os.path.basename(self.sheetpath))

# A static class of utilities that are used all through to code in various applications
class Utils():
    DIRPATH = os.path.dirname(os.path.realpath(__file__))
    ASSET_FOLDER = os.path.join(DIRPATH, 'assets/')
    MAPS_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/maps/')
    TILES_FOLDER = os.path.join(ASSET_FOLDER, 'mapping/tilesets/')

    WINDOW_SCALED_FONT = None

    # font loader
    def load_fonts():
        Utils.WINDOW_SCALED_FONT = pygame.font.Font(
            pygame.font.get_default_font(), 20)

    # colour constants
    CLR_RED = (255, 0, 0)
    CLR_BLUE = (0, 0, 255)
    CLR_GREEN = (0, 255, 0)
    CLR_BLACK = (0, 0, 0)
    CLR_WHITE = (255,255,255)

    # a limit function to limit the values of an expresion
    def limit(n, min_n, max_n):
        return max(min(max_n, n), min_n)

    # a function to return a random integer beteen 0 and 255, used for the unique colour constant generator
    def get_randint_255():
        return random.randint(0, 255)

    # unique colour constant generator
    def get_hexcolor(input):
        random.seed(input)
        return pygame.Color(Utils.get_randint_255(), Utils.get_randint_255(), Utils.get_randint_255())


# game object declaration and initialisation
game = Game()
game.start()
