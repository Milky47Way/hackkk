import pygame
CELL_SIZE = 37
OFFSET_X, OFFSET_Y = 220, 23

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size, screen_width, screen_height, speed=5):
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height

    def handle_input(self, lab_map):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy = self.speed

        old_x, old_y = self.rect.topleft

        self.rect.x += dx
        if self.collides_with_walls(lab_map) or not self.on_screen():
            self.rect.x = old_x

        self.rect.y += dy
        if self.collides_with_walls(lab_map) or not self.on_screen():
            self.rect.y = old_y

    def update(self, lab_map):
        self.handle_input(lab_map)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def collides_with_walls(self, lab_map):
        rows = len(lab_map)
        cols = len(lab_map[0])
        for y in range(rows):
            for x in range(cols):
                if lab_map[y][x] == 1:
                    wall_rect = pygame.Rect(
                        OFFSET_X + x * CELL_SIZE,
                        OFFSET_Y + y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE
                    )
                    if self.rect.colliderect(wall_rect):
                        return True
        return False

    def on_screen(self):
        return (0 <= self.rect.left < self.screen_width and
                0 <= self.rect.top < self.screen_height and
                self.rect.right <= self.screen_width and
                self.rect.bottom <= self.screen_height)