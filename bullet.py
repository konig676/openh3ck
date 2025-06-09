# ------------ bullet.py ------------
import pygame
import math
from settings import *

class Bullet:
    def __init__(self, start_x, start_y, target_x, target_y, damage):
        self.x = start_x
        self.y = start_y
        self.speed = BULLET_SPEED
        angle = math.atan2(target_y - start_y, target_x - start_x)
        self.dx = math.cos(angle) * self.speed
        self.dy = math.sin(angle) * self.speed
        self.size = 5
        self.damage = 25
        self.damage = damage

    def update(self):
        self.x += self.dx
        self.y += self.dy

    def draw(self, screen, camera):
        screen_x = self.x - camera.x
        screen_y = self.y - camera.y
        color = COLORS['yellow']
        if self.damage == 50:  # Дробовик
            color = (255, 0, 0)  # Красный
            pygame.draw.circle(screen, color, (screen_x, screen_y), self.size + 2)
        elif self.damage == 15:  # Пулемёт
            color = (0, 255, 0)  # Зелёный
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), self.size)
    
    def check_hit(self, enemy):
        distance = math.hypot(self.x - enemy.x, self.y - enemy.y)
        return distance < (self.size + enemy.size)