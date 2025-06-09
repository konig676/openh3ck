import pygame
from settings import *
# ------------ player.py ------------
class Player:
    def __init__(self, game_map):
        self.map = game_map
        self.reset()
        self.weapons = ['pistol', 'shotgun', 'machinegun']
        self.current_weapon = 0
        self.last_shot = 0
        
    def reset(self):
        self.x = self.map.width // 2  # вместо WIDTH
        self.y = self.map.height // 2 # вместо HEIGHT
        self.speed = PLAYER_SPEED
        self.health = 100
        self.max_health = 100
        self.size = 32
        self.score = 0
        self.wave = 1
        self.invincible = False
    
        
    def switch_weapon(self):
        self.current_weapon = (self.current_weapon + 1) % len(self.weapons)
        
    def take_damage(self, amount):
        if not self.invincible:
            self.health = max(self.health - amount, 0)
            
    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)

    def move(self, keys):
        dx, dy = 0, 0
        if keys[pygame.K_w]: dy -= self.speed
        if keys[pygame.K_s]: dy += self.speed
        if keys[pygame.K_a]: dx -= self.speed
        if keys[pygame.K_d]: dx += self.speed

        self.x += dx
        self.y += dy

        # Ограничение движения в пределах карты
        self.x = max(0, min(self.x, self.map.width))
        self.y = max(0, min(self.y, self.map.height))