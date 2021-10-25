import pygame
import sys
import random
import math

size = width, height = 800, 600
platform_2_width = 110

stopgame = False

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
                self.objectrect.x += self.c_x*2
            if self.objectrect.y < 0:
                self.c_y *= -1
                self.objectrect.y += self.c_y*2
            if self.objectrect.y+self.objectrect.height > height:
                global stopgame
                stopgame = True
            if object != False:
                if self.objectrect.colliderect(object.objectrect):
                    self.c_y *= -1
                    self.objectrect.y += self.c_y
                    if isinstance(object, Platform_2):
                        if object.baf == 0:
                            Platform_2.erase(object.lvl, object.pos)
                        elif object.baf == 1:
                            Platform_2.erase(object.lvl, object.pos)
                            Platform_2.erase(object.lvl-1, object.pos)
                            print(object.lvl)
                            Platform_2.erase(object.lvl, object.pos-1)
                            Platform_2.erase(object.lvl, object.pos+1)


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


class Platform_2(Object):
    platform_arr = [[]]
    point = 0

    @staticmethod
    def erase(lvl, pos):
        try:
            Platform_2.platform_arr[lvl][pos] = False
            Platform_2.point += 1
        except:
            pass


    def __init__(self, file_name, screen, x=0, y=0, new_lvl = False, baf = 0):
        if baf == 0:
            super().__init__(file_name, screen, x, y)
        if baf == 1:
            super().__init__("platform_2_green.png", screen, x, y)

        if new_lvl:
            self.platform_arr.append([])
        self.platform_arr[-1].append(self)
        self.lvl = len(self.platform_arr)-1
        self.pos = len(self.platform_arr[-1])-1
        self.baf = baf

def main():
    global stopgame
    pygame.init()
    screen = pygame.display.set_mode(size)
    black = 0,0,0
    ball = Ball("ball.png", screen)
    platform = Platform("platform.png", screen)
    t_x, t_y = (width % platform_2_width) // 2, 10
    for j in range(2):
        platform_2 = Platform_2("platform_2.png", screen, t_x, t_y, True,1)
        for i in range((width // platform_2_width)):
            platform_2 = Platform_2("platform_2.png", screen, t_x, t_y)
            t_x += 110
        t_y += 110
        t_x = (width % 110) // 2

    gameover = False
    startgame = False
    max_point = len(Platform_2.platform_arr)
    while not gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameover = True
            if event.type == pygame.KEYDOWN:
                startgame = True
                if event.key == pygame.K_d:
                    platform.c_x = 5
                if event.key == pygame.K_a:
                    platform.c_x = -5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d or event.key == pygame.K_a:
                    platform.c_x = 0
        if startgame:
            flag = False
            for i in Platform_2.platform_arr:
                for j in i:
                    if j != 0:
                        flag = True
            if not flag:
                t_x, t_y = (width % platform_2_width) // 2, 10
                for j in range(2):
                    platform_2 = Platform_2("platform_2.png", screen, t_x, t_y, True)
                    for i in range((width // platform_2_width)):
                        platform_2 = Platform_2("platform_2.png", screen, t_x, t_y)
                        t_x += 110
                    t_y += 110
                    t_x = (width % 110) // 2

            if stopgame:
                screen.fill((255,0,0))
                font = pygame.font.Font(None, 36)
                text = font.render("Game Over! Your result: {}".format(Platform_2.point).format(0), 2, (10, 10, 10))
                textpos = text.get_rect(centerx=screen.get_width() / 2, centery = screen.get_height() / 2)
                screen.blit(text, textpos)
                pygame.display.flip()
            else:
                screen.fill(black)
                for i in Platform_2.platform_arr:
                    for j in i:
                        if j != False:
                            j.draw()
                            ball.get_collision(j)
                platform.move()
                ball.move(platform)
                pygame.display.flip()
                pygame.time.wait(10)
        else:
            screen.fill((0, 255, 0))
            font = pygame.font.Font(None, 36)
            text = font.render("Нажмите любую кнопку что бы начать игру", 2, (10, 10, 10))
            textpos = text.get_rect(centerx=screen.get_width() / 2, centery=screen.get_height() / 2)
            screen.blit(text, textpos)
            pygame.display.flip()
    sys.exit()
main()
