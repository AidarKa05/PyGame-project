import pygame
import sys
from methods_lib import start_screen, load_level, generate_level, all_sprites, screen, level_up, clear, maps, levels
from methods_lib import lose_screen, choose_pers

FPS = 60
clock = pygame.time.Clock()

if __name__ == '__main__':
    player = None
    start_screen()
    choose_pers()
    running = True
    while running:
        if level_up:
            levels += 1
            if levels > 1:
                levels = 1
            else:
                player, fn = generate_level(load_level(maps[levels]))
                level_up = False
        if player.up_lv:
            clear()
            level_up = True
        if player.on_trap:
            lose_screen()
            clear()
            player, fn = generate_level(load_level(maps[levels]))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and player.move:
                    player.speedx = 40
                    player.speedy = 0
                    player.move = False
                    player.rt = True
                    player.lf = False
                    player.dw = False
                    player.up = False
                if event.key == pygame.K_LEFT and player.move:
                    player.speedx = -40
                    player.speedy = 0
                    player.move = False
                    player.rt = False
                    player.lf = True
                    player.dw = False
                    player.up = False
                if event.key == pygame.K_UP and player.move:
                    player.speedy = -40
                    player.speedx = 0
                    player.move = False
                    player.rt = False
                    player.lf = False
                    player.dw = False
                    player.up = True
                if event.key == pygame.K_DOWN and player.move:
                    player.speedy = 40
                    player.speedx = 0
                    player.move = False
                    player.rt = False
                    player.lf = False
                    player.dw = True
                    player.up = False
        if player.rect.x == fn.rect.x and player.rect.y == fn.rect.y:
            player.f = True
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
