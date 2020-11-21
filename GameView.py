import pygame

from constants import *

class GameView:
    def __init__(self):
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__FPS = pygame.time.Clock()

    def starting_settings(self):
        pygame.display.set_caption(TITULO)
        self.__screen.fill(WHITE)

    def paint(self):
        #TODO - Transformar  em um background
        self.__screen.fill(WHITE)

    def update(self):
        pygame.display.update()
        self.__FPS.tick(FPS)

    def render(self, entity):
        #TODO - Passar essa função draw para o view
        entity.draw(self.__screen)
        entity.move()

    def end(self):
        self.__screen.fill(RED)
        pygame.display.update()