import pygame
import random
import math
width = 800
height = 600
score = 0
back = pygame.display.set_mode((width, height))

class Cloud:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        scale = random.uniform(0.3, 0.6)
        self.image.set_alpha(220)
        self.image = pygame.transform.scale(
            self.image,
            (
                int(self.image.get_width() * scale),
                int(self.image.get_height() * scale)
            )
        )

        self.x = random.randint(0, 800)
        self.y = random.randint(-self.image.get_height(), 600)

        self.offset = random.uniform(0, math.pi * 2)
        self.speed = random.uniform(0.5, 1.5)

    def move(self):
        self.x += self.speed
        if self.x > 900:
            self.x = -self.image.get_width()
            self.y = random.randint(-self.image.get_height(), 600)
            self.offset = random.uniform(0, math.pi * 2)

    def draw(self, surface):
        wave = math.sin(pygame.time.get_ticks() / 1000 + self.offset) * 5
        y = self.y + wave
        surface.blit(self.image, (self.x, y))

class Rain:
    def __init__(self):
        self.x = random.randint(0, 800)
        self.y = random.randint(-600, 0)
        self.length = random.randint(10, 20)
        self.speed = random.uniform(4, 10)
        self.color = (180, 180, 255)

    def fall(self):
        self.y += self.speed
        if self.y > 600:
            self.y = random.randint(-100, -10)
            self.x = random.randint(0, 800)

    def draw(self, surface):
        pygame.draw.line(surface, self.color, (self.x, self.y), (self.x, self.y + self.length), 1)



class Flower:
    def __init__(self, image_path):
        self.image = pygame.image.load(image_path).convert_alpha()
        scale = random.uniform(0.1, 0.2)
        self.image = pygame.transform.scale(self.image, (
            int(self.image.get_width() * scale),
            int(self.image.get_height() * scale)
        ))
        self.x = random.randint(0, 800)
        self.y = random.randint(-600, 0)
        self.speed_y = random.uniform(0.5, 1.5)
        self.speed_x = random.uniform(-0.5, 0.5)
        self.angle = 0
        self.rotation_speed = random.uniform(-1, 1)

    def fall(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.angle += self.rotation_speed

        if self.y > 600:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, 800)

    def draw(self, surface):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect.topleft)

lab_map = [
    [3, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 2, 1],
]

lab_map_2 = [
    [3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
]

lab_map_3 = [
    [3, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1],
]


lab_map_4 = [
    [3, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 2, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 2, 1],
    [1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1],
]

CELL_SIZE = 38
OFFSET_X, OFFSET_Y = 160, 19


def draw_lab(surface, lab):
    wall_color =(255, 255, 255)
    rows = len(lab)
    cols = len(lab[0])

    for y in range(rows):
        for x in range(cols):
            if lab[y][x] == 1:
                cx = OFFSET_X + x * CELL_SIZE
                cy = OFFSET_Y + y * CELL_SIZE

                if y == 0 or lab[y-1][x] == 0:
                    pygame.draw.line(surface, wall_color, (cx, cy), (cx + CELL_SIZE, cy), 2)
                if y == rows - 1 or lab[y+1][x] == 0:
                    pygame.draw.line(surface, wall_color, (cx, cy + CELL_SIZE), (cx + CELL_SIZE, cy + CELL_SIZE), 2)
                if x == 0 or lab[y][x-1] == 0:
                    pygame.draw.line(surface, wall_color, (cx, cy), (cx, cy + CELL_SIZE), 2)
                if x == cols - 1 or lab[y][x+1] == 0:
                    pygame.draw.line(surface, wall_color, (cx + CELL_SIZE, cy), (cx + CELL_SIZE, cy + CELL_SIZE), 2)


def find_spawn_point(lab_map):
    for y, row in enumerate(lab_map):
        for x, cell in enumerate(row):
            if cell == 0:
                px = OFFSET_X + x * CELL_SIZE
                py = OFFSET_Y + y * CELL_SIZE
                return px, py
    return 0, 0