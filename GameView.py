import pygame

class GameView:
    def __init__(self):
        self.__width = 300
        self.__height = 300
        self.__display = pygame.display.set_mode((self.__width, self.__height))
        self.__title = pygame.display.set_caption('Jogo')
        self.__FPS = pygame.time.Clock()

    def set_settings(self):
        White = (255, 255, 255)#RGB pra branco
        self.__display.fill(White)

    def frames(self):
        FPSnum = 30
        self.__FPS.tick(FPSnum)

    def update(self):
        pygame.display.update()

    def set_square(self):
        Red = (255, 0, 0)
        pygame.draw.rect(self.__display, Red, (100, 200, 100, 50), 2)