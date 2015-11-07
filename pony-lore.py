import pygame, sys
from pygame.locals import *

WINDOW_WIDTH = 768
WINDOW_HEIGHT = 1024
show_map = 0

class Tile:
    def __init__(self, x, y, w, h, color, edge_color):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.n_edge = 0
        self.e_edge = 0
        self.s_edge = 0
        self.w_edge = 0
        self.edge_color = edge_color

    def set_edge(self, dir, val):
        if dir == 0:
            self.n_edge = val
        if dir == 1:
            self.e_edge = val
        if dir == 2:
            self.s_edge = val
        if dir == 3:
            self.w_edge = val

class Map:
    def __init__(self, map_size):
        squares = [[0 for x in range(map_size)] for x in range(map_size)]
        size = 50
        color = (255, 255, 255)
        edge_color = (200, 200, 200)

        for i in range(10):
            self.add_to_map(squares, i, 0, size, color, edge_color)

        for i in range(10):
            self.add_to_map(squares, 9, i, size, color, edge_color)

        for i in range(10):
            self.add_to_map(squares, i, 4, size, color, edge_color)

        for i in range(10):
            self.add_to_map(squares, 4, i, size, color, edge_color)

        self.tiles = squares
        self.add_edges()

    def add_edges(self):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[0])):
                if self.tiles[i][j] != 0:
                    if i+1 <= 9:
                        if self.tiles[i+1][j] == 0:
                            self.tiles[i][j].e_edge = 1
                    else:
                        self.tiles[i][j].e_edge = 1
                    if i-1 >= 0:
                        if self.tiles[i-1][j] == 0:
                            self.tiles[i][j].w_edge = 1
                    else:
                        self.tiles[i][j].w_edge = 1
                    if j+1 <= 9:
                        if self.tiles[i][j+1] == 0:
                            self.tiles[i][j].s_edge = 1
                    else:
                        self.tiles[i][j].s_edge = 1
                    if j-1 >= 0:
                        if self.tiles[i][j-1] == 0:
                            self.tiles[i][j].n_edge = 1
                    else:
                        self.tiles[i][j].n_edge = 1

    def add_to_map(self, squares, x, y, size, color, edge_color):
        squares[x][y] = Tile(size * x, size * y, size, size, color, edge_color)

    def render_map(self, window):
        for i in self.tiles:
            for j in i:
                if j != 0:
                    pygame.draw.rect(window, j.color, (j.x, j.y, j.w, j.h))
                    if j.n_edge:
                        pygame.draw.rect(window, j.edge_color, (j.x, j.y, j.w, 2))
                    if j.e_edge:
                        pygame.draw.rect(window, j.edge_color, (j.x + j.w - 2, j.y, 2, j.h))
                    if j.s_edge:
                        pygame.draw.rect(window, j.edge_color, (j.x, j.y + j.h - 2, j.w, 2))
                    if j.w_edge:
                        pygame.draw.rect(window, j.edge_color, (j.x, j.y, 2, j.h))

    def render_3d_map(self, window, player):
        player_middle_tile = 0
        
        if player.dir == 0 and player.tile_y >= 0 and player.tile_y <= len(self.tiles[0])-2:
            player_middle_tile = self.tiles[player.tile_x][player.tile_y-1]
        elif player.dir == 1 and player.tile_x >= 0 and player.tile_x <= len(self.tiles)-2:
            player_middle_tile = self.tiles[player.tile_x+1][player.tile_y]
        elif player.dir == 2 and player.tile_y >= 0 and player.tile_y <= len(self.tiles[0])-2:
            player_middle_tile = self.tiles[player.tile_x][player.tile_y+1]
        elif player.dir == 3 and player.tile_x >= 0 and player.tile_x <= len(self.tiles)-2:
            player_middle_tile = self.tiles[player.tile_x-1][player.tile_y]

        self.draw_ground(window, (200,200,200))
        self.draw_ceiling(window, (200,200,200))

        player_tile = self.tiles[player.tile_x][player.tile_y]

        if player.dir == 0:
            self.draw_wall(window, player_tile.w_edge, self.draw_left_wall, (255,255,255))
            self.draw_wall(window, player_tile.e_edge, self.draw_right_wall, (255,255,255))
            self.draw_wall(window, player_tile.n_edge, self.draw_front_wall, (255,255,255))
        if player.dir == 1:
            self.draw_wall(window, player_tile.n_edge, self.draw_left_wall, (255,255,255))
            self.draw_wall(window, player_tile.s_edge, self.draw_right_wall, (255,255,255))
            self.draw_wall(window, player_tile.e_edge, self.draw_front_wall, (255,255,255))
            if player_middle_tile != 0:
                self.draw_wall(window, player_middle_tile.n_edge, self.draw_middle_left_wall, (255,255,255))
                self.draw_wall(window, player_middle_tile.s_edge, self.draw_middle_right_wall, (255,255,255))
        if player.dir == 2:
            self.draw_wall(window, player_tile.e_edge, self.draw_left_wall, (255,255,255))
            self.draw_wall(window, player_tile.w_edge, self.draw_right_wall, (255,255,255))
            self.draw_wall(window, player_tile.s_edge, self.draw_front_wall, (255,255,255))
        if player.dir == 3:
            self.draw_wall(window, player_tile.s_edge, self.draw_left_wall, (255,255,255))
            self.draw_wall(window, player_tile.n_edge, self.draw_right_wall, (255,255,255))
            self.draw_wall(window, player_tile.w_edge, self.draw_front_wall, (255,255,255))
    
    def draw_wall(self, window, edge, func, color):
        if edge == 1:
            func(window, color)
        else:
            func(window, (0,0,0))

    def draw_left_wall(self, window, color):
        pygame.draw.polygon(window, color, ((0, 0), (WINDOW_HEIGHT / 8, WINDOW_WIDTH / 8), (WINDOW_HEIGHT / 8, (WINDOW_WIDTH / 8) * 7), (0, WINDOW_WIDTH)))

    def draw_middle_left_wall(self, window, color):
        pygame.draw.polygon(window, color, ((WINDOW_HEIGHT / 8, WINDOW_WIDTH / 8), (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4), (WINDOW_HEIGHT / 4, (WINDOW_WIDTH / 4) * 3), (WINDOW_HEIGHT / 8, (WINDOW_WIDTH / 8) * 7)))

    def draw_right_wall(self, window, color):
        pygame.draw.polygon(window, color, ((WINDOW_HEIGHT, 0), ((WINDOW_HEIGHT / 8) * 7, WINDOW_WIDTH / 8), ((WINDOW_HEIGHT / 8) * 7, (WINDOW_WIDTH / 8) * 7), (WINDOW_HEIGHT, WINDOW_WIDTH)))
    
    def draw_middle_right_wall(self, window, color):
        pygame.draw.polygon(window, color, (((WINDOW_HEIGHT / 8) * 7, WINDOW_WIDTH / 8), ((WINDOW_HEIGHT / 4) * 3, WINDOW_WIDTH / 4), ((WINDOW_HEIGHT / 4) * 3, (WINDOW_WIDTH / 4) * 3), ((WINDOW_HEIGHT / 8) * 7, (WINDOW_WIDTH / 8) * 7)))

    def draw_front_wall(self, window, color):
        pygame.draw.rect(window, color, (WINDOW_HEIGHT / 8, WINDOW_WIDTH / 8, WINDOW_HEIGHT / 1.333333, WINDOW_WIDTH / 1.333333))

    def draw_middle_front_wall(self, window, color):
        pygame.draw.rect(window, color, (WINDOW_HEIGHT / 4, WINDOW_WIDTH / 4, WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2))

    def draw_ground(self, window, color):
        pygame.draw.polygon(window, color, ((0, WINDOW_WIDTH), (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2), (WINDOW_HEIGHT, WINDOW_WIDTH)))

    def draw_ceiling(self, window, color):
        pygame.draw.polygon(window, color, ((0,0), (WINDOW_HEIGHT / 2, WINDOW_WIDTH / 2), (WINDOW_HEIGHT, 0)))

class Player:
    def __init__(self, tile_size):
        self.x = tile_size / 4
        self.y = tile_size / 4
        self.tile_x = 0
        self.tile_y = 0
        self.color = (100, 100, 100)
        self.w = tile_size / 2
        self.h = tile_size / 2
        self.dir = 1
        self.tile_size = tile_size
        self.player_surface = self.create_player_surface()

    def create_player_surface(self):
        player = pygame.Surface([self.w, self.h])
        player.fill((255, 255, 255))
        pygame.draw.line(player, self.color, (0, self.h/2), (self.w, self.h/2))
        pygame.draw.line(player, self.color, (self.w/2, 0), (self.w, self.h/2))
        pygame.draw.line(player, self.color, (self.w/2, self.h), (self.w, self.h/2))
        return player

    def render_player(self, window):
        window.blit(self.player_surface, (self.x, self.y))
    
    def move_forward(self):
        if self.dir == 0:
            self.y -= self.tile_size
            self.tile_y -= 1
        elif self.dir == 1:
            self.x += self.tile_size
            self.tile_x += 1
        elif self.dir == 2:
            self.y += self.tile_size
            self.tile_y += 1
        elif self.dir == 3:
            self.x -= self.tile_size
            self.tile_x -= 1

    def rotate_left(self):
        if self.dir > 0:
            self.dir -= 1
        else:
            self.dir = 3
        self.player_surface = pygame.transform.rotate(self.player_surface, 90)

    def rotate_right(self):
        if self.dir < 3:
            self.dir += 1
        else:
            self.dir = 0
        self.player_surface = pygame.transform.rotate(self.player_surface, -90)

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
    player = Player(50)
    while True:
        handle_events(player)
        draw(window, test_map, player)

if __name__ == "__main__":
    main()
