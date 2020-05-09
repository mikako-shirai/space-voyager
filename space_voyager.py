
import sys
from math import radians, sin, cos
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_SPACE, K_LEFT, K_RIGHT, K_UP, K_DOWN, Rect

WIDTH = 600
HEIGHT = 600
MISSILE_MAX = 5

class Rock():
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 23, 23)
        self.rect.center = (x, y)
        self.explode = False
        self.image = pygame.image.load("rock 25.png").convert_alpha()
        self.burst = pygame.image.load("explosion 40.png").convert_alpha()
        self.theta = randint(150, 180)
        self.speed = randint(2, 13)
        self.x_move = cos(radians(self.theta)) * self.speed
        self.y_move = sin(radians(self.theta)) * self.speed

    def draw(self):
        rotated = pygame.transform.rotozoom(self.image, self.theta, 1.0)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
        if self.explode:
            SURFACE.blit(self.burst, rect)

    def move(self):
        self.theta += 5
        rect = self.rect.center
        xpos = (rect[0] + self.x_move) % WIDTH
        ypos = (rect[1] + self.y_move)
        self.rect.center = (xpos, ypos)

class Ship():
    def __init__(self):
        self.rect = Rect(WIDTH / 2, HEIGHT - 50, 22, 37)
        self.explode = False
        self.image = pygame.image.load("ship 22.png").convert_alpha()
        self.burst = pygame.image.load("explosion 40.png").convert_alpha()

    def draw(self):
        rect = self.image.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(self.image, rect)
        if self.explode:
            SURFACE.blit(self.burst, rect)

class Missile():
    def __init__(self, x, y):
        self.rect = Rect(0, 0, 5, 5)
        self.rect.center = (x, y)
        self.speed = 20
        self.image = pygame.image.load("missile 10.png").convert_alpha()
        self.x_move = 0
        self.y_move = sin(radians(-90)) * self.speed

    def draw(self):
        rect = self.image.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(self.image, rect)

    def move(self):
        rect = self.rect.center
        xpos = (rect[0] + self.x_move)
        ypos = (rect[1] + self.y_move)
        self.rect.center = (xpos, ypos)

pygame.init()
pygame.key.set_repeat(10, 10)
SURFACE = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Voyager")

def main():
    message_font = pygame.font.SysFont(None, 37)
    message_clear = message_font.render("CLEARED!", True, (0, 255, 0))
    message_over = message_font.render("GAME OVER!", True, (200, 10, 10))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH / 2, HEIGHT - 30)

    keylist = []
    rocks = []
    missile_count = 0
    on_fire = False
    back_image = pygame.image.load("back.jpg").convert()
    back_rect = back_image.get_rect()
    clock = pygame.time.Clock()
    ship = Ship()
    game_over = False
    while len(rocks) < 20:
        rock = Rock(randint(500, WIDTH), randint(30, HEIGHT - 200))
        rocks.append(rock)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key not in keylist:
                    keylist.append(event.key)
            elif event.type == KEYUP:
                keylist.remove(event.key)
            if K_LEFT in keylist and ship.rect.centerx > 11:
                ship.rect.centerx -= 2
            elif K_RIGHT in keylist and ship.rect.centerx < 589:
                ship.rect.centerx += 2
            elif K_UP in keylist:
                ship.rect.centery -= 3
            elif K_DOWN in keylist and ship.rect.centery < 576:
                ship.rect.centery += 3

        if not game_over:
            if ship.rect.centery < 20:
                game_over = True
            for rock in rocks:
                rock.move()
                if rock.rect.colliderect(ship.rect):
                    ship.explode = True
                    game_over = True
            for rock in rocks:
                if rock.rect.centery > 500:
                    rock.rect.centerx = randint(500, WIDTH)
                    rock.rect.centery = randint(100, HEIGHT - 100)
            if on_fire:
                missile.move()
                if missile.rect.centery < 20:
                    on_fire = False
                    missile = None
            for rock in rocks:
                if rock.explode:
                    rocks.remove(rock)
            if on_fire:
                for rock in rocks:
                    if rock.rect.colliderect(missile.rect):
                        rock.explode = True
            if K_SPACE in keylist:
                if missile_count < MISSILE_MAX:
                    if not on_fire:
                        missile = Missile(ship.rect.centerx, ship.rect.centery)
                        missile_count += 1
                        on_fire = True

            SURFACE.fill((0, 0, 0))
            SURFACE.blit(back_image, back_rect)
            for rock in rocks:
                rock.draw()
            ship.draw()
            if on_fire:
                missile.draw()
            if game_over:
                if not ship.explode:
                    SURFACE.blit(message_clear, message_rect.topleft)
                else:
                    SURFACE.blit(message_over, message_rect.topleft)
            pygame.display.update()
            clock.tick(10)

if __name__ == '__main__':
    main()
