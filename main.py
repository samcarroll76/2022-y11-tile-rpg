import pygame
import sys
import os
import time

import maps
import characters
import constants

class Game:
    
    def __init__(self):
        pass
    
    def start(self):
        self.init_pygame()
        
        
    def init_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT), 0, 32)
        pygame.display.set_caption('Pygame Tile Based RPG Example')
        self.clock = pygame.time.Clock()
    
    pass

game = Game()
game.start()