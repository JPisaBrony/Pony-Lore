import pygame

class Player:
    def __init__(self, tile_size, cur_map):
        self.x = tile_size / 4
        self.y = tile_size / 4
        self.tile_x = 0
        self.tile_y = 0
        self.color = (100, 100, 100)
        self.w = tile_size / 2
        self.h = tile_size / 2
        self.dir = 1
        self.tile_size = tile_size
        self.cur_map = cur_map
        self.tiles_around_size = 3
        self.tiles_around = [[0 for x in range(self.tiles_around_size)] for x in range(self.tiles_around_size)]
        self.getTilesAround()
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

    def getTilesAround(self):
        for i in range(self.tiles_around_size):
            for j in range(self.tiles_around_size):
                if self.dir == 0:
                    self.setAroundPlayerTile(i, j, -1, -2)
                elif self.dir == 1:
                    self.setAroundPlayerTile(i, j, 0, -1)
                elif self.dir == 2:
                    self.setAroundPlayerTile(i, j, -1, 0)
                elif self.dir == 3:
                    self.setAroundPlayerTile(i, j, -2, -1)

    def setAroundPlayerTile(self, i, j, m_i, m_j):
        x = self.tile_x+i+m_i
        y = self.tile_y+j+m_j
        if x >= 0 and y >= 0 and x <= len(self.cur_map.tiles)-1 and y <= len(self.cur_map.tiles[0])-1:
            self.tiles_around[i][j] = self.cur_map.tiles[x][y]
        else:
            self.tiles_around[i][j] = 0

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
        self.getTilesAround()

    def rotate_left(self):
        if self.dir > 0:
            self.dir -= 1
        else:
            self.dir = 3
        self.player_surface = pygame.transform.rotate(self.player_surface, 90)
        self.getTilesAround()

    def rotate_right(self):
        if self.dir < 3:
            self.dir += 1
        else:
            self.dir = 0
        self.player_surface = pygame.transform.rotate(self.player_surface, -90)
        self.getTilesAround()
