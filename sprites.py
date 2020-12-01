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

    @abstractmethod
    def wall_collisions(self):
        pass


class Princess(Character):
    def __init__(self, position_x, position_y, model):
        super().__init__(PRINCESS_IMG, 52, 60, position_x * TILESIZE, position_y * TILESIZE, model)
        self.last_attack = 0

    def update(self):
        self.acc = vec(0, PLAYER_GRAV)
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

    def attack(self, x, y):
        now = pygame.time.get_ticks()
        if now - self.last_attack > ATTACK_RATE:
            self.last_attack = now
            dir = self.pos + vec(x,y)
            Attack(dir, self.model)

# TODO - Criar classe Enemy
class Orc(Character):
    def __init__(self, position_x, position_y, model):
        super().__init__(ORC_IMG, 52, 32, position_x * TILESIZE, position_y * TILESIZE, model)
        self.image.fill(RED)
        self.direction = 1

        self.model.enemies.add(self)

    def update(self):
        self.acc = vec(ENEMY_ACC * self.direction, ENEMY_GRAV).rotate(self.direction)
        self.acc.x += self.vel.x * ENEMY_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        self.wall_collisions()

    def wall_collisions(self):
        self.rect.centerx = self.pos.x
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False):
            if self.vel.x > 0:
                self.vel.x = 0
                self.direction = - self.direction
                self.rect.right = wall.rect.left
            elif self.vel.x < 0:
                self.vel.x = 0
                self.direction = - self.direction
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


class Tile(ABC,pygame.sprite.Sprite):
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
    def __init__(self, position_x, position_y, model):
        super().__init__(UNBREAKABLE_IMG, position_x, position_y, model)
        self.image.fill(BLUE)


class Breakable(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(BREAKABLE_IMG, position_x, position_y, model)
        self.image.fill(GREEN)
        # Adiciona o bloco como se fosse um inimigo para poder ser destrutivel
        self.model.enemies.add(self)


class Attack(pygame.sprite.Sprite):
    def __init__(self, pos, model):
        super().__init__()
        self.__image = pygame.Surface((TILESIZE/1.5, TILESIZE/1.5))
        self.__rect = self.__image.get_rect()
        self.__pos = pos
        self.__rect.center = self.__pos
        self.__spawn_time = pygame.time.get_ticks()
        self.__model = model

        self.__model.all_sprites.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    def update(self):
        # Checa se o ataque acertou algum inimigo
        pygame.sprite.spritecollide(self, self.__model.enemies, True)
        # Destroi o attaque apos certo tempo
        if pygame.time.get_ticks() - self.__spawn_time > ATTACK_LIFETIME:
            self.kill()