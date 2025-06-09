# ------------ map.py ------------
import pygame
import random
from settings import *

class Map:
    def __init__(self):
        self.width = WIDTH * 2
        self.height = HEIGHT * 2
        self.tiles = []
        self.obstacles = []
        self.generate()
        
    def generate(self):
        # Генерация ландшафта
        for y in range(0, self.height, TILE_SIZE):
            row = []
            for x in range(0, self.width, TILE_SIZE):
                if random.random() < 0.1:  # 10% стен
                    tile_type = 'wall'
                    self.obstacles.append(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
                else:
                    tile_type = 'grass'
                row.append(tile_type)
            self.tiles.append(row)
            
    def draw(self, screen, camera):
        # Отрисовка тайлов
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                rect = pygame.Rect(
                    x * TILE_SIZE - camera.x, 
                    y * TILE_SIZE - camera.y, 
                    TILE_SIZE, 
                    TILE_SIZE
                )
                if tile == 'wall':
                    pygame.draw.rect(screen, COLORS['wall'], rect)
                else:
                    pygame.draw.rect(screen, COLORS['grass'], rect.inflate(-2, -2))