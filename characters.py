# characters.py

from mimetypes import init
import pygame, os

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
    images = "players": {
        "dude-d": getCharIm("dude-d.png"),
        "dude-u": getCharIm("dude-u.png"),
        "dude-r": getCharIm("dude-r.png"),
        "dude-l": getCharIm("dude-l.png"),
    
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
        
    def draw(self):
    # pygame.draw.rect(
    #   self.surf, 
    #   self.color, 
    #   pygame.Rect(
    #     self.col * box_size + (box_size/3), 
    #     self.row * box_size + (box_size/3), 
    #     item_size, item_size
    #   )
    # )
    window.blit(self.path, (self.col * box_size + (box_size/4), self.row * box_size - (box_size/3),))
        
    pass

class Skeleton(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass

class Enderman(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass