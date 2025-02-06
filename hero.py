import pygame

# Загрузка спрайтов анимации героя
hero_images = [pygame.image.load(f"source/pers/pers_{i}.png") for i in range(1, 8)]

class Hero:
    def __init__(self, x, y, screen_width):
        self.initial_x = x
        self.initial_y = y
        self.x = x
        self.y = y
        self.index = 0  # Начинаем с первого спрайта
        self.image = hero_images[self.index]
        self.speed = 2
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.direction = 1  # 1 - вправо, -1 - влево
        self.moving = False
        self.screen_width = screen_width  # Добавляем ширину экрана
        self.distance_traveled = 0  # Пройденное расстояние (учитывая направление)
        self.angle = 0  # Угол поворота

    def update(self, keys):
        prev_x = self.x  # Запоминаем предыдущую позицию
        self.moving = False

        if keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.direction = -1
            self.moving = True
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.direction = 1
            self.moving = True

        # Учитываем направление при подсчёте пройденного пути
        self.distance_traveled += (self.x - prev_x)

        # Проверка выхода за границы карты
        if self.x > self.screen_width:
            self.x = 0  # Перемещаем в начало
        elif self.x < 0:
            self.x = self.screen_width  # Перемещаем в конец

        # Обновление анимации только при движении
        if self.moving:
            self.index += 0.1
            if self.index >= len(hero_images):
                self.index = 0
        else:
            self.index = 0  # При остановке возвращаем индекс к 0 (первый спрайт)

        self.image = hero_images[int(self.index)]

        # Отражение при смене направления
        if self.direction == -1:
            self.image = pygame.transform.flip(self.image, True, False)

        # Поворот изображения
        if self.angle != 0:
            self.image = pygame.transform.rotate(self.image, self.angle)

        # Обновление позиции
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def get_distance(self):
        return self.distance_traveled  # Возвращает пройденное расстояние с учётом направления

    def rotate(self, angle):
        self.angle = angle  # Устанавливаем угол поворота

    def set_sprite(self, index):
        self.index = index  # Устанавливаем индекс спрайта