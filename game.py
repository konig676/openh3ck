# ------------ game.py ------------
import pygame
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Улучшенный ESP-Шутер")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.spawn_wave()
        
    def spawn_wave(self):
        for _ in range(ENEMIES_PER_WAVE + self.player.wave):
            self.enemies.append(Enemy(self.player.wave))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.bullets.append(Bullet(
                    self.player.x, 
                    self.player.y, 
                    mouse_x, 
                    mouse_y
                ))
        return True
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        
        # Обновление врагов
        for enemy in self.enemies:
            enemy.update(self.player, self.bullets)
            
            # Столкновение с игроком
            distance = math.hypot(self.player.x - enemy.x, self.player.y - enemy.y)
            if distance < self.player.size + enemy.size:
                self.player.health = max(self.player.health - 0.5, 0)
                
        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update()
            
            # Удаление за пределами экрана
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                self.bullets.remove(bullet)
                continue
                
            # Проверка попаданий
            for enemy in self.enemies[:]:
                distance = math.hypot(bullet.x - enemy.x, bullet.y - enemy.y)
                if distance < enemy.size:
                    enemy.health -= bullet.damage
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.player.score += 100
                    self.bullets.remove(bullet)
                    break
                    
        # Респавн волны
        if not self.enemies:
            self.player.wave += 1
            self.spawn_wave()
            
        return self.player.health > 0
    
    def draw_esp(self):
        for enemy in self.enemies:
            # Бокс с информацией
            box_width = 60
            box_height = 30
            health_width = 50 * (max(enemy.health, 0) / enemy.max_health)
            
            pygame.draw.rect(self.screen, COLORS['white'], 
                (enemy.x-30, enemy.y-50, box_width, box_height), 2)
            pygame.draw.rect(self.screen, COLORS['red'], 
                (enemy.x-25, enemy.y-45, 50, 5))
            pygame.draw.rect(self.screen, COLORS['green'], 
                (enemy.x-25, enemy.y-45, health_width, 5))
                
    def draw_interface(self):
        font = pygame.font.Font(None, 36)
        text = font.render(
            f"Score: {self.player.score} | HP: {int(self.player.health)} | Wave: {self.player.wave}",
            True, COLORS['white']
        )
        self.screen.blit(text, (10, 10))
        
    def run(self):
        running = True
        while running:
            self.screen.fill(COLORS['dark_gray'])
            
            if not self.handle_events():
                break
                
            if not self.update():
                print("Game Over!")
                break
                
            # Отрисовка
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            for bullet in self.bullets:
                bullet.draw(self.screen)
            self.draw_esp()
            self.draw_interface()
            
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()