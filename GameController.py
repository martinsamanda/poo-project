import pygame
import sys
import time

from pygame.locals import *
from GameView import GameView
from Characters import Princess, Orc

class GameController:
    def __init__(self):
        pygame.init()
        self.__GameView = GameView()

    def start(self):
        self.__GameView.starting_settings()

        #TODO - Colocar isso em um model
        princess = Princess()
        orc = Orc()

        enemies = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()

        enemies.add(orc)
        all_sprites.add(orc)
        all_sprites.add(princess)
        #Todo - Colocar isso em um model

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()

            # Todo futuro background
            self.__GameView.paint()

            # TODO pegar essa lista do model
            for entity in all_sprites:
                self.__GameView.render(entity)

            # Todo pegar valores do model
            if pygame.sprite.spritecollideany(princess, enemies):
                self.__GameView.end()
                for entity in all_sprites:
                    entity.kill()
                time.sleep(2)
                self.quit()

            self.__GameView.update()

    def quit(self):
        pygame.quit()
        sys.exit()