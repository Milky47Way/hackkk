from PIL import Image
import pygame
import sys
import os

from lab import  lab_map, lab_map_2, lab_map_3, lab_map_4, lab_map_5, draw_lab, Cloud, Rain, Flower, Snowflake, find_spawn_point
from coin import Coin, generate_random_coins
from hero import Player
from enemies import Enemy, img_enemy1, img_enemy2, img_enemy3, img_enemy4, img_enemy5, img_enemy6, img_enemy7

pygame.mixer.init()
pygame.init()

CELL_SIZE = 37
OFFSET_X, OFFSET_Y = 220, 23

#таймер
start_ticks = pygame.time.get_ticks()
time_limit = 25 * 60

#музика та ефекти
music_on = True
music_path = os.path.join(os.path.dirname(__file__), "res/sounds/The Cascades - Rhythm of the Rain.mp3")

def toggle_music():
    global music_on
    if pygame.mixer.music.get_busy():
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
    show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
    show_lab_info = not show_lab_info
    pygame.time.wait(100)

def open_menu():
    global show_menu_info
    show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
    show_menu_info = not show_menu_info
    pygame.time.wait(200)

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
    surface.blit(timer_surface, (width - 740, 100))

    if remaining == 0:
        end_game()

#монетки
score = 0
last_coin_type = None

def add_score(points):
    global score
    score += points

def draw_score(surface, score, last_coin_type):
    if last_coin_type == 'gold':
        color = (255, 244, 255)
    elif last_coin_type == 'silver':
        color = (224, 155, 255)
    elif last_coin_type == 'diamond':
        color = (131, 127, 189)
    else:
        color = (255, 255, 255)

    score_text = font10.render(f"Score: {score}", True, color)
    surface.blit(score_text, (50, 60))

def draw_exit(surface, row, col, color=(255, 0, 0)):
    pygame.draw.rect(
        surface,
        color,
        pygame.Rect(
            OFFSET_X + col * CELL_SIZE,
            OFFSET_Y + row * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
    )

#Зображення
def load_tif_image(path, size):
    img = Image.open(path)
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    data = img.tobytes()
    surface = pygame.image.fromstring(data, img.size, img.mode)
    return pygame.transform.smoothscale(surface, size)

def load_images():
    backgrounds = {
        "main_menu": load_tif_image('img/menu.tif', (800, 600)),
        "menu_game":  load_tif_image('img/menu_game.tif', (800, 600)),
        "set": load_tif_image('img/set.tif', (800, 600)),

        "game1": load_tif_image('img/game1/game1.tif', (800, 600)),
        "game11": load_tif_image('img/game1/game11.tif', (800, 600)),

        "game2": load_tif_image('img/game2/game2.tif', (800, 600)),
        "game22": load_tif_image('img/game2/game22.tif', (800, 600)),

        "game3": load_tif_image('img/game3/game3.tif', (800, 600)),
        "game33": load_tif_image('img/game3/game33.tif', (800, 600)),

        "game4": load_tif_image('img/game4/game4.tif', (800, 600)),
        "game44": load_tif_image('img/game4/game44.tif', (800, 600)),

        "game5": load_tif_image('img/game5/game5.tif', (800, 600)),
        "game55": load_tif_image('img/game5/game55.tif', (800, 600)),

        "game_final": load_tif_image('img/game5/game.final.tif', (800, 600)),
    }
    return backgrounds

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

def pause_game():
    global paused
    paused = True
    font_pause = pygame.font.SysFont('Verdana', 48)
    while paused:
        draw_button("Continue", width // 2 - 15, height // 2 - 50, 200, 60,
                    (63, 91, 120), (137, 167, 200), unpause_game, 255, 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                unpause_game()

        pygame.display.update()
        pygame.time.Clock().tick(10)

def unpause_game():
    global paused
    paused = False

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
paused = False

#вороги
enemy1 = Enemy(0, 512, (200, 250), img_enemy1, (40,40), (1))
enemy2 = Enemy(102, 400, (520, 570), img_enemy2, (50,40), (1))
enemy3 = Enemy(92, 320, (320, 370), img_enemy3, (40,40), (1))
enemy4 = Enemy(92, 320, (320, 370), img_enemy4, (40,40), (1))
enemy5 = Enemy(92, 320, (320, 370), img_enemy5, (40,40), (1))
enemy6 = Enemy(110, 520, (320, 370), img_enemy6, (30,40), (1))
enemy7 = Enemy(333, 120, (320, 370), img_enemy7, (40,40), (1))

enemies_by_level = {
    1: pygame.sprite.Group(enemy1, enemy2, enemy3),
    2: pygame.sprite.Group(enemy1, enemy4),
    3: pygame.sprite.Group(enemy4, enemy6, enemy7),
    4: pygame.sprite.Group(enemy4, enemy5),
    5: pygame.sprite.Group(enemy4, enemy5)
}

#герой
player = {
    1: (lab_map, "img/hero.png", (25, 33), 5),
    2: (lab_map_2, "img/hero.png", (25, 33), 4),
    3: (lab_map_3, "img/hero.png", (25, 33), 3),
    4: (lab_map_4, "img/hero.png", (25, 33), 2),
    5: (lab_map_5, "img/hero.png", (25, 33), 1),
}

players= {}
for i in range(1, 6):
    spawn_x, spawn_y = find_spawn_point(player[i][0])

    players[i] = Player(spawn_x, spawn_y,player[i][1],player[i][2],width, height,player[i][3])

#кнопки
def draw_button(text, x, y, w, h, base_color, hover_color, action=None, alpha=255, border_radius=0):
    global mouse_was_pressed
    mouse_pos = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    current_color = hover_color if rect.collidepoint(mouse_pos) else base_color

    button_surface = pygame.Surface((w, h), pygame.SRCALPHA)
    pygame.draw.rect(button_surface, (*current_color, alpha), button_surface.get_rect(), border_radius=border_radius)
    back.blit(button_surface, (x, y))

    text_surface = font9.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=rect.center)
    back.blit(text_surface, text_rect)

    mouse_pressed = pygame.mouse.get_pressed()[0]

    if not mouse_pressed:
        mouse_was_pressed = False

    if mouse_pressed and rect.collidepoint(mouse_pos) and not mouse_was_pressed:
        mouse_was_pressed = True
        if action:
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
        back.blit(backgrounds["main_menu"], (0, 0))
        button_x = width - 251
        button_xs = width - 725

        buttonSet_y = 520

        buttonI_y = 373
        buttonS_y = 438

        button_w = 180
        button_h = 56

        draw_button("Start", button_x, buttonS_y, button_w, button_h, (124, 128, 81), (156, 162, 118), start_backk, 255, 50)
        draw_button("Info", button_x, buttonI_y, button_w, button_h, (197, 143, 99), (213, 171, 129), info_back, 255, 50)
        draw_button("Settings", button_xs, buttonSet_y, button_w, button_h, (58, 57, 70), (89, 85, 104), settings_back, 255, 50)

        for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            print("Info")
                            sys.exit()

        pygame.time.wait(10)
        pygame.display.update()


#меню ігр
def start_backk():
    while True:

        back.blit(backgrounds["menu_game"],(0,0))
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

        pygame.time.wait(10)
        pygame.display.update()

def game_four():
    global score, current_lab_map, coins, last_coin_type, current_level
    current_level = 4
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())
    current_lab_map = lab_map_4
    coins = generate_random_coins(current_lab_map, 20)  # Наприклад, 5 монет
    total_coins = len(coins)
    last_coin_type = None

    clock = pygame.time.Clock()

    while True:
        back.blit(backgrounds["game4"], (0, 0))
        draw_lab(back, current_lab_map)
        draw_timer(back)
        draw_score(back, score, last_coin_type)
        collected_coins = total_coins - len(coins)
        enemies.update()
        enemies.draw(back)

        for coin in coins:
            coin.draw(back)

        players[4].update(current_lab_map)
        players[4].draw(back)

        if pygame.sprite.spritecollideany(players[4], enemies):
            score = max(0, score - 4)

        # Кнопки
        draw_button('music', width // 2 - 365, height // 2 + 78, 116, 38,
                    (58, 69, 144), (67, 71, 173), toggle_music, 255, 50)
        draw_button('menu', width // 2 - 366, height // 2 + 20, 116, 38,
                    (58, 69, 144), (67, 71, 173), open_menu, 255, 50)
        draw_circle_button('', width // 2 - 290, height // 2 + 157, 30,
                           (131, 127, 189), open_que, 0)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_SPACE:
                    coins, score, last_coin_type = collect_coin(coins, players[4], score, last_coin_type)

        if not coins:
            exit_row, exit_col = 14, 11
            #draw_exit(back, exit_row, exit_col)
            player_row = (players[4].rect.centery - OFFSET_Y) // CELL_SIZE
            player_col = (players[4].rect.centerx - OFFSET_X) // CELL_SIZE
            if (player_row, player_col) == (exit_row, exit_col):
                show_level_complete_window(4, backgrounds)
                return
        if show_menu_info:
            show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
        if show_lab_info:
            show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
        clock.tick(60)
        pygame.display.update()

def game_one():
    global score, current_lab_map, coins, last_coin_type, current_level

    current_level = 1
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

    current_lab_map = lab_map
    coins = generate_random_coins(lab_map, 10)
    last_coin_type = None

    clouds = [Cloud('img/game1/cloud.png') for _ in range(25)]

    while True:
        back.blit(backgrounds["game1"], (0, 0))
        draw_lab(back, lab_map)
        draw_timer(back)
        draw_score(back, score, last_coin_type)

        enemies.update()
        enemies.draw(back)


        for coin in coins:
            coin.draw(back)

        players[1].update(current_lab_map)
        players[1].draw(back)

        if pygame.sprite.spritecollideany(players[1], enemies):
            score = max(0, score - 1)

        draw_button('menu', width // 2 - 366, height // 2 + 20, 116, 38, (58, 69, 144), (67, 71, 173), open_menu, 255,50)
        draw_circle_button('', width // 2 - 290, height // 2 + 157, 30, (131, 127, 189), open_que,  0)
        draw_button('music', width // 2 - 365, height // 2 + 78, 116, 38, (58, 69, 144), (67, 71, 173), toggle_music,255, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_SPACE:
                    coins, score, last_coin_type = collect_coin(coins, players[1], score, last_coin_type)

        for cloud in clouds:
            cloud.move()
            cloud.draw(back)


        if not coins:
            exit_row, exit_col = 14,11
            player_row = (players[1].rect.centery - OFFSET_Y) // CELL_SIZE
            player_col = (players[1].rect.centerx - OFFSET_X) // CELL_SIZE
            if (player_row, player_col) == (exit_row, exit_col):
                show_level_complete_window(1, backgrounds)
                return
        if show_menu_info:
            show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
        if show_lab_info:
            show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
        pygame.time.wait(10)
        pygame.display.update()

def collect_coin(coins, player, score, last_coin_type):
    for coin in coins:
        if player.rect.colliderect(coin.rect):
            score += coin.value
            last_coin_type = coin.type
            coins.remove(coin)
            break
    return coins, score, last_coin_type

def game_two():
        global score, current_lab_map, coins, last_coin_type, current_level

        current_level = 2
        enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

        current_lab_map = lab_map_2
        coins = generate_random_coins(lab_map_2, 1)
        last_coin_type = None

        rain = [Rain() for _ in range(100)]

        clock = pygame.time.Clock()

        while True:
            back.blit(backgrounds["game2"], (0, 0))
            draw_lab(back, lab_map_2)
            draw_timer(back)
            draw_score(back, score, last_coin_type)

            enemies.update()
            enemies.draw(back)

            for coin in coins:
                coin.draw(back)



            players[2].update(current_lab_map)
            players[2].draw(back)

            if pygame.sprite.spritecollideany(players[2], enemies):
                score = max(0, score - 2)
            draw_button('menu', width // 2 - 366, height // 2 + 20, 116, 38, (58, 69, 144), (67, 71, 173), open_menu, 255, 50)
            draw_circle_button('', width // 2 - 290, height // 2 + 157, 30, (58, 69, 144), open_que, 0)
            draw_button('music', width // 2 - 365, height // 2 + 78, 116, 38, (58, 69, 144), (67, 71, 173), toggle_music, 255, 50)
            for drop in rain:
                drop.fall()
                drop.draw(back)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_p:
                        pause_game()
                    elif event.key == pygame.K_SPACE:
                        coins, score, last_coin_type = collect_coin(coins, players[2], score, last_coin_type)
            if not coins:
                exit_row, exit_col = 14,11
                player_row = (players[2].rect.centery - OFFSET_Y) // CELL_SIZE
                player_col = (players[2].rect.centerx - OFFSET_X) // CELL_SIZE
                if (player_row, player_col) == (exit_row, exit_col):
                    show_level_complete_window(2, backgrounds)
                    return
            if show_menu_info:
                show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
            if show_lab_info:
                show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
            clock.tick(60)
            pygame.display.update()

def game_three():
    global score, current_lab_map, coins, last_coin_type, current_level

    current_level = 3
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())
    current_lab_map = lab_map_3
    coins = generate_random_coins(lab_map_3, 13)
    last_coin_type = None

    flowers = [Flower('img/game3/Flower.png') for _ in range(20)]

    clock = pygame.time.Clock()

    while True:
        back.blit(backgrounds["game3"], (0, 0))
        draw_lab(back, lab_map_3)
        draw_timer(back)
        draw_score(back, score, last_coin_type)

        enemies.update()
        enemies.draw(back)

        for coin in coins:
            coin.draw(back)


        players[3].update(current_lab_map)
        players[3].draw(back)
        if pygame.sprite.spritecollideany(players[3], enemies):
            score = max(0, score - 3)
        draw_button('menu', width // 2 - 366, height // 2 + 20, 116, 38, (102, 95, 172), (131, 127, 189), open_menu,255, 50)
        draw_circle_button('', width // 2 - 290, height // 2 + 157, 30, (131, 127, 189), open_que, 0)
        draw_button('music', width // 2 - 365, height // 2 + 78, 116, 38, (102, 95, 172), (131, 127, 189), toggle_music,255, 50)
        for flower in flowers:
            flower.fall()
            flower.draw(back)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_SPACE:

                    coins, score, last_coin_type = collect_coin(coins, players[3], score, last_coin_type)


        if not coins:
            exit_row, exit_col = 14,11
            player_row = (players[3].rect.centery - OFFSET_Y) // CELL_SIZE
            player_col = (players[3].rect.centerx - OFFSET_X) // CELL_SIZE
            if (player_row, player_col) == (exit_row, exit_col):
                show_level_complete_window(3, backgrounds)
                return
        if show_menu_info:
            show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
        if show_lab_info:
            show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
        clock.tick(60)
        pygame.display.update()

def game_five():
    global score, current_lab_map, coins, last_coin_type, current_level

    current_level = 5
    enemies = enemies_by_level.get(current_level, pygame.sprite.Group())

    start_time = pygame.time.get_ticks()
    current_lab_map = lab_map_5
    coins = generate_random_coins(lab_map_5, 15)
    last_coin_type = None

    clock = pygame.time.Clock()
    snowflakes = [Snowflake() for _ in range(200)]
    while True:
        back.blit(backgrounds["game5"], (0, 0))
        draw_lab(back, lab_map_5)
        draw_timer(back)
        draw_score(back, score, last_coin_type)

        enemies.update()
        enemies.draw(back)

        for coin in coins:
            coin.draw(back)

        coins, score, last_coin_type = collect_coin(coins, players[5], score, last_coin_type)

        players[5].update(current_lab_map)
        players[5].draw(back)
        if pygame.sprite.spritecollideany(players[5], enemies):
            score = max(0, score - 5)
        text = font9.render('', True, (50, 50, 50))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        back.blit(text, text_rect)

        draw_button('menu', width // 2 - 366, height // 2 + 20, 116, 38, (58, 69, 144), (67, 71, 173), open_menu,255, 50)
        draw_circle_button('', width // 2 - 290, height // 2 + 157, 30, (131, 127, 189), open_que, 0)
        draw_button('music', width // 2 - 365, height // 2 + 78, 116, 38, (58, 69, 144), (67, 71, 173), toggle_music,255, 50)
        for snowflake in snowflakes:
            snowflake.update()
            snowflake.draw(back)
        if not coins:
            exit_row, exit_col = 14,11
            player_row = (players[5].rect.centery - OFFSET_Y) // CELL_SIZE
            player_col = (players[5].rect.centerx - OFFSET_X) // CELL_SIZE
            if (player_row, player_col) == (exit_row, exit_col):
                show_level_complete_window(5, backgrounds)
                return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_SPACE:
                    coins, score, last_coin_type = collect_coin(coins, players[5], score, last_coin_type)
        if show_menu_info:
            show_queue_window('res/txt/menu.txt', width=180, height=40, x=0, y=300, bg_color=(131, 127, 189))
        if show_lab_info:
            show_queue_window('res/txt/lab.txt', width=300, height=300, x=0, y=150, bg_color=(131, 127, 189))
        clock.tick(60)
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


def info_back():
    inf_image = pygame.image.load('img/inf.jpg')
    inf_image = pygame.transform.scale(inf_image, (800, 800))

    inc_image = pygame.image.load('img/cat_inf.png')
    inc_image = pygame.transform.scale(inc_image, (500, 500))

    while True:
        back.fill((240, 240, 240))
        back.blit(inf_image, (0, 0))
        back.blit(inc_image, (480, 80))

        draw_button("Language", width // 2 - 90, height - 100 - 400, 180, 50, (63, 91, 120), (137, 167, 200),
                    toggle_language)

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
                    if width // 2 - 90 <= mouse_pos[0] <= width // 2 + 90 and height - 100 - 400 <= mouse_pos[
                        1] <= height - 100 - 350:
                        toggle_language()
                    elif width // 2 - 40 <= mouse_pos[0] <= width // 2 + 40 and height - 100 - 360 <= mouse_pos[
                        1] <= height - 100 - 280:
                        return_to_main_menu()

        pygame.display.update()

def settings_back():
    global total_score, music_on
    back.blit(backgrounds["set"],(0,0))

    score_text = font8.render(f'Score: {score}', True, (55, 82, 109))
    score_rect = score_text.get_rect(center=(width // 2, height // 2 + 150))

    while True:
        back.blit(backgrounds["set"], (0, 0))
        back.blit(score_text, score_rect)


        music_text = "Music: ON" if music_on else "Music: OFF"
        draw_button(music_text, width // 2 - 150, height // 4, 300, 60, (63, 91, 120), (137, 167, 200), toggle_music)
        draw_button('Menu', width // 2 - 150, height // 2, 300, 60, (63, 91, 120), (137, 167, 200), return_to_main_menu)


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

                    if width // 2 - 150 <= mouse_pos[0] <= width // 2 + 150 and height // 4 <= mouse_pos[1] <= height // 4 + 60:
                        toggle_music()

                    elif width // 2 - 150 <= mouse_pos[0] <= width // 2 + 150 and height // 2 <= mouse_pos[1] <= height // 2 + 60:
                        return_to_main_menu()

        pygame.display.update()

def toggle_music():
    global music_on
    music_on = not music_on
    if music_on:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()


def show_level_complete_window(level, backgrounds):
    screen = pygame.display.set_mode((800, 600))
    screen.fill((63, 91, 120))

    if level == 1:
        image_surface = backgrounds["game11"]
    elif level == 2:
        image_surface = backgrounds["game_final"]
    elif level == 3:
        image_surface = backgrounds["game33"]
    elif level == 4:
        image_surface = backgrounds["game22"]
    elif level == 5:
        image_surface = backgrounds["game55"]
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


backgrounds = load_images()

if __name__ == "__main__":
    load_music()
    main_menu()
