# ------------ game.py ------------
import pygame
import math
import random
from player import Player
from enemy import Enemy
from bullet import Bullet
from game_map import Map
from camera import Camera
from powerups import PowerUp
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Мега-Крутая ESP Игра!")
        self.clock = pygame.time.Clock()
        self.map = Map()
        self.camera = Camera()
        self.player = Player(self.map)
        self.enemies = []
        self.bullets = []
        self.powerups = []
        self.spawn_wave()
        
    def spawn_wave(self):
        for _ in range(ENEMIES_PER_WAVE + self.player.wave * 2):
            x = random.randint(100, self.map.width - 100)
            y = random.randint(100, self.map.height - 100)
            while any(abs(x - e.x) < 100 and abs(y - e.y) < 100 for e in self.enemies):
                x = random.randint(100, self.map.width - 100)
                y = random.randint(100, self.map.height - 100)
            self.enemies.append(Enemy(x, y, self.player.wave))
            
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.shoot()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    self.player.switch_weapon()
                    pygame.mixer.Sound("switch.wav").play()
        return True
    
    def shoot(self):
        weapon_name = self.player.weapons[self.player.current_weapon]
        weapon = WEAPONS[weapon_name]
        now = pygame.time.get_ticks()
    
        if now - self.player.last_shot > weapon['cooldown']:
            mx, my = pygame.mouse.get_pos()
            target_x = mx + self.camera.x  # Переменные объявлены внутри условия!
            target_y = my + self.camera.y  # Теперь они точно существуют
        
            if weapon_name == 'shotgun':
                for _ in range(5):
                    spread = random.uniform(-0.2, 0.2)
                    self.bullets.append(Bullet(
                        self.player.x, self.player.y,
                        target_x + spread * 100, 
                        target_y + spread * 100,
                        weapon['damage']
                    ))
            else:
                self.bullets.append(Bullet(
                    self.player.x, self.player.y,
                    target_x, target_y,
                    weapon['damage']
                ))
        self.player.last_shot = now 
            
    def check_collisions(self):
        # Столкновение игрока с препятствиямwи
        player_rect = pygame.Rect(
            self.player.x - self.player.size//2,
            self.player.y - self.player.size//2,
            self.player.size, self.player.size
        )
        
        for obstacle in self.map.obstacles:
            if player_rect.colliderect(obstacle):
                # Выталкивание игрока
                if self.player.x < obstacle.left:
                    self.player.x = obstacle.left - self.player.size//2
                elif self.player.x > obstacle.right:
                    self.player.x = obstacle.right + self.player.size//2
                if self.player.y < obstacle.top:
                    self.player.y = obstacle.top - self.player.size//2
                elif self.player.y > obstacle.bottom:
                    self.player.y = obstacle.bottom + self.player.size//2
                    
    def update(self):
        keys = pygame.key.get_pressed()
        self.player.move(keys)
        self.check_collisions()
        self.camera.update(self.player)
        
        # Обновление врагов и проверка столкновений
        for enemy in self.enemies[:]:
            enemy.update(self.player, self.bullets)
            if enemy.health <= 0:
                self.enemies.remove(enemy)
                self.player.score += 100 * self.player.wave
                if random.random() < 0.2:
                    self.powerups.append(PowerUp(enemy.x, enemy.y, 
                        random.choice(['health', 'speed'])))

        for powerup in self.powerups[:]:
            if math.hypot(self.player.x - powerup.x, self.player.y - powerup.y) < 30:
                if powerup.type == 'health':
                    self.player.heal(50)
                elif powerup.type == 'speed':
                    self.player.speed *= 1.5  # Ускорение на 5 секунд
                    pygame.time.set_timer(pygame.USEREVENT, 5000)  # Сброс через 5 сек
                self.powerups.remove(powerup)         
        # Обновление пуль
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.x < 0 or bullet.x > self.map.width or bullet.y < 0 or bullet.y > self.map.height:
                self.bullets.remove(bullet)
                continue
                
            # Попадание по врагам
            for enemy in self.enemies[:]:
                if bullet.check_hit(enemy):
                    enemy.take_damage(bullet.damage)
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                    self.bullets.remove(bullet)
                    break
                    
        # Проверка волн
        if not self.enemies:
            self.player.wave += 1
            self.spawn_wave()
            
        return self.player.health > 0
    
    def draw(self):
        self.screen.fill(COLORS['dark_gray'])
        self.map.draw(self.screen, self.camera)
        
        # Отрисовка игрока
        screen_x = self.player.x - self.camera.x
        screen_y = self.player.y - self.camera.y
        pygame.draw.circle(self.screen, COLORS['blue'], (int(screen_x), int(screen_y)), self.player.size)
            
        # Отрисовка врагов
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera)
            
        # Отрисовка пуль и бонусов
        for bullet in self.bullets:
            bullet.draw(self.screen, self.camera)
        for powerup in self.powerups:
            powerup.draw(self.screen, self.camera)
            
        # Интерфейс
        self.draw_interface()
        
    def draw_interface(self):
     # Добавьте создание шрифта
        font = pygame.font.Font(None, 36)
    
        text = f"Score: {self.player.score} | HP: {int(self.player.health)} | Wave: {self.player.wave}"
        text += f" | Weapon: {self.player.weapons[self.player.current_weapon]}"
    
        render = font.render(text, True, COLORS['white'])
        self.screen.blit(render, (10, 10))
        
    def show_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, COLORS['red'])
        self.screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 50))
        pygame.display.update()
        pygame.time.wait(3000)


    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)
            
            if not self.handle_events():
                break
                
            if not self.update():
                self.show_game_over()
                break
                
            self.draw()
            pygame.display.update()
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()