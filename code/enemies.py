import pygame

img_enemy1 = 'img/Picsart_25-05-07_20-43-17-253.png'
img_enemy2 = 'img/Picsart_25-05-07_21-56-10-755.png'
img_enemy3 = 'img/Picsart_25-05-07_22-44-04-341.png'

img_enemy6 = 'img/game3/dra.png'
img_enemy7 = 'img/game3/akss.png'

img_enemy4 = 'img/game5/rabb.png'
img_enemy5 = 'img/game5/foxx.png'

tile_size = 40
clock = pygame.time.Clock()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, path, image_path, size, speed):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.start_x, self.end_x = path
        self.speed = speed
        self.direction = 1
        self.pos_x = float(x)

    def update(self):
        self.pos_x += self.speed * self.direction

        if self.pos_x >= self.end_x:
            self.pos_x = self.end_x
            self.direction = -1
        elif self.pos_x <= self.start_x:
            self.pos_x = self.start_x
            self.direction = 1

        self.rect.x = int(self.pos_x)