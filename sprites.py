import pygame
import random

from abc import ABC, abstractmethod
from settings import *
from pygame.locals import *

#Alias
vec = pygame.math.Vector2


class Character(ABC, pygame.sprite.Sprite):
    def __init__(self, image_link, width, height, position_x, position_y, model):
        super().__init__()
        #self.__image = pygame.image.load(image_link)
        self.__image = pygame.Surface((width, height))
        self.__rect = self.__image.get_rect()
        self.pos = vec(position_x, position_y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.model = model

        self.model.characters.add(self)
        self.model.all_sprites.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    @abstractmethod
    def update(self):
        # Movimento que o personagem faz
        self.wall_collisions()

    def wall_collisions(self):
        self.rect.centerx = self.pos.x
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False):
            if self.vel.x > 0:
                self.vel.x = 0
                self.rect.right = wall.rect.left
            elif self.vel.x < 0:
                self.vel.x = 0
                self.rect.left = wall.rect.right
            self.pos.x = self.rect.centerx

        self.rect.centery = self.pos.y
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False):
            if self.vel.y > 0:
                self.vel.y = 0
                self.rect.bottom = wall.rect.top
            elif self.vel.y < 0:
                self.vel.y = 0
                self.rect.top = wall.rect.bottom
            self.pos.y = self.rect.centery


class Princess(Character):
    def __init__(self, model, position_x, position_y):
        super().__init__(PRINCESS_IMG, 52, 60, position_x * TILESIZE, position_y * TILESIZE, model)

    def update(self):
        self.acc = vec(0,PLAYER_GRAV)
        pressed_key = pygame.key.get_pressed()

        if pressed_key[K_RIGHT] or pressed_key[K_d]:
            self.acc.x = PLAYER_ACC

        if pressed_key[K_LEFT] or pressed_key[K_a]:
            self.acc.x = -PLAYER_ACC

        self.acc.x += self.vel.x * PLAYER_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        self.wall_collisions()


class Orc(Character):
    def __init__(self):
        super().__init__(ORC_IMG, 50, 80, random.randint(40, 360), random.randint(160, 400))

    def update(self):
        # Se move 5 pixels para a direita, se bater no canto direito, se move -5 até bater no canto esquerdo.
        self.rect.move_ip(self.pixel_mov, 0)

        if self.rect.right > SCREEN_WIDTH:
            self.pixel_mov = - self.pixel_mov
        elif self.rect.left < 0:
            self.pixel_mov = - self.pixel_mov


class Tile(ABC ,pygame.sprite.Sprite):
    def __init__(self, image_link, position_x, position_y, model):
        super().__init__()
        #self.__image = pygame.image.load(image_link)
        self.__image = pygame.Surface((TILESIZE, TILESIZE))
        self.__rect = self.__image.get_rect()
        self.__rect.x = position_x * TILESIZE
        self.__rect.y = position_y * TILESIZE
        self.model = model

        self.model.tiles.add(self)
        self.model.all_sprites.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image


class Unbreakable(Tile):
    def __init__(self, image_link,position_x, position_y, model):
        super().__init__(image_link,position_x, position_y, model)
        self.image.fill(BLUE)


class Breakable(Tile):
    def __init__(self, image_link, position_x, position_y, model):
        super().__init__(image_link, position_x, position_y, model)
        self.image.fill(GREEN)




