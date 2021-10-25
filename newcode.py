import pygame
import sys
import random
import math



class GameInfo:
    gameOver = False
    gamePause = True
    gameStop = False
    gamePoint = 0
    size = width, height = 800, 600


class Colors:
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    black = (0, 0, 0)

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
    ball_arr = []

    @staticmethod
    def clone():
        Ball.ball_arr.append(Ball("ball.png", Ball.ball_arr[0].screen))

    def __init__(self, file_name, screen, c_x=3, c_y=-3, x=GameInfo.height / 2, y=GameInfo.height / 2):
        super().__init__(file_name, screen, x, y)
        self.c_x = c_x
        self.c_y = c_y
        self.ball_arr.append(self)

    def collision_walls(self):
        if self.objectrect.x + self.objectrect.width > GameInfo.width or self.objectrect.x < 0:
            self.c_x *= -1
            self.objectrect.x += self.c_x * 2
        if self.objectrect.y < 0:
            self.c_y *= -1
            self.objectrect.y += self.c_y * 2
        if self.objectrect.y + self.objectrect.height > GameInfo.height:
            Ball.ball_arr.remove(self)
            print(len(Ball.ball_arr))
            if len(Ball.ball_arr) == 0:
                GameInfo.gameStop = True

    def collision_objects(self, allobjects):
        for objects in allobjects:
            for object in objects:
                if object != False:
                    if self.objectrect.colliderect(object.objectrect):
                        self.c_y *= -1
                        if object.baf == 0:
                            Platform_2.erase(object.lvl, object.pos)
                        elif object.baf == 1:
                            Platform_2.erase(object.lvl, object.pos)
                            Platform_2.erase(object.lvl - 1, object.pos)
                            Platform_2.erase(object.lvl, object.pos - 1)
                            Platform_2.erase(object.lvl, object.pos + 1)
                        elif object.baf == 2:
                            Platform_2.erase(object.lvl, object.pos)
                            Ball.clone()
                        break

    def collision_platform(self, platform):
        if self.objectrect.colliderect(platform.objectrect):
            self.c_y *= -1
            self.objectrect.y += self.c_y*2

    def move(self, platform, objects=[]):
        self.collision_walls()
        self.collision_objects(objects)
        self.collision_platform(platform)
        self.objectrect.x += self.c_x
        self.objectrect.y += self.c_y
        self.draw()


class Platform(Object):
    def __init__(self, file_name, screen, c_x=0, x=GameInfo.width / 2, y=GameInfo.height - 100):
        super().__init__(file_name, screen, x, y)
        self.c_x = c_x

    def collision_walls(self):
        if self.objectrect.x < 0 or self.objectrect.x > GameInfo.width - self.objectrect.width:
            self.c_x = 0
            if self.objectrect.x <= 0: self.objectrect.x = 1
            if self.objectrect.x >= GameInfo.width - self.objectrect.width: self.objectrect.x = GameInfo.width - self.objectrect.width - 1

    def move(self):
        self.collision_walls()
        self.objectrect.x += self.c_x
        self.draw()

    def right(self):
        self.c_x += 5

    def left(self):
        self.c_x -= 5

    def stop(self):
        self.c_x = 0


class Platform_2(Object):
    platform_arr = []
    width = 110

    @staticmethod
    def erase(lvl, pos):
        try:
            Platform_2.platform_arr[lvl][pos] = False
            GameInfo.gamePoint += 1
        except:
            pass

    @staticmethod
    def draws():
        for i in Platform_2.platform_arr:
            for j in i:
                if j != False:
                    j.draw()

    @staticmethod
    def new_lvl():
        Platform_2.platform_arr.append([])

    @staticmethod
    def empty():
        for i in Platform_2.platform_arr:
            for j in i:
                if j != False:
                    return False
        return True

    @staticmethod
    def generate(screen):
        t_x, t_y = (GameInfo.width % Platform_2.width) // 2, 10
        for j in range(2):
            Platform_2.new_lvl()
            arr = [0 for i in range((GameInfo.width // Platform_2.width))]
            arr[random.randint(0, len(arr)-1)] = 1
            arr[random.randint(0, len(arr)-1)] = 2
            for i in range((GameInfo.width // Platform_2.width)):
                platform_2 = Platform_2(screen, t_x, t_y, False, arr[i])
                t_x += 110
            t_y += 110
            t_x = (GameInfo.width % 110) // 2

    def __init__(self, screen, x=0, y=0, new_lvl=False, baf=0):
        if new_lvl:
            self.platform_arr.append([])
        self.platform_arr[-1].append(self)
        self.lvl = len(self.platform_arr) - 1
        self.pos = len(self.platform_arr[-1]) - 1
        self.baf = baf

        if self.baf == 0:
            super().__init__("platform_2.png", screen, x, y)
        elif self.baf == 1:
            super().__init__("platform_2_green.png", screen, x, y)
        elif self.baf == 2:
            super().__init__("platform_2_orange.png", screen, x, y)

def draw_text(text, font, color, x, y, screen):
    font = pygame.font.Font(None, font)
    text = font.render(text, 2, color)
    textPos = text.get_rect(centerx=x, centery=y)
    screen.blit(text, textPos)


def main():
    pygame.init()
    screen = pygame.display.set_mode(GameInfo.size)
    ball = Ball("ball.png", screen)
    platform = Platform("platform.png", screen)
    Platform_2.generate(screen)

    while not GameInfo.gameOver:
        if not GameInfo.gameStop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    GameInfo.gameOver = True
                if event.type == pygame.KEYDOWN:
                    GameInfo.gamePause = False
                    if event.key == pygame.K_d:
                        platform.right()
                    if event.key == pygame.K_a:
                        platform.left()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_d or event.key == pygame.K_a:
                        platform.stop()
            if GameInfo.gamePause:
                screen.fill(Colors.green)
                draw_text("Нажмите любую клавишу.", 32, Colors.black, screen.get_width()/2, screen.get_height()/2,screen)
            else:
                screen.fill(Colors.black)
                Platform_2.draws()
                for ball in Ball.ball_arr:
                    ball.move(platform, Platform_2.platform_arr)
                platform.move()
            pygame.display.flip()
            if Platform_2.empty():
                Platform_2.generate(screen)
            pygame.time.wait(10)
        else:
            screen.fill(Colors.black)
            draw_text("Ваш счёт: {}".format(GameInfo.gamePoint), 32, Colors.red, screen.get_width()/2, screen.get_height()/2,screen)
            pygame.display.flip()


main()
