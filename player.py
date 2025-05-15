# ------------ player.py ------------
import pygame
from settings import *

class Player:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.size = 20
        self.score = 0
        self.wave = 1

    def move(self, keys):
        if keys[pygame.K_w] and self.y > 0: 
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < HEIGHT: 
            self.y += self.speed
        if keys[pygame.K_a] and self.x > 0: 
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < WIDTH: 
            self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, COLORS['blue'], (self.x, self.y), self.size)