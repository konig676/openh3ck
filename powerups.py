from settings import *
# ------------ powerups.py ------------
class PowerUp:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type
        self.radius = 20
        self.color = (0, 255, 0) if type == 'health' else (255, 165, 0)
        
    def draw(self, screen, camera):
        pygame.draw.circle(
            screen, 
            self.color,
            (self.x - camera.x, self.y - camera.y),
            self.radius
        )