import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800,600
screen = pygame.display.set_mode ((WIDTH, HEIGHT))
pygame.display.set_caption("openh3ck v0.1")
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
class Player:
    def __init__(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = random.randint(50, HEIGHT - 50)
        self.health = random.randint(1, 100)
        self.team = random.choice(["Sharks", "Hunters"])

players = [Player() for _ in range(5)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    # Render players
    for player in players:
        color = RED if player.team == "Hunters" else GREEN
        pygame.draw.circle(screen, color, (player.x, player.y), 20)

        # Wallhack
        box_width, box_height = 40, 60
        box_x = player.x - box_width // 2
        box_y = player.y - box_height // 2
        pygame.draw.rect(screen, WHITE, (box_x, box_y, box_width, box_height), 2)

        health_bar_width = 30
        health_x = player.x - health_bar_width // 2
        health_y = box_y - 10
        pygame.draw.rect(screen, RED, (health_x, health_y, health_bar_width, 5))
        pygame.draw.rect(screen, GREEN, (health_x, health_y, health_bar_width * (player.health / 100), 5))

    # Trigger
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for player in players:
        distance = ((mouse_x - player.x)**2 + (mouse_y - player.y)**2)**0.5
        if distance < 20:
            print("Shot! :", player.team)

    pygame.display.flip()

pygame.quit()