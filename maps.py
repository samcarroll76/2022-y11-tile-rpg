# maps.py 

import pygame

class Map():
    
    def __init__(self, map_path):
        self._map_path = map_path
        # self._map_width = map_width
        # self._map_height = map_height
        
    pass

class Tile(Map):
    
    def __init__(self):
        super().__init__()
        
    
    def __init__(self, row, col, tile_set, path, passable, item, surf):
        self.col = col
        self.row = row
        self.tile_set = tile_set
        self.path = path
        self.passable = passable
        self.item = item
        self.surf = surf # pygame surface 

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
