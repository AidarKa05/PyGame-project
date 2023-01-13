import time
import pygame
import sys
import os


FPS = 60
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1200, 800
levels = 0
score = 0
level_up = False

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


tile_width = tile_height = 40

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
coins_group = pygame.sprite.Group()
checkpoint_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()

tile_images = {
    'gr': load_image('gr.jpg'),
    'wwr': load_image('wwr.jpg'),
    'up_l': load_image('wl.jpg'),
    'up_r': load_image('wr.jpg'),
    'dw_l': load_image('nl.jpg'),
    'dw_r': load_image('nr.jpg'),
    'finish': load_image('finish.jpg'),
    'fon': load_image('fon_map.jpg'),
    'empty': load_image('block.jpg'),
    'coin': load_image('coin.png', -1)
}
maps = ['lv2.txt']
anim = [load_image('anim1.png', -1), load_image('anim2.png', -1), load_image('anim3.png', -1)]
plim_rt = [load_image('rt1.png', -1), load_image('rt2.png', -1)]
plim_lf = [load_image('lf1.png', -1), load_image('lf2.png', -1)]
plim_dw = [load_image('dw1.png', -1), load_image('dw2.png', -1)]
plim_up = [load_image('up1.png', -1), load_image('up2.png', -1)]


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


class Checkpoint(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(checkpoint_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = plim_up[0]
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

    def update(self):
        if self.skintm + 1 >= 60:
            self.skintm = 0
        if self.rt:
            self.image = plim_rt[self.skintm // 30]
        if self.lf:
            self.image = plim_lf[self.skintm // 30]
        if self.up:
            self.image = plim_up[self.skintm // 30]
        if self.dw:
            self.image = plim_dw[self.skintm // 30]
        self.skintm += 1

        score = str(self.count_coins)
        font = pygame.font.Font(None, 30)
        text_surface = font.render(score, True, pygame.Color('yellow'))
        intro_rect = text_surface.get_rect()
        intro_rect.midtop = (40, 40)
        screen.blit(text_surface, intro_rect)

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
        collis_coin = pygame.sprite.groupcollide(player_group, coins_group, False, True)
        if collis_coin:
            for coin in collis_coin.values():
                self.count_coins += 50 * len(coin)
        collis_check = pygame.sprite.groupcollide(player_group, checkpoint_group, False, True)
        if collis_check:
            for check in collis_check.values():
                self.count_coins += 10 * len(check)
        if self.f:
            if self.animtm < 21:
                screen.blit(anim[self.animtm // 10], (self.rect.x - 20, self.rect.y - 20))
                self.animtm += 1
            else:
                global levels, scores
                levels += 1
                scores = self.count_coins
                self.kill()
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
                fin = Finish('finish', x, y)
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
            elif level[y][x] == 'a':
                Coins('coin', x, y)
    return new_player, fin


def menu_screen():
    global scores, level_up
    fon = pygame.transform.scale(load_image('menu_fon.jpg'), (1200, 800))
    screen.blit(fon, (0, 0))
    intro_text = "Чтобы продолжить нажмите на любую кнопку"
    font = pygame.font.Font(None, 40)
    text_surface = font.render(intro_text, True, pygame.Color('yellow'))
    intro_rect = text_surface.get_rect()
    intro_rect.midtop = (600, 730)
    screen.blit(text_surface, intro_rect)

    sc = 'Счет:' + str(scores)
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
                level_up = True
                return
        pygame.display.flip()
        clock.tick(FPS)
