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
## make the screen and main function
def main():
    pg.init()
    black = 0, 0, 0
    # setup the screen
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
