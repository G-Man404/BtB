import pygame
import sys
import random

size = width, height = 800, 600

class Object:
    def __init__(self, file_name, screen, x=0, y=0):
        self.screen = screen
        self.object = pygame.image.load(file_name)
        self.objectrect = self.object.get_rect()
        self.objectrect.x = x
        self.objectrect.y = y

    def draw(self):
        self.screen.blit(self.object, self.objectrect)

class Ball(Object):
    def __init__(self, file_name, screen, c_x=5, c_y=5, x=height/2, y=height/2, side_x=100, side_y=100):
        super().__init__(file_name, screen, x, y)
        self.c_x = c_x
        self.c_y = c_y

    def get_collision(self, object=False):
            if self.objectrect.x+self.objectrect.width > width or self.objectrect.x < 0:
                self.c_x *= -1
            if self.objectrect.y+self.objectrect.height > height or self.objectrect.y < 0:
                self.c_y *= -1
            if object != False:
                if self.objectrect.x+self.objectrect.width>object.objectrect.x and self.objectrect.x < object.objectrect.x +\
                        object.objectrect.width and self.objectrect.y+self.objectrect.height > object.objectrect.y:
                    self.c_y *= -1

    def move(self, object = False):
        self.objectrect.x += self.c_x
        self.objectrect.y += self.c_y
        self.get_collision(object)
        self.draw()

class Platform(Object):
    def __init__(self, file_name, screen, c_x=0, x=width/2, y=height-100):
        super().__init__(file_name, screen, x, y)
        self.c_x = c_x

    def get_collision(self):
        if self.objectrect.x < 0 or self.objectrect.x > width-self.objectrect.width:
            self.c_x = 0


    def move(self):
        self.objectrect.x += self.c_x
        self.get_collision()
        self.draw()
def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    black = 0,0,0
    ball = Ball("ball.png", screen)
    platform = Platform("platform.png", screen)
    gameover = False
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    platform.c_x = 5
                if event.key == pygame.K_a:
                    platform.c_x = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    platform.c_x = 0
        screen.fill(black)
        platform.move()
        ball.move(platform)
        pygame.display.flip()
        pygame.time.wait(10)
    sys.exit()
main()
