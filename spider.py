import pygame

# Размеры увеличенного паука
SPIDER_WIDTH, SPIDER_HEIGHT = 200, 80  # Можно настроить под нужные размеры

# Загрузка и увеличение спрайтов паука
spider_images = [
    pygame.transform.scale(
        pygame.image.load(f"source/spider/sp{i}.png"), (SPIDER_WIDTH, SPIDER_HEIGHT)
    )
    for i in range(1, 5)
]

class Spider:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = 0  # Индекс текущего кадра анимации
        self.image = spider_images[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.animation_speed = 0.1  # Скорость анимации
        self.moving = True  # Флаг для движения паука
        self.alpha = 255  # Прозрачность паука
        self.fading = False  # Флаг для плавного исчезновения
        self.fade_speed = 510  # Скорость исчезновения (255 / 0.5 секунды = 510)
        self.distance_traveled = 0  # Пройденное расстояние

    def update(self, hero_x, hero_y):
        if self.moving:
            # Двигаем паука в сторону героя
            if self.x < hero_x:
                self.x += 1  # Двигаем вправо к герою
            elif self.x > hero_x:
                self.x -= 1  # Двигаем влево к герою

            # Увеличиваем пройденное расстояние
            self.distance_traveled += 1

        # Обновление анимации
        self.index += self.animation_speed
        if self.index >= len(spider_images):
            self.index = 0
        self.image = spider_images[int(self.index)]

        # Обновляем прямоугольник (для обработки столкновений)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Плавное исчезновение
        if self.fading:
            self.alpha = max(0, self.alpha - self.fade_speed * 1/60)
            self.image.set_alpha(self.alpha)

    def draw(self, screen):
        if self.alpha > 0:  # Рисуем только если прозрачность больше 0
            screen.blit(self.image, self.rect)

    def stop(self):
        self.moving = False  # Останавливаем движение паука

    def start_fade(self):
        self.fading = True  # Начинаем плавное исчезновение

    def stop_fade(self):
        self.fading = False  # Останавливаем плавное исчезновение
        self.alpha = 255  # Восстанавливаем прозрачность

    def bounce(self, direction):
        # Отскок паука в зависимости от направления столкновения
        self.x += direction * 120