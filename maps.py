# maps.py 

import pygame

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
