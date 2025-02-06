import pygame
import random
from hero import Hero
from spider import Spider
from ball import Ball, ball_images
from torch import Torch
from imgbutton import ImageButton

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 640, 480
FPS = 60
NUM_TORCHES = 3  # Количество факелов

# Функция для запуска игрового уровня
def run_game():
    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pygame Level")

    # Загрузка фона
    background = pygame.image.load("source/lv.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    # Создание героя
    hero = Hero(0, 308, WIDTH)

    # Ширина каждого факела
    torch_width = 40  # Примерная ширина факела

    # Расположение факелов
    torch_spacing = (WIDTH - NUM_TORCHES * torch_width) // (NUM_TORCHES + 1)

    # Создание факелов
    torches = [Torch(torch_spacing * (i + 1) + i * torch_width, 200) for i in range(NUM_TORCHES)]

    # Счетчик пройденного расстояния для спавна паука
    spawn_distance = 0

    # Переменная для отслеживания спавна паука
    spider_spawned = False
    spider = None  # Пока паука нет

    # Счетчик касаний героя с пауком
    collision_count = 0

    # Счетчик касаний шара с пауком
    ball_collision_count = 0

    # Переменная для отслеживания состояния игры
    game_over = False
    game_over_timer = 0

    # Список для хранения шаров
    balls = []

    # Таймер для блокировки кнопки
    last_ball_time = 0

    # Игровой цикл
    running = True
    clock = pygame.time.Clock()
    while running:
        clock.tick(FPS)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Получение нажатых клавиш
            keys = pygame.key.get_pressed()

            # Создание шара при нажатии клавиши F
            current_time = pygame.time.get_ticks()
            if keys[pygame.K_f] and (current_time - last_ball_time > 1000):
                ball_image = random.choice(ball_images)
                direction = hero.direction  # Направление движения шара совпадает с направлением взгляда героя
                ball_x = hero.x + direction * 20  # Позиция шара в 20 единицах от героя
                ball = Ball(ball_x, hero.y, ball_image, direction)
                balls.append(ball)
                last_ball_time = current_time  # Обновляем время последнего создания шара

            # Запоминаем старые координаты
            previous_x = hero.x

            # Обновляем героя
            hero.update(keys)

            # Ограничение движения влево, если пройденное расстояние < 480
            if hero.get_distance() < 480 and keys[pygame.K_LEFT]:
                hero.x = previous_x  # Возвращаем героя на старую позицию

            # Обновляем счетчик пройденного расстояния (только если движение было)
            spawn_distance += abs(hero.x - previous_x)

            # Спавн паука только один раз при прохождении WIDTH * 3
            if (spawn_distance >= WIDTH * 1 or spawn_distance >= WIDTH * 3) and hero.x == 10 and not spider_spawned:
                spider = Spider(hero.x + 350, 275)  # Создаём паука на нужной позиции
                spider_spawned = True  # Фиксируем, что паук уже создан

            # Если паук создан, обновляем его движение
            if spider:
                spider.update(hero.x, hero.y)  # Передаем координаты героя в update

                # Проверка расстояния между героем и пауком
                distance = abs(hero.x - spider.x)
                if distance < 15:
                    # Отскок героя и паука на 10 единиц назад
                    if hero.x < spider.x:
                        hero.x -= 30
                        spider.x += 60
                    else:
                        hero.x += 30
                        spider.x -= 60

                    # Увеличиваем счетчик касаний
                    collision_count += 1

                    # Если произошло 3 касания
                    if collision_count >= 3:
                        # Останавливаем паука
                        spider.stop()
                        # Переворачиваем героя на 90 градусов
                        hero.rotate(90)
                        # Переключаем на пятый спрайт
                        hero.set_sprite(5)
                        # Устанавливаем состояние игры как "GAME OVER"
                        game_over = True
                        game_over_timer = pygame.time.get_ticks()

            # Обновление анимации факелов
            for torch in torches:
                torch.update()

            # Обновление шаров
            for ball in balls:
                ball.update()
                if ball.collides_with(spider):
                    balls.remove(ball)
                    ball_collision_count += 1
                    if ball_collision_count >= 3:
                        spider.start_fade()
                    # Отскок паука
                    direction = 1 if ball.x < spider.x else -1
                    spider.bounce(direction)
                elif ball.is_off_screen():
                    balls.remove(ball)

            # Удаление паука, если он полностью исчез
            if spider and spider.alpha <= 0:
                spider.stop_fade()
                spider = None
                spider_spawned = False
                ball_collision_count = 0

        # Отрисовка
        screen.blit(background, (0, 0))
        hero.draw(screen)

        # Рисуем факелы
        for torch in torches:
            torch.draw(screen)

        # Рисуем паука, если он есть
        if spider:
            spider.draw(screen)

        # Рисуем шары
        for ball in balls:
            ball.draw(screen)

        # Если игра окончена, затемняем экран и отображаем надпись "GAME OVER!"
        if game_over:
            # Затемнение экрана
            dark_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            dark_surface.fill((0, 0, 0, 128))
            screen.blit(dark_surface, (0, 0))

            # Отображение надписи "GAME OVER!"
            if pygame.time.get_ticks() - game_over_timer > 5000:
                font = pygame.font.Font(None, 74)
                text = font.render("GAME OVER!", True, (255, 0, 0))
                screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()

    pygame.quit()

# Основное меню
def main_menu():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Menu")
    background = pygame.image.load("source/menu/background.jpeg")

    btn1 = ImageButton(WIDTH/2 - (400/2), 200, 400, 180, "PLAY", "source/menu/btn1.png", "source/menu/btn2.png")
    btn2 = ImageButton(WIDTH/2 - (400/2), 300, 400, 180, "EXIT", "source/menu/btn1.png", "source/menu/btn2.png")

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
                run_game()  # Запуск игры при нажатии кнопки "Play"
            if event.type == pygame.USEREVENT and event.button == btn2:
                running = False
                pygame.quit()
            btn1.event(event)
            btn2.event(event)

        btn1.check_mouse(pygame.mouse.get_pos())
        btn1.draw(screen)
        btn2.check_mouse(pygame.mouse.get_pos())
        btn2.draw(screen)
        pygame.display.flip()

# Запуск основного меню
main_menu()