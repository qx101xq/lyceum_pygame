# torch.py
import pygame

# Загрузка анимации факела
torch_images = [pygame.image.load(f"source/torch/t{i}.png") for i in range(1, 6)]  # допустим, 5 кадров для факела

class Torch:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = 0
        self.image = torch_images[self.index]
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        # Анимация факела
        self.index += 0.1
        if self.index >= len(torch_images):
            self.index = 0
        self.image = torch_images[int(self.index)]

    def draw(self, screen):
        screen.blit(self.image, self.rect)