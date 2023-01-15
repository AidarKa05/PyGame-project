import pygame
import pygame_gui
import sys
import os


FPS = 60
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1200, 800
levels = -1
score = 0
level_up = True
clear_sprites = False
skin = ''

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Labyrinth of freedom')
pygame.display.set_icon(pygame.image.load('data/ico.jpg'))


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    intro_text = "Чтобы продолжить нажмите на любую кнопку"
    fon = pygame.transform.scale(load_image('fon.jpg'), (1200, 800))
    screen.blit(fon, (0, 0))
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, 40)
    text_surface = font.render(intro_text, True, pygame.Color('yellow'))
    intro_rect = text_surface.get_rect()
    intro_rect.midtop = (600, 726)
    screen.blit(text_surface, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def choose_pers():
    fon = pygame.transform.scale(load_image('lose_fon.jpg'), (1200, 800))
    screen.blit(fon, (0, 0))
    screen.blit(plimst[0], (380, 400))
    screen.blit(plimst[1], (780, 400))
    intro_text = "Чтобы продолжить нажмите на любую кнопку"
    font = pygame.font.Font(None, 40)
    text_surface = font.render(intro_text, True, pygame.Color('yellow'))
    intro_rect = text_surface.get_rect()
    intro_rect.midtop = (600, 720)
    screen.blit(text_surface, intro_rect)

    lose = 'Выберите персонажа'
    font_l = pygame.font.Font(None, 70)
    l_text = font_l.render(lose, True, pygame.Color('yellow'))
    l_rect = l_text.get_rect()
    l_rect.midtop = (600, 150)
    screen.blit(l_text, l_rect)

    manager = pygame_gui.UIManager((1200, 800))

    pers1 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((350, 500), (100, 50)),
        text='PAC-MAN',
        manager=manager
    )
    pers2 = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((750, 500), (100, 50)),
        text='TOTEM',
        manager=manager
    )
    global skin
    while True:
        time_d = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == pers1:
                        skin = 'Pacman'
                        print(skin)
                    if event.ui_element == pers2:
                        skin = 'TOTM'
                        print(skin)
            elif event.type == pygame.KEYDOWN:
                return
            manager.process_events(event)
        manager.update(time_d)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(FPS)


tile_width = tile_height = 40

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
checkpoint_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
traps_group = pygame.sprite.Group()

tile_images = {
    'gr': load_image('gr.jpg'),
    'wwr': load_image('wwr.jpg'),
    'up_l': load_image('wl.jpg'),
    'up_r': load_image('wr.jpg'),
    'dw_l': load_image('nl.jpg'),
    'dw_r': load_image('nr.jpg'),
    'trap_up': load_image('trapu.jpg', -1),
    'trap_dw': load_image('trapd.jpg', -1),
    'trap_l': load_image('trapl.jpg', -1),
    'trap_r': load_image('trapr.jpg', -1),
    'finish': load_image('fin1.png'),
    'trap1': load_image('trap1.jpg', -1),
    'trap2': load_image('trap2.jpg', -1),
    'trap3': load_image('trap3.jpg', -1),
    'trap4': load_image('trap4.jpg', -1),
    'fon': load_image('fon_map.jpg'),
    'empty': load_image('check1.png'),
    'coin': load_image('coin1.png', -1)
}
maps = ['lv1.txt', 'lv2.txt']
fin_im = [load_image('fin1.png'), load_image('fin2.png')]
anim = [load_image('anim1.png', -1), load_image('anim2.png', -1), load_image('anim3.png', -1)]
coin_im = [load_image('coin1.png'), load_image('coin2.jpg')]
check_im = [load_image('check1.png'), load_image('check2.png')]

plimst = [load_image('plst.png'), load_image('totmdw1.jpg')]
plim_rt = [load_image('rt1.png', -1), load_image('rt2.png', -1), load_image('totmrt1.jpg', -1), load_image('totmrt2.jpg', -1)]
plim_lf = [load_image('lf1.png', -1), load_image('lf2.png', -1), load_image('totmlf1.jpg', -1), load_image('totmlf2.jpg', -1)]
plim_dw = [load_image('dw1.png', -1), load_image('dw2.png', -1), load_image('totmdw1.jpg', -1), load_image('totmdw2.jpg', -1)]
plim_up = [load_image('up1.png', -1), load_image('up2.png', -1), load_image('totmup1.jpg', -1), load_image('totmup2.jpg', -1)]


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '0'), level_map))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Coins(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(coins_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.skintm = 0

    def update(self):
        if self.skintm + 1 >= 60:
            self.skintm = 0
        self.image = coin_im[self.skintm // 30]
        self.skintm += 1


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(checkpoint_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.skintm = 0

    def update(self):
        if self.skintm + 1 >= 60:
            self.skintm = 0
        self.image = check_im[self.skintm // 30]
        self.skintm += 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y


class Trap(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(traps_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = pos_x
        self.y = pos_y


class Finish(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(finish_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.skintm = 0

    def update(self):
        if self.skintm + 1 >= 60:
            self.skintm = 0
        self.image = fin_im[self.skintm // 30]
        self.skintm += 1


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        if skin == 'Pacman':
            self.image = plimst[0]
        if skin == 'TOTM':
            self.image = plimst[1]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y
        self.count_coins = 0
        self.f = False
        self.move = True
        self.animtm = 0
        self.skintm = 0
        self.rt = False
        self.lf = False
        self.dw = False
        self.up = False
        self.up_lv = False
        self.on_trap = False
        self.level = levels + 2

    def update(self):

        if self.skintm + 1 >= 60:
            self.skintm = 0
        if skin == 'Pacman':
            if self.rt:
                self.image = plim_rt[self.skintm // 30]
            if self.lf:
                self.image = plim_lf[self.skintm // 30]
            if self.up:
                self.image = plim_up[self.skintm // 30]
            if self.dw:
                self.image = plim_dw[self.skintm // 30]
        if skin == 'TOTM':
            if self.rt:
                self.image = plim_rt[self.skintm // 30 + 2]
            if self.lf:
                self.image = plim_lf[self.skintm // 30 + 2]
            if self.up:
                self.image = plim_up[self.skintm // 30 + 2]
            if self.dw:
                self.image = plim_dw[self.skintm // 30 + 2]
        self.skintm += 1

        score = str(self.count_coins)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(score, True, pygame.Color('yellow'))
        intro_rect = text_surface.get_rect()
        intro_rect.midtop = (100, 40)
        screen.blit(text_surface, intro_rect)

        lvl = 'Уровень ' + str(self.level)
        font = pygame.font.Font(None, 30)
        lvl_surface = font.render(lvl, True, pygame.Color('yellow'))
        lvl_rect = lvl_surface.get_rect()
        lvl_rect.midtop = (600, 40)
        screen.blit(lvl_surface, lvl_rect)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, walls_group):
            self.move = True
            if self.speedx > 0:
                self.speedx = 0
                self.rect.x = self.rect.x - 40
            if self.speedx < 0:
                self.speedx = 0
                self.rect.x = self.rect.x + 40
            if self.speedy > 0:
                self.speedy = 0
                self.rect.y = self.rect.y - 40
            if self.speedy < 0:
                self.speedy = 0
                self.rect.y = self.rect.y + 40
        if pygame.sprite.spritecollideany(self, traps_group):
            self.on_trap = True
        collis_coin = pygame.sprite.groupcollide(player_group, coins_group, False, True)
        if collis_coin:
            for coin in collis_coin.values():
                self.count_coins += 100 * len(coin)
        collis_check = pygame.sprite.groupcollide(player_group, checkpoint_group, False, True)
        if collis_check:
            for check in collis_check.values():
                self.count_coins += 10 * len(check)
        if self.f:
            if self.animtm < 21:
                screen.blit(anim[self.animtm // 10], (self.rect.x - 20, self.rect.y - 20))
                self.animtm += 1
            else:
                global scores
                scores = self.count_coins
                self.up_lv = True
                self.kill()
                self.level += 1
                menu_screen()


def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('fon', x, y)
                new_player = Player(x, y)
            if level[y][x] == '.':
                Checkpoint('empty', x, y)
            elif level[y][x] == '0':
                Tile('fon', x, y)
            elif level[y][x] == 'f':
                fn = Finish('finish', x, y)
            elif level[y][x] == '2':
                Wall('up_l', x, y)
            elif level[y][x] == '1':
                Wall('dw_l', x, y)
            elif level[y][x] == '3':
                Wall('up_r', x, y)
            elif level[y][x] == '4':
                Wall('dw_r', x, y)
            elif level[y][x] == '-':
                Wall('gr', x, y)
            elif level[y][x] == '|':
                Wall('wwr', x, y)
            elif level[y][x] == '=':
                Trap('trap_up', x, y)
            elif level[y][x] == '+':
                Trap('trap_dw', x, y)
            elif level[y][x] == '!':
                Trap('trap_r', x, y)
            elif level[y][x] == '/':
                Trap('trap_l', x, y)
            elif level[y][x] == 'q':
                Trap('trap1', x, y)
            elif level[y][x] == 'w':
                Trap('trap2', x, y)
            elif level[y][x] == 'e':
                Trap('trap3', x, y)
            elif level[y][x] == 'r':
                Trap('trap4', x, y)
            elif level[y][x] == 'a':
                Coins('coin', x, y)
    return new_player, fn


def menu_screen():
    global scores
    fon = pygame.transform.scale(load_image('menu_fon.jpg'), (1200, 800))
    screen.blit(fon, (0, 0))
    intro_text = "Чтобы продолжить нажмите на любую кнопку"
    font = pygame.font.Font(None, 40)
    text_surface = font.render(intro_text, True, pygame.Color('yellow'))
    intro_rect = text_surface.get_rect()
    intro_rect.midtop = (600, 730)
    screen.blit(text_surface, intro_rect)

    sc = 'Счёт: ' + str(scores)
    sc_font = pygame.font.Font(None, 70)
    sc_text = sc_font.render(sc, True, pygame.Color('yellow'))
    sc_rect = sc_text.get_rect()
    sc_rect.midtop = (350, 300)
    screen.blit(sc_text, sc_rect)

    lv_up = 'Уровень пройден!'
    lv_up_text = sc_font.render(lv_up, True, pygame.Color('yellow'))
    lv_up_rect = lv_up_text.get_rect()
    lv_up_rect.midtop = (350, 200)
    screen.blit(lv_up_text, lv_up_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def clear():
    global all_sprites, tiles_group, coins_group, checkpoint_group, walls_group, player_group, finish_group
    for sprite in all_sprites:
        sprite.kill()
    for sprite in tiles_group:
        sprite.kill()
    for sprite in coins_group:
        sprite.kill()
    for sprite in checkpoint_group:
        sprite.kill()
    for sprite in walls_group:
        sprite.kill()
    for sprite in player_group:
        sprite.kill()
    for sprite in finish_group:
        sprite.kill()


def lose_screen():
    fon = pygame.transform.scale(load_image('lose_fon.jpg'), (1200, 800))
    screen.blit(fon, (0, 0))
    intro_text = "Чтобы начать заново нажмите на любую кнопку"
    font = pygame.font.Font(None, 40)
    text_surface = font.render(intro_text, True, pygame.Color('yellow'))
    intro_rect = text_surface.get_rect()
    intro_rect.midtop = (600, 720)
    screen.blit(text_surface, intro_rect)

    lose = 'Вы проиграли!'
    font_l = pygame.font.Font(None, 70)
    l_text = font_l.render(lose, True, pygame.Color('yellow'))
    l_rect = l_text.get_rect()
    l_rect.midtop = (600, 300)
    screen.blit(l_text, l_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)
