import pygame
import sys
import os
from PIL import Image
from lab import  lab_map, lab_map_2, lab_map_3, lab_map_4, draw_lab, Cloud, Rain, Flower, find_spawn_point
from coin import Coin, generate_random_coins
from hero import Player
from enemies import Enemy, img_enemy1, img_enemy2, img_enemy3, img_enemy4, img_enemy5
pygame.init()
pygame.mixer.init()
CELL_SIZE = 38
OFFSET_X, OFFSET_Y = 160, 19

#таймер
start_ticks = pygame.time.get_ticks()
time_limit = 25 * 60

#музика та ефекти
music_on = True
music_path = os.path.join(os.path.dirname(__file__), "res/sounds/The Cascades - Rhythm of the Rain.mp3")

def toggle_music():
    global music_on
    if music_on:
        pygame.mixer.music.pause()
        music_on = False
    else:
        pygame.mixer.music.unpause()
        music_on = True

def load_music():
    try:
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1, 0.0)
        print("Music loaded and playing")
    except pygame.error as e:
        print("Could not load music:", e)

        pygame.display.update()

#віконце.Лабіринт
def open_que():
    global show_lab_info
    show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(75, 108, 94))
    show_lab_info = not show_lab_info

def open_menu():
    global show_menu_info
    show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(75, 108, 94))
    show_menu_info = not show_menu_info

def show_queue_window(filename, width=300, height=300, x=None, y=150, bg_color=(137, 167, 200)):
    queue_window = pygame.Surface((width, height))
    queue_window.fill(bg_color)

    font4 = pygame.font.SysFont('Verdana', 13)
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        lines = ["Файл не знайдено."]

    oy = 10
    for line in lines:
        text = font4.render(line.strip(), True, (50, 50, 50))
        queue_window.blit(text, (10, oy))
        oy += text.get_height() + 6

    if x is None:
        screen_rect = back.get_rect()
        x = screen_rect.centerx - width // 2

    back.blit(queue_window, (x, y))
    pygame.display.update()

    window_open = True
    while window_open:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                window_open = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                window_open = False
        pygame.display.update()

def show_level_complete_window(level):
    screen = pygame.display.set_mode((800, 600))
    screen.fill((63, 91, 120))  #


    if level == 1:
        image_surface = game12_bg
    elif level == 2:
        image_surface = game22_bg
    elif level == 3:
        image_surface = game33_bg
    elif level == 4:
        image_surface = game44_bg
    elif level == 5:
        image_surface = game55_bg
    else:
        image_surface = None

    if image_surface:
        img = pygame.transform.scale(image_surface, (800, 600))
        screen.blit(img, (0, 0))

    pygame.display.update()


    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                waiting = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                waiting = False


def end_game():
    start_backk()
    pygame.quit()
    sys.exit()

def draw_timer(surface, text_alpha=255):
    global start_ticks, time_limit
    elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
    remaining = max(0, time_limit - elapsed)
    minutes = remaining // 60
    seconds = remaining % 60
    timer_text = font9.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))

    timer_surface = pygame.Surface(timer_text.get_size(), pygame.SRCALPHA)
    timer_surface.blit(timer_text, (0, 0))
    timer_surface.set_alpha(text_alpha)
    surface.blit(timer_surface, (width - 780, 50))

    if remaining == 0:
        end_game()

#монетки
score = 0
last_coin_type = None

def add_score(points):
    global score
    score += points

def draw_score(surface):
    color = (255, 255, 255)
    if last_coin_type == 'gold':
        color = (255, 215, 0)
    elif last_coin_type == 'silver':
        color = (192, 192, 192)
    elif last_coin_type == 'diamond':
        color = (0, 255, 255)

    score_text = font10.render(f"Score: {score}", True, (255, 255, 0))
    surface.blit(score_text, (20, 20))

#Зображення
def load_tif_image(path, size):
    img = Image.open(path)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    data = img.tobytes()
    surface = pygame.image.fromstring(data, img.size, img.mode)
    return pygame.transform.smoothscale(surface, size)

def load_images():
    main_menu_bg = load_tif_image('img/Цей бешкетник може бути де завгодно! (1).tif', (800, 600))
    menu_game_bg = load_tif_image('img/menu_game.tif', (800, 600))
    game1_bg = load_tif_image('img/game1/lab_one.tif', (800, 600))
    game12_bg = load_tif_image('img/game1/game.back1.tif', (800, 600))
    game2_bg = load_tif_image('img/game2/game2.tif', (800, 600))
    game22_bg = load_tif_image('img/game2/game.back2.tif', (800, 600))
    game3_bg = load_tif_image('img/game3/game3.tif', (800, 600))
    game33_bg = load_tif_image('img/game3/game.back3.tif', (800, 600))
    game4_bg = load_tif_image('img/game4/game4.tif', (800, 600))
    game44_bg = load_tif_image('img/game4/game.back4.tif', (800, 600))
    game5_bg = load_tif_image('img/game5/game5.tif', (800, 600))
    game55_bg = load_tif_image('img/game5/game.final.tif', (800, 600))
    return main_menu_bg, menu_game_bg, game1_bg, game2_bg, game3_bg, game4_bg, game5_bg, game12_bg, game22_bg, game33_bg, game44_bg, game55_bg

main_menu_bg, main_game_bg, game1_bg, game2_bg, game3_bg, game4_bg, game5_bg, game12_bg, game22_bg, game33_bg, game44_bg, game55_bg = load_images()

#сцена
width = 800
height = 600
back = pygame.display.set_mode((width, height))

pygame.display.set_caption('Cat Trail')
icon = pygame.image.load('img/cat_inf.png')
pygame.display.set_icon(icon)

#шрифт
import pygame
def load_font(path, size):
    return pygame.font.Font(path, size)

def load_fonts():
    font_path = 'res/JosefinSans-SemiBold.ttf'
    font8 = load_font(font_path, 36)
    font9 = load_font(font_path, 20)
    font10 = load_font(font_path, 24)
    return font8, font9, font10

font8, font9, font10 = load_fonts()

#змінні
white = (255, 255, 255)
black = (0,0,0)
gray = (200, 200, 200)
total_score = 0
box = pygame.Rect(50, 500, 700, 50)
color_inactive = gray
color_active = (0, 255, 0)
color = color_inactive
active = False
text = ''
chat_history = []
tile_size = 40
show_lab_info = False
show_menu_info = False

#вороги
enemy1 = Enemy(0, 512, (200, 250), img_enemy1, (40,40), (0.1))
enemy2 = Enemy(102, 400, (520, 570), img_enemy2, (50,40), (0.1))
enemy3 = Enemy(92, 320, (320, 370), img_enemy3, (40,40), (0.1))
enemy4 = Enemy(92, 320, (320, 370), img_enemy4, (40,40), (0.1))
enemy5 = Enemy(92, 320, (320, 370), img_enemy5, (40,40), (0.1))

enemies_by_level = {
    1: pygame.sprite.Group(enemy1, enemy2, enemy3),
    2: pygame.sprite.Group(enemy1, enemy4),
    3: pygame.sprite.Group(enemy1, enemy4),
    4: pygame.sprite.Group(enemy4, enemy5),
    5: pygame.sprite.Group(enemy4, enemy5),
}


#герой
spawn_x, spawn_y = find_spawn_point(lab_map)
player1 = Player(spawn_x, spawn_y, "img/hero.png", (20, 33), width, height, 5)

spawn_x1, spawn_y1 = find_spawn_point(lab_map_2)
player2 = Player(spawn_x1, spawn_y1, "img/hero.png", (20, 33), width, height, 4)

spawn_x2, spawn_y2 = find_spawn_point(lab_map_3)
player3 = Player(spawn_x2, spawn_y2, "img/hero.png", (20, 33), width, height, 3)

spawn_x3, spawn_y3 = find_spawn_point(lab_map_4)
player4 = Player(spawn_x3, spawn_y3, "img/hero.png", (20, 30), width, height, 5)

spawn_x4, spawn_y4 = find_spawn_point(lab_map)
player5 = Player(spawn_x4, spawn_y4, "img/hero.png", (20, 33), width, height, 5)


#кнопки
def draw_button(text, x, y, w, h, base_color, hover_color, action=None, alpha=255, border_radius=0):
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    current_color = hover_color if rect.collidepoint(mouse_pos) else base_color

    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    color_with_alpha = (*current_color, alpha)
    pygame.draw.rect(button_surface, color_with_alpha, button_surface.get_rect(), border_radius=border_radius)
    button_surface.fill((*current_color, alpha))
    back.blit(button_surface, (x, y))

    text_surface = font9.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    back.blit(text_surface, text_rect)

    if action and pygame.mouse.get_pressed()[0] and rect.collidepoint(mouse_pos):
        action()

def draw_circle_button(text, x, y, radius, color, action=None, alpha=0):
    circle_surface = pygame.Surface((radius *  2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(circle_surface, (*color,alpha), (radius, radius), radius)
    back.blit(circle_surface, (x - radius, y - radius))

    text_surface = font9.render(text, True, (158, 189, 230))
    text_rect = text_surface.get_rect(center=(x, y))
    back.blit(text_surface, text_rect)

    for event in pygame.event.get(pygame.MOUSEBUTTONDOWN):

        if event.button == 1:
            mouse_x, mouse_y = event.pos
            if (mouse_x - x) ** 2 + (mouse_y - y) ** 2 <= radius**2:
                if action:
                    action()

#функції для кнопок
def start_game():
    start_backk()

def info_game():
    info_back()

def settings_game():
    settings_back()

#меню
def return_to_main_menu():
    main_menu()

def main_menu():
    while True:
        back.fill(white)
        back.blit(main_menu_bg, (0, 0))
        button_x = width - 220
        buttonSet_y = 450

        buttonI_y = 300
        buttonS_y = 150

        button_w = 180
        button_h = 60

        draw_button("Start", button_x, buttonS_y, button_w, button_h, (116, 122, 82), (156, 162, 118), start_backk, 255, 0)
        draw_button("Info", button_x, buttonI_y, button_w, button_h, (137, 97, 111), (170, 131, 144), info_back, 255, 0)
        draw_button("Settings", button_x, buttonSet_y, button_w, button_h, (200, 150, 100), (213, 171, 129), settings_back, 255, 0)

        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            print("Info")
                            sys.exit()

        pygame.display.update()

#меню ігр
def start_backk():
    while True:

        back.blit(main_game_bg,(0,0))
        draw_timer(back, text_alpha=0)
        #back.fill((240, 240, 240))
        font_big = pygame.font.SysFont(None, 80)
        text = font_big.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)

        draw_button('Menu', width // 2 + 133, height // 2 + 175, 250, 75, (63, 103, 55), (200, 200, 200), return_to_main_menu, 30, 22)
        draw_button('', width // 2 - 375, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), game_one, 18)
        draw_button('', width // 2 - 113, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), game_two, 18)
        draw_button('', width // 2 + 149, height // 2 - 242, 220, 220, (100, 200, 100), (63, 103, 55), game_four, 12)

        draw_button("", width // 2 - 113, height // 2 + 33 , 220, 220, (100, 200, 100), (63, 103, 55), game_five, 18)
        draw_button("", width // 2 - 375, height // 2 + 33, 220, 220, (100, 200, 100), (63, 103, 55),game_three , 18)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

#меню лабіринт
def game_five():
    global score, current_lab_map, coins, last_coin_type, current_level

    current_level = 5
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

    start_time = pygame.time.get_ticks()
    current_lab_map = lab_map
    coins = generate_random_coins(lab_map, 10)
    last_coin_type = None
    while True:
        back.blit(game5_bg, (0, 0))
        draw_lab(back, lab_map)
        draw_timer(back)

        draw_score(back, last_coin_type)

        def draw_score(surface, coin_type=None):
            color = (255, 255, 255)
            if coin_type == 'gold':
                color = (255, 215, 0)
            elif coin_type == 'silver':
                color = (192, 192, 192)
            elif coin_type == 'diamond':
                color = (0, 255, 255)

            score_text = font10.render(f"Score: {score}", True, color)
            surface.blit(score_text, (20, 20))
        for coin in coins:
            coin.draw(back)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                with open('res/txt/scores.txt', 'a') as f:
                    f.write(f"Score: {score}\n")
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    for coin in coins[:]:
                        if player5.rect.colliderect(coin.rect):
                            score += coin.value
                            last_coin_type = coin.type
                            coins.remove(coin)
                            break

            if not coins:
                exit_row, exit_col = 13, 15
                player_row = (player5.rect.centery - OFFSET_Y) // CELL_SIZE
                player_col = (player5.rect.centerx - OFFSET_X) // CELL_SIZE
                if (player_row, player_col) == (exit_row, exit_col):
                    show_level_complete_window(5)
                    return

        enemies.update()
        enemies.draw(back)

        player5.update(current_lab_map)
        player5.draw(back)

        draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49,
                    (88, 130, 71), (106, 141, 94), open_menu, 255, 30)
        draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18,
                           (255, 255, 255), open_que, 0, 30)
        draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49,
                    (88, 130, 71), (106, 141, 94), toggle_music, 255, 30)

        pygame.display.update()

def game_one(): global score, current_lab_map, coins, last_coin_type, current_level

current_level = 1
enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

current_lab_map = lab_map
coins = generate_random_coins(lab_map, 15)
last_coin_type = None

clouds = [Cloud('img/game1/cloud.png') for _ in range(25)]
while True:
    back.blit(game1_bg, (0, 0))
    draw_lab(back, lab_map)
    draw_timer(back)
    draw_score(back, last_coin_type)

    enemies.update()
    enemies.draw(back)

    for cloud in clouds:
        cloud.move()
        cloud.draw(back)

    for coin in coins:
        coin.draw(back)

    player1.update(current_lab_map)
    player1.draw(back)

    draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49, (88, 130, 71), (106, 141, 94), open_menu, 255, 30)
    draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18, (255, 255, 255), open_que, 0)
    draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49, (88, 130, 71), (106, 141, 94), toggle_music, 255, 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:


                for coin in coins[:]:
                    if player1.rect.colliderect(coin.rect):
                        score += coin.value
                        last_coin_type = coin.type
                        coins.remove(coin)
                        break

                        if not coins:
                            exit_row, exit_col = 13, 15
                            player_row = (player1.rect.centery - OFFSET_Y) // CELL_SIZE
                            player_col = (player1.rect.centerx - OFFSET_X) // CELL_SIZE
                            if (player_row, player_col) == (exit_row, exit_col):
                                show_level_complete_window(1)


    pygame.display.update()


    def game_two():
        global score, current_lab_map, coins, last_coin_type, current_level, draw_score
        current_level = 2
        enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

        current_lab_map = lab_map_2
        coins = generate_random_coins(lab_map_2, 12)
        last_coin_type = None

        rain = [Rain() for _ in range(100)]

        while True:
            back.blit(game2_bg, (0, 0))
            draw_lab(back, lab_map_2)
            draw_timer(back)
            draw_score(back)

            enemies.update()
            enemies.draw(back)

            for coin in coins:
                coin.draw(back)

                if player2.rect.colliderect(coin.rect):
                    score += coin.value
                    coins.remove(coin)

            for drop in rain:
                drop.fall()
                drop.draw(back)

            player2.update(current_lab_map)
            player2.draw(back)

            text = font9.render('', True, (50, 50, 50))
            text_rect = text.get_rect(center=(width // 2, height // 2))
            back.blit(text, text_rect)

            draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49, (88, 130, 71), (106, 141, 94), open_menu, 255,30)
            draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18, (255, 255, 255), open_que, 0)
            draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49, (88, 130, 71), (106, 141, 94), toggle_music, 255, 255)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        for coin in coins:
                            if player2.rect.colliderect(coin.rect):
                                score += coin.value
                                last_coin_type = coin.type
                                coins.remove(coin)
                                break

                    if not coins:
                        exit_row, exit_col = 13, 15
                        player_row = (player5.rect.centery - OFFSET_Y) // CELL_SIZE
                        player_col = (player5.rect.centerx - OFFSET_X) // CELL_SIZE
                        if (player_row, player_col) == (exit_row, exit_col):
                            show_level_complete_window(2)
                            return
pygame.display.update()


def game_two():
        global score, current_lab_map, coins, last_coin_type, current_level

        current_level = 2
        enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

        start_time = pygame.time.get_ticks()
        current_lab_map = lab_map
        coins = generate_random_coins(lab_map, 10)
        last_coin_type = None
        while True:
            back.blit(game5_bg, (0, 0))
            draw_lab(back, lab_map)
            draw_timer(back)

            draw_score(back, last_coin_type)

            def draw_score(surface, coin_type=None):
                color = (255, 255, 255)
                if coin_type == 'gold':
                    color = (255, 215, 0)
                elif coin_type == 'silver':
                    color = (192, 192, 192)
                elif coin_type == 'diamond':
                    color = (0, 255, 255)

                score_text = font10.render(f"Score: {score}", True, color)
                surface.blit(score_text, (20, 20))
            for coin in coins:
                coin.draw(back)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    with open('res/txt/scores.txt', 'a') as f:
                        f.write(f"Score: {score}\n")
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    if event.key == pygame.K_SPACE:
                        for coin in coins[:]:
                            if player5.rect.colliderect(coin.rect):
                                score += coin.value
                                last_coin_type = coin.type
                                coins.remove(coin)
                                break

                if not coins:
                    exit_row, exit_col = 13, 15
                    player_row = (player5.rect.centery - OFFSET_Y) // CELL_SIZE
                    player_col = (player5.rect.centerx - OFFSET_X) // CELL_SIZE
                    if (player_row, player_col) == (exit_row, exit_col):
                        show_level_complete_window(5)
                        return

            enemies.update()
            enemies.draw(back)

            player5.update(current_lab_map)
            player5.draw(back)

            draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49,
                        (88, 130, 71), (106, 141, 94), open_menu, 255, 30)
            draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18,
                               (255, 255, 255), open_que, 0, 30)
            draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49,
                        (88, 130, 71), (106, 141, 94), toggle_music, 255, 30)

            pygame.display.update()

def game_three():
    global score, current_lab_map, coins, last_coin_type, current_level, draw_score
    current_level = 3
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())
    current_lab_map = lab_map_3
    coins = generate_random_coins(lab_map_3, 13)
    last_coin_type = None

    flowers = [Flower('img/game3/floww.png') for _ in range(20)]

    while True:
        back.blit(game3_bg, (0, 0))
        draw_lab(back, lab_map_3)
        draw_timer(back)
        draw_score(back)

        enemies.update()
        enemies.draw(back)

        for coin in coins:
            coin.draw(back)

            if player3.rect.colliderect(coin.rect):
                score += coin.value
                coins.remove(coin)

        for flower in flowers:
            flower.fall()
            flower.draw(back)

        player3.update(current_lab_map)
        player3.draw(back)

        text = font9.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)

        draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49, (88, 130, 71), (106, 141, 94), open_menu, 255,30)
        draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18, (255, 255, 255), open_que, 0)
        draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49, (88, 130, 71), (106, 141, 94), toggle_music,255, 255)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    for coin in coins:
                        if player3.rect.colliderect(coin.rect):
                            score += coin.value
                            last_coin_type = coin.type
                            coins.remove(coin)
                            break

                if not coins:
                    exit_row, exit_col = 13, 15
                    player_row = (player5.rect.centery - OFFSET_Y) // CELL_SIZE
                    player_col = (player5.rect.centerx - OFFSET_X) // CELL_SIZE
                    if (player_row, player_col) == (exit_row, exit_col):
                        show_level_complete_window(3)
                        return

        pygame.display.update()

def game_four():
    global score, current_lab_map, coins, last_coin_type, current_level, draw_score

    current_level = 4
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

    start_time = pygame.time.get_ticks()
    current_lab_map = lab_map_4
    coins = generate_random_coins(lab_map_4, 1)
    last_coin_type = None

    while True:
        back.blit(game4_bg, (0, 0))
        draw_lab(back, lab_map_4)
        draw_timer(back)
        draw_score(back)

        enemies.update()
        enemies.draw(back)

        for coin in coins:
            coin.draw(back)

            if player4.rect.colliderect(coin.rect):
                score += coin.value
                coins.remove(coin)

        player4.update(current_lab_map)
        player4.draw(back)

        text = font9.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)

        draw_button('menu', width // 2 - 373, height // 2 + 59, 115, 49, (88, 130, 71), (106, 141, 94), open_menu, 255,30)
        draw_circle_button('what', width // 2 - 315, height // 2 + 200, 18, (255, 255, 255), open_que, 0)
        draw_button('music', width // 2 - 373, height // 2 + 118, 115, 49, (88, 130, 71), (106, 141, 94), toggle_music, 255, 255)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_SPACE:
                    for coin in coins:
                        if player4.rect.colliderect(coin.rect):
                            score += coin.value
                            last_coin_type = coin.type
                            coins.remove(coin)
                            break

                if not coins:
                    exit_row, exit_col = 13, 15
                    player_row = (player5.rect.centery - OFFSET_Y) // CELL_SIZE
                    player_col = (player5.rect.centerx - OFFSET_X) // CELL_SIZE
                    if (player_row, player_col) == (exit_row, exit_col):
                        show_level_complete_window(4)
                        return
        pygame.display.update()


#переклад
current_language = 'ua'

def load_text_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            text = file.read()
        return text
    except FileNotFoundError:
        return None

def display_text_from_file(file_path, start_y=320, text_size=40):
    try:
        with open(file_path, 'r', encoding= 'utf-8') as file:
            lines = file.readlines()
            font = pygame.font.SysFont(None, text_size)
            x = 10
            y = start_y
            for line in lines:
                text_surface =font.render(line.strip(), True, (255, 255, 255))
                text_rect = text_surface.get_rect(topleft=(x,y))
                back.blit(text_surface, text_rect)
                y += text_size + 10

    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено.")

def toggle_language():
    global current_language
    current_language = 'en' if current_language == 'ua' else 'ua'


#правила
def info_back():
    inf_image = pygame.image.load('img/inf.jpg')
    inf_image = pygame.transform.scale(inf_image, (800, 800))

    inc_image = pygame.image.load('img/cat_inf.png')
    inc_image = pygame.transform.scale(inc_image, (500, 500))

    while True:
        back.fill((240, 240, 240))
        back.blit(inf_image, (0, 0))
        back.blit(inc_image, (480, 80))

        draw_button("Language", width // 2 - 90, height - 100 - 400, 180, 50, (63, 91, 120), (137, 167, 200), toggle_language)
        draw_circle_button("Okay", width // 2, height - 100 - 320, 40, (63, 91, 120), return_to_main_menu, alpha=0)

        if current_language == 'en':
            display_text_from_file('res/txt/informationEng.txt', text_size=24)
        else:

            display_text_from_file('res/txt/information.txt', text_size=24)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if width // 2 - 90 <= mouse_pos[0] <= width // 2 - 90 + 180 and height - 100 <= mouse_pos[1] <= height - 100 + 50: toggle_language()
        pygame.display.update()

def settings_back():
    global total_score
    global music_on
    set_back = pygame.image.load('img/inf.jpg')
    set_back = pygame.transform.scale(set_back, (width, height))




    score_text = font8.render(f'score {score}', True, (55, 82, 109))
    score_rect = score_text.get_rect(center=(width // 2, height //2 + 150))

    while True:
        back.blit(set_back, (0, 0))


        back.blit(score_text, score_rect)

        music_text = "Music: ON" if music_on else "Music: OFF"
        draw_button(music_text, width //2 - 150, height // 4, 300, 60,(63, 91, 120), (137, 167, 200),toggle_music)
        draw_button('Menu', width // 2 - 150, height // 2, 300, 60, (63, 91, 120), (137, 167, 200),return_to_main_menu)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        pygame.display.update()

if __name__ == "__main__":

    load_music()
    main_menu()