import pygame, sys
from pygame.locals import *
from Map import *
from Tile import *
from Player import *

WINDOW_WIDTH = 768
WINDOW_HEIGHT = 1024
show_map = 0

def handle_events(player):
    global show_map
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                player.move_forward()
            elif event.key == K_LEFT:
                player.rotate_left()
            elif event.key == K_RIGHT:
                player.rotate_right()
            elif event.key == K_m:
                if show_map == 0:
                    show_map = 1
                else:
                    show_map = 0

def draw(window, test_map, player):
    global show_map
    window.fill((0, 0, 0))
    if show_map == 0:
        test_map.render_3d_map(window, player)
    else:
        test_map.render_map(window)
        player.render_player(window)
    pygame.display.flip()

def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_HEIGHT, WINDOW_WIDTH))
    test_map = Map(10)
    player = Player(50, test_map)
    while True:
        handle_events(player)
        draw(window, test_map, player)

if __name__ == "__main__":
    main()
