import pygame
import sys
import os

FPS = 50
clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 1400, 800

pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Labyrinth of freedom')

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
finish = pygame.sprite.Group()


def terminate():
    pygame.quit()
    sys.exit()


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
    intro_text = ["", "", "", "", "", "Чтобы продолжить нажмите на любую кнопку"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 40)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 100
        intro_rect.top = text_coord
        intro_rect.x = 350
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'gr': load_image('gr.jpg'),
    'wwr': load_image('wwr.jpg'),
    'up_l': load_image('wl.jpg'),
    'up_r': load_image('wr.jpg'),
    'dw_l': load_image('nl.jpg'),
    'dw_r': load_image('nr.jpg'),
    'finish': load_image('finish.jpg'),
    'wall': load_image('wall.jpg'),
    'fon': load_image('fon_map.jpg'),
    'empty': load_image('block.jpg')
}
player_image = load_image('nplayer.png', -1)

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Wall(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(walls_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Finish(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(finish, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.speedx = 0
        self.speedy = 0
        self.rect.x = tile_width * pos_x
        self.rect.y = tile_height * pos_y
        self.coins = None
        self.count_coins = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if pygame.sprite.spritecollideany(self, walls_group):
            self.speedx = 0
            self.speedy = 0


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                Tile('fon', x, y)
                new_player = Player(x, y)
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Wall('wall', x, y)
            elif level[y][x] == '0':
                Tile('fon', x, y)
            elif level[y][x] == 'f':
                Finish('finish', x, y)
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
    return new_player, x, y


if __name__ == '__main__':
    player = None
    start_screen()
    player, level_x, level_y = generate_level(load_level('map.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.speedx = 2
                    player.speedy = 0
                if event.key == pygame.K_LEFT:
                    player.speedx = -2
                    player.speedy = 0
                if event.key == pygame.K_UP:
                    player.speedy = -2
                    player.speedx = 0
                if event.key == pygame.K_DOWN:
                    player.speedy = 2
                    player.speedx = 0
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(60)
        pygame.display.update()
        pygame.display.flip()
    pygame.quit()

