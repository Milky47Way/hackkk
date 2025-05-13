import pygame
import random

width = 800
height = 600
back = pygame.display.set_mode((width, height))

CELL_SIZE = 37
OFFSET_X, OFFSET_Y = 215, 14

pygame.init()

def load_font(path, size):
    return pygame.font.Font(path, size)

def load_fonts():
    font_path = 'res/JosefinSans-SemiBold.ttf'
    font8 = load_font(font_path, 36)
    font9 = load_font(font_path, 20)
    font10 = load_font(font_path, 24)
    return font8, font9, font10

font8, font9, font10 = load_fonts()

class Coin (pygame.sprite.Sprite):
    def __init__(self, x, y, coin_type='gold'):
        super().__init__()
        self.type = coin_type

        if self.type == 'gold':
            self.image = pygame.image.load('img/coin.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.value = 1

        elif self.type == 'silver':
            self.image = pygame.image.load('img/star.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (35, 35))
            self.value = 2

        elif self.type == 'diamond':
            self.image = pygame.image.load('img/paw.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (45, 55))
            self.value = 5

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def generate_random_coins(lab_map, count):
    coin_types = ['gold', 'silver', 'diamond']
    coins = []
    empty_cells = [(x, y) for y, row in enumerate(lab_map) for x, cell in enumerate(row) if cell == 0]
    random.shuffle(empty_cells)
    for i in range(min(count, len(empty_cells))):
        x, y = empty_cells[i]
        px = OFFSET_X + x * CELL_SIZE + 9
        py = OFFSET_Y + y * CELL_SIZE + 9
        ctype = random.choice(coin_types)
        coins.append(Coin(px, py, ctype))
    return coins

