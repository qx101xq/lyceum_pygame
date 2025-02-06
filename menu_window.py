import pygame
import sys
from imgbutton import ImageButton

# Инициализация Pygame
pygame.init()

size = WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode(size)
screen.fill((255, 255, 255))
pygame.display.set_caption("Menu")
background = pygame.image.load("source/menu/background.jpeg")


btn1 = ImageButton(WIDTH/2 - (400/2), 200, 400, 180, "PLAY", "source/menu/btn1.png", "source/menu/btn2.png")
btn2 = ImageButton(WIDTH/2 - (400/2), 300, 400, 180, "EXIT", "source/menu/btn1.png", "source/menu/btn2.png")
def main():
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(background, (0, -350))

        font = pygame.font.Font(None, 70)
        text_surface = font.render("GRAYLAND", True, 'white')
        text_rect = text_surface.get_rect(center=(WIDTH/2, 100))
        screen.blit(text_surface, text_rect)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.USEREVENT and event.button == btn1:
                print('you pushed play button')
            #  логика
            btn1.event(event)
            btn2.event(event)
        btn1.check_mouse(pygame.mouse.get_pos())
        btn1.draw(screen)
        btn2.check_mouse(pygame.mouse.get_pos())
        btn2.draw(screen)
        pygame.display.flip()