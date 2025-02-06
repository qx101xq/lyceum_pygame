import pygame

# Загрузка спрайтов для шаров
ball_images = [pygame.image.load(f"source/ball/ball{i}.png") for i in range(1, 4)]

class Ball:
    def __init__(self, x, y, image, direction):
        self.x = x
        self.y = y
        self.image = image
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 5  # Скорость движения шара
        self.direction = direction  # Направление движения шара

    def update(self):
        self.x += self.speed * self.direction  # Двигаем шар вдоль оси X
        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def collides_with(self, spider):
        if spider:
            return self.rect.colliderect(spider.rect)
        return False

    def is_off_screen(self):
        return self.x < -100 or self.x > 700  # Проверяем, вышел ли шар за границы экрана