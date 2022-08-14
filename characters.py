from asyncio import constants
import * from constants


class Character: 
    
    def __init__(self):
        pass
    
    def printInfo(self):
        healthText = BUTTON_FONT.render(
            f'HP: {playerStats["health"]}', 1, BLACK)
        constants.window.blit(healthText, (self.col * box_size + (box_size/8), self.row * box_size - 2*(box_size/3)))
    pass
    
    pass

class Player(Character):
    
    def __init__(self, row, col, color, path, surf):
        super().__init__()
        self.row = row
        self.col = col
        self.path = path
        self.color = color
        self.surf = surf
        
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
        
    pass


class Monster(Character):
    
    def __init__(self):
        super().__init__()
        
    pass

class Skeleton(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass

class Enderman(Monster):
    
    def __init__(self):
        super().__init__()
        
    pass