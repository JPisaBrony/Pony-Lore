import pygame
from Tile import *

WINDOW_WIDTH = 768
WINDOW_HEIGHT = 1024

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
        """
        player_middle_tile = 0

        if player.dir == 0 and player.tile_y >= 0 and player.tile_y <= len(self.tiles[0])-2:
            player_middle_tile = self.tiles[player.tile_x][player.tile_y-1]
        elif player.dir == 1 and player.tile_x >= 0 and player.tile_x <= len(self.tiles)-2:
            player_middle_tile = self.tiles[player.tile_x+1][player.tile_y]
        elif player.dir == 2 and player.tile_y >= 0 and player.tile_y <= len(self.tiles[0])-2:
            player_middle_tile = self.tiles[player.tile_x][player.tile_y+1]
        elif player.dir == 3 and player.tile_x >= 0 and player.tile_x <= len(self.tiles)-2:
            player_middle_tile = self.tiles[player.tile_x-1][player.tile_y]
        """

        self.draw_ground(window, (200,200,200))
        self.draw_ceiling(window, (200,200,200))

        if player.dir == 1:
            self.draw_wall_2(window, player.tiles_around[0][0], self.draw_left_wall, (255,255,255))
            self.draw_wall_2(window, player.tiles_around[0][2], self.draw_right_wall, (255,255,255))
            self.draw_wall_2(window, player.tiles_around[1][0], self.draw_middle_left_wall, (255,255,255))
            self.draw_wall_2(window, player.tiles_around[1][2], self.draw_middle_right_wall, (255,255,255))
            if player.tiles_around[1][1] != 0:
                self.draw_wall_2(window, player.tiles_around[1][2], self.draw_middle_front_wall, (255,255,255))
            if player.tiles_around[1][1] == 0:
                self.draw_front_wall(window, (255,255,255))

        """
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
        """


    def draw_wall_2(self, window, tile, func, color):
        if tile == 0:
            func(window, color)
        else:
            func(window, (0,0,0))

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
