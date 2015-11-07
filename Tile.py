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