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


class Bat(pg.sprite.Sprite):
    """ 
    movable tennis "bat" with wich one hits the ball 
    return: bat object
    functions: reinit , update, moveup, movedown
    attributes: which , speed
    """

    def __init__(self, side):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("bat.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.side = side
        self.speed = 10
        self.state = "still"
        self.reinit()

    def reinit(self):
        self.state = "still"
        self.movepos = [0, 0]
        if self.side == "left":
            self.rect.midleft = self.area.midleft
        elif self.side == "right":
            self.rect.midright = self.area.midright

    def update(self):
        newpos = self.rect.move(self.movepos)
        if self.area.contains(newpos):
            self.rect = newpos
        pg.event.pump()

    def moveup(self):
        self.movepos[1] = self.movepos[1] - (self.speed)
        self.state = "moveup"

    def movedown(self):
        self.movepos[1] = self.movepos[1] + (self.speed)
        self.state = "movedown"


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
            # elif event.type == pg.KEYDOWN:
            #     if event.key == pg.K_UP:
            #         player.moveup()
            #     if event.key == pg.K_DOWN:
            #         player.movedown()
            # elif event.type == pg.KEYUP:
            #     if event.key == pg.K_UP or event.key == pg.K_DOWN:
            #         player.movepos = [0, 0]
            #         player.state = "still"

        screen.fill(black)
        pg.display.flip()


if __name__ == "__main__":
    main()
