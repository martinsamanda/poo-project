import pygame
import sys
import time

from pygame.locals import *
from settings import *
from game_view import GameView
from game_model import GameModel
from tilemap import Map
from os import path


class GameController:
    def __init__(self):
        pygame.init()
        self.__GameModel = GameModel(self)
        self.__GameView = GameView(self, self.__GameModel)
        self.__map = None
        self.score = 0
        self.load_data()

    def start_screen(self):
        waiting = True
        while waiting:
            self.__GameView.draw_start_screen()
            self.start_events()

    def game_over_screen(self):
        waiting = True
        self.__GameView.draw_game_over()
        #time.sleep para fazer com que a tela não desapareça mto rápido
        #um draw antes pra paralisar na tela correta
        time.sleep(1.1)
        while waiting:
            self.__GameView.draw_game_over()
            for sprite in self.__GameModel.all_sprites:
                sprite.kill()
            self.start_events()

    def win_screen(self):
        waiting = True
        self.__GameView.draw_win_screen()
        #time.sleep para fazer com que a tela não desapareça mto rápido
        #um draw antes pra paralisar na tela correta
        time.sleep(1.1)
        while waiting:
            self.__GameView.draw_win_screen()
            for sprite in self.__GameModel.all_sprites:
                sprite.kill()
            self.start_events()

    def start_game(self):
        self.score = 0
        self.load_data()
        self.__GameModel.load_map(self.__map)

        playing = True
        while playing:
            self.game_events()
            self.__GameModel.update_positions()
            self.__GameView.draw_game()

            enemy_hits = pygame.sprite.spritecollide(self.__GameModel.princess, self.__GameModel.enemies, False, pygame.sprite.collide_mask)
            door_found = pygame.sprite.spritecollide(self.__GameModel.princess, self.__GameModel.door_tile, False, pygame.sprite.collide_mask)

            if enemy_hits or door_found:
                if enemy_hits:
                    self.game_over_screen()
                if door_found:
                    self.win_screen()

    def load_data(self):
        self.__map = Map(path.join(GAME_FOLDER, 'map.txt'))

    def game_events(self):
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                #Eventos para spawnar os ataques da princesa
                if event.key == pygame.K_LEFT:
                    self.__GameModel.princess.attack(-ATTACK_RANGE,0)
                elif event.key == pygame.K_RIGHT:
                    self.__GameModel.princess.attack(ATTACK_RANGE,0)
                elif event.key == pygame.K_UP:
                    self.__GameModel.princess.attack(0,-ATTACK_RANGE/1.5)
                elif event.key == pygame.K_DOWN:
                    self.__GameModel.princess.attack(0,ATTACK_RANGE/1.5)

    def start_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                self.start_game()
