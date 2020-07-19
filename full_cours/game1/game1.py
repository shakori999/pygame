try:
    import os
    import sys
    import pygame as pg
    import random
    import math
    import getopt
    from pygame.locals import *
except ImportError as err:
    print("this moudle didn't import", err)
    sys.exit(2)


def load_png(name):
    # load images and return them as objects
    fullname = os.path.join("full_cours/images", name)
    try:
        image = pg.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pg.error as message:
        print("cannot load image", fullname)
        raise SystemExit and message
    return image, image.get_rect()


class Ball(pg.sprite.Sprite):
    # a ball that wiill move across the screen
    # returns: ball object
    # functions: update, calcnewpos
    # attributs: area , vector
    def __init__(self, vector):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("ball.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos

    def calcnewpos(self, rect, vector):
        (angle, z) = vector
        (dx, dy) = (z * math.cos(angle), z * math.sin(angle))
        return rect.move(dx, dy)


## make the screen and main function
def main():
    pg.init()
    black = 0, 0, 0
    # """setup the screen"""
    size = width, height = 500, 500
    screen = pg.display.set_mode(size)

    while 1:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

        screen.fill(black)
        pg.display.flip()


if __name__ == "__main__":
    main()
