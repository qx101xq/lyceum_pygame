import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
class ImageButton:
    def __init__(self, x, y, width, height, text, image_path, after_image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        if after_image_path:
            self.after_image = pygame.image.load(after_image_path)
            self.after_image = pygame.transform.scale(self.after_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mouse_on = False


    def draw(self, screen):
        current_image = self.after_image if self.mouse_on else self.image
        screen.blit(current_image, self.rect.topleft)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_mouse(self, mouse_pos):
        self.mouse_on = self.rect.collidepoint(mouse_pos)

    def event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.mouse_on:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))