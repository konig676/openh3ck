# ------------ bullet.py ------------
import pygame
import math
from settings import *

class Bullet:
    def __init__(self, start_x, start_y, target_x, target_y):
        self.x = start_x
        self.y = start_y
        self.speed = BULLET_SPEED
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.size = 5
        self.damage = 25

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS['yellow'], (int(self.x), int(self.y)), self.size)