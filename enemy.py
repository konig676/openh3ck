# ------------ enemy.py ------------
import pygame
import math
import random
from settings import *

class Enemy:
    def __init__(self, x, y, wave):  # Добавьте x и y как параметры
        self.x = x
        self.y = y
        self.size = 15 + wave
        self.speed = 1.0 + wave * 0.1
        self.max_health = 50 + wave * 10
        self.health = self.max_health
        self.type = random.choice(['normal', 'fast', 'tank'])[:wave//3]

        # Модификаторы для разных типов
        if self.type == 'fast':
            self.speed *= 1.5
            self.max_health /= 2
        elif self.type == 'tank':
            self.speed *= 0.7
            self.max_health *= 2

    def update(self, player, bullets):
        angle = math.atan2(player.y - self.y, player.x - self.x)
        self.x += self.speed * math.cos(angle)
        self.y += self.speed * math.sin(angle)

        for bullet in bullets:
            distance = math.hypot(bullet.x - self.x, bullet.y - self.y)
            if distance < 50:
                angle_bullet = math.atan2(self.y - bullet.y, self.x - bullet.x)
                self.x += math.cos(angle_bullet) * 5
                self.y += math.sin(angle_bullet) * 5


    def draw(self, screen, camera):  # Добавьте параметр camera
        color = COLORS['red']
        if self.type == 'fast':
            color = (255, 165, 0)
        elif self.type == 'tank':
            color = (139, 69, 19)
        # Корректировка позиции с учетом камеры
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.size)
    
    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)