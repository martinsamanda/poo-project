from abc import ABC, abstractmethod
from os import path, listdir

import pygame
from pygame import mixer
from pygame.locals import *
from settings import *


class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        super().__init__()
        self.__image = pygame.Surface((TILESIZE / 1.5, TILESIZE))
        self.__rect = self.__image.get_rect()
        self.__pos = pos
        self.__rect.center = self.__pos
        self.__spawn_time = pygame.time.get_ticks()
        self.__model = model
        self.__image.fill(BLACK)
        self.__image.set_colorkey(BLACK)

        self.__model.all_sprites.add(self)
        # TODO - Só por motivos de debug, remover depois!
        self.__model.characters.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    def update(self):
        # Checa se o ataque acertou algum inimigo e aumenta o score
        enemy_hits = pygame.sprite.spritecollide(self, self.__model.enemies, True)
        for hit in enemy_hits:
            pygame.mixer.init()
            princesshit = mixer.Sound(path.join(SOUNDS_FOLDER, PRINCESS_HITTING))
            princesshit.play()
            self.__model.score += 10
        # Checa se o ataque acertou um bloco destrutivel
        pygame.sprite.spritecollide(self, self.__model.destructive_tiles, True)
        # se o destrutivel for do tipo coin, aumenta score
        broken_coin_tiles = pygame.sprite.spritecollide(self, self.__model.coin_tiles, True)
        for broke in broken_coin_tiles:
            self.__model.score += 5
        # Destroi o ataque apos certo tempo
        if pygame.time.get_ticks() - self.__spawn_time > ATTACK_LIFETIME:
            self.kill()
            self.__model.princess.attacking = False