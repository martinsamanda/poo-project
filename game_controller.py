import pygame
import sys
import time

from pygame.locals import *
from settings import *
from game_view import GameView
from game_model import GameModel
from sounds import Sound


class GameController:
    def __init__(self):
        pygame.init()
        self.__GameModel = GameModel(self)
        self.__GameView = GameView(self, self.__GameModel)
        self.__sounds = Sound()

    def start_screen(self):
        self.__sounds.princess_hit_sound()
        self.__sounds.background_sound()
        waiting = True
        while waiting:
            self.__GameView.draw_start_screen()
            self.start_events()

    def game_over_screen(self):
        self.__sounds.orc_sound()
        waiting = True
        new_highscore = False
        if self.__GameModel.score > self.__GameModel.highscore.data:
            self.__GameModel.highscore.new_hs(self.__GameModel.score)
            new_highscore = True

        self.__GameView.draw_game_over(new_highscore)
        #time.sleep para fazer com que a tela não desapareça mto rápido
        #um draw antes pra paralisar na tela correta
        time.sleep(1.1)
        while waiting:
            self.__GameView.draw_game_over(new_highscore)
            for sprite in self.__GameModel.all_sprites:
                sprite.kill()
            self.start_events()

    def win_screen(self):
        waiting = True
        new_highscore = False
        if self.__GameModel.score > self.__GameModel.highscore.data:
            self.__GameModel.highscore.new_hs(self.__GameModel.score)
            new_highscore = True

        self.__GameView.draw_win_screen(new_highscore)
        #time.sleep para fazer com que a tela não desapareça mto rápido
        #um draw antes pra paralisar na tela correta
        time.sleep(1.1)
        while waiting:
            self.__GameView.draw_win_screen(new_highscore)
            for sprite in self.__GameModel.all_sprites:
                sprite.kill()
            self.start_events()

    def start_game(self):
        self.__GameModel.score = 0
        self.__GameModel.load_map()

        playing = True
        while playing:
            self.game_events()
            self.__GameModel.update_positions()
            self.__GameView.draw_game()

            enemy_hits = pygame.sprite.spritecollide(self.__GameModel.princess, self.__GameModel.enemies, False, pygame.sprite.collide_mask)
            door_found = pygame.sprite.collide_rect(self.__GameModel.princess, self.__GameModel.door_tile)

            if enemy_hits or door_found:
                if enemy_hits:
                    self.game_over_screen()
                if door_found:
                    self.win_screen()

    def game_events(self):
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

    def start_events(self):
        #self.__sounds.background_sound()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                self.start_game()
