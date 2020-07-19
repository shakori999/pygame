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
    def __init__(self, xy, vector):
        pg.sprite.Sprite.__init__(self)
        self.image, self.rect = load_png("ball.png")
        screen = pg.display.get_surface()
        self.area = screen.get_rect()
        self.vector = vector
        self.hit = 0

    def update(self):
        newpos = self.calcnewpos(self.rect, self.vector)
        self.rect = newpos
        (angle, z) = self.vector

        if not self.area.contains(newpos):
            tl = not self.area.collidepoint(newpos.topleft)
            tr = not self.area.collidepoint(newpos.topright)
            bl = not self.area.collidepoint(newpos.bottomleft)
            br = not self.area.collidepoint(newpos.bottomright)
            if tr and tl or (br and bl):
                angle = -angle
            # if tl and bl:
            #     # self.offcourt(player=2)
            # if tr and br:
            #     # self.offcourt(player=1)
        else:
            player1.rect.inflate(-3, -3)
            player2.rect.inflate(-3, -3)
            if self.rect.colliderect(player1.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.rect.colliderect(player2.rect) == 1 and not self.hit:
                angle = math.pi - angle
                self.hit = not self.hit
            elif self.hit:
                self.hit = not self.hit
        self.vector = (angle, z)

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
        # filled_rect = pg.Rect(100, 100, 25, 150)
        # bat = pg.draw.rect(screen, (125, 214, 129), filled_rect)
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
    size = width, height = 1900, 1050
    screen = pg.display.set_mode(size)

    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((150, 200, 100))

    # initialise players
    global player1
    global player2
    player1 = Bat("left")
    player2 = Bat("right")

    # """setup the screen"""
    speed = 13
    ball = Ball((0, 0), (0.46, speed))

    ballsprite = pg.sprite.RenderPlain(ball)
    playersprites = pg.sprite.RenderPlain(player1, player2)

    screen.blit(background, (0, 0))
    pg.display.flip()

    clock = pg.time.Clock()
    while 1:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_a:
                    player1.moveup()
                if event.key == pg.K_z:
                    player1.movedown()
                if event.key == pg.K_DOWN:
                    player2.movedown()
                if event.key == pg.K_UP:
                    player2.moveup()
            elif event.type == pg.KEYUP:
                if event.key == pg.K_UP or event.key == pg.K_DOWN:
                    player2.movepos = [0, 0]
                    player2.state = "still"
                if event.key == pg.K_a or event.key == pg.K_z:
                    player1.movepos = [0, 0]
                    player1.state = "still"

        screen.blit(background, ball.rect, ball.rect)
        screen.blit(background, player1.rect, player1.rect)
        screen.blit(background, player2.rect, player2.rect)
        ballsprite.update()
        playersprites.update()
        ballsprite.draw(screen)
        playersprites.draw(screen)
        pg.display.flip()


if __name__ == "__main__":
    main()
