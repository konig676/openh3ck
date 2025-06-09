from settings import *

# ------------ camera.py ------------
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = WIDTH
        self.height = HEIGHT
        
    def update(self, target):
        # Центрирование камеры на игроке
        self.x = target.x - self.width // 2
        self.y = target.y - self.height // 2