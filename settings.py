# hehe
WIDTH = 1600
HEIGHT = 1200
FPS = 60
ENEMIES_PER_WAVE = 8
PLAYER_SPEED = 7
BULLET_SPEED = 15
TILE_SIZE = 64
COLORS = {
    'white': (255, 255, 255),
    'red': (255, 0, 0),
    'blue': (0, 128, 255),
    'yellow': (255, 255, 0),
    'dark_gray': (25, 25, 25),
    'green': (0, 200, 0),
    'grass': (34, 139, 34),
    'wall': (100, 100, 100)
}

ENEMY_EMOJIS = {
    'normal': '😈',
    'fast': '👻',
    'tank': '💀'
}

WEAPONS = {
    'pistol': {'cooldown': 300, 'damage': 25},
    'shotgun': {'cooldown': 1000, 'damage': 50},
    'machinegun': {'cooldown': 100, 'damage': 15}
}