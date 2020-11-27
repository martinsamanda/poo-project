import pygame
import random

from abc import ABC, abstractmethod
from constants import *
from pygame.locals import *

class Character(ABC, pygame.sprite.Sprite):
    def __init__(self, image_link, width, height, position: tuple, pixel_mov):
        super().__init__()
        #self.__image = pygame.image.load(image_link)
        self.__surf = pygame.Surface((width, height))
        self.__rect = self.__surf.get_rect(center=position)
        self.pixel_mov = pixel_mov

        #Todo - substituir o quadrado por imagems
        self.__image = self.__surf

    @property
    def rect(self):
        return self.__rect

    @abstractmethod
    def move(self):
        # Movimento que o personagem faz
        pass

    #TODO - Passar isso para o view
    def draw(self, surface: pygame.surface):
        # Desenha o personagem em uma tela
        try:
            surface.blit(self.__image, self.__rect)
        except AttributeError as ex:
            print(f'Houve um erro ao tentar desenhar um personagem. Erro - {ex}')
            pygame.quit()


class Princess(Character):
    def __init__(self):
        super().__init__(PRINCESS_IMG, 50, 100, (100, 100), 20)

    def move(self):
        pressed_key = pygame.key.get_pressed()

        if self.rect.top > 0:
            if pressed_key[K_UP]:
                self.rect.move_ip(0, - self.pixel_mov)

        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_key[K_DOWN]:
                self.rect.move_ip(0, self.pixel_mov)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_key[K_RIGHT]:
                self.rect.move_ip(self.pixel_mov, 0)

        if self.rect.left > 0:
            if pressed_key[K_LEFT]:
                self.rect.move_ip(- self.pixel_mov, 0)


class Orc(Character):
    def __init__(self):
        super().__init__(ORC_IMG, 50, 80, (random.randint(40, 360), random.randint(160, 400)), 10)

    def move(self):
        # Se move 5 pixels para a direita, se bater no canto direito, se move -5 até bater no canto esquerdo.
        self.rect.move_ip(self.pixel_mov, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.pixel_mov = - self.pixel_mov
        elif self.rect.left < 0:
            self.pixel_mov = - self.pixel_mov

