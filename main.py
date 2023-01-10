import time

import pygame
import sys
from methods_lib import start_screen, load_level, generate_level, all_sprites, screen, menu_screen

FPS = 60
clock = pygame.time.Clock()


if __name__ == '__main__':
    player = None
    start_screen()
    player = generate_level(load_level('map.txt'))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and player.move:
                    player.speedx = 40
                    player.speedy = 0
                    player.move = False
                if event.key == pygame.K_LEFT and player.move:
                    player.speedx = -40
                    player.speedy = 0
                    player.move = False
                if event.key == pygame.K_UP and player.move:
                    player.speedy = -40
                    player.speedx = 0
                    player.move = False
                if event.key == pygame.K_DOWN and player.move:
                    player.speedy = 40
                    player.speedx = 0
                    player.move = False
        if player.f:
            time.sleep(1)
            player.open_menu()
        screen.fill(pygame.Color('black'))
        all_sprites.draw(screen)
        all_sprites.update()
        clock.tick(FPS)
        pygame.display.update()
        pygame.display.flip()
    pygame.display.quit()
    pygame.quit()
    sys.exit()
