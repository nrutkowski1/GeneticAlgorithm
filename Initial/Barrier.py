import pygame as pg


class Barrier:

    def __init__(self, surface, leftp, rightp, topp, botp):
        # define a box to have a left right top and bottom point as well as a surface to be drawn on
        self.surface = surface
        self.leftp = leftp
        self.rightp = rightp
        self.topp = topp
        self.botp = botp
        # drawn in blue
        pg.gfxdraw.line(surface, leftp, botp, leftp, topp, (0, 0, 255))
        pg.gfxdraw.line(surface, leftp, topp, rightp, topp, (0, 0, 255))
        pg.gfxdraw.line(surface, rightp, topp, rightp, botp, (0, 0, 255))
        pg.gfxdraw.line(surface, rightp, botp, leftp, botp, (0, 0, 255))

    def get_leftp(self): return self.leftp

    def get_rightp(self): return self.rightp

    def get_topp(self): return self.topp

    def get_botp(self): return self.botp




