from abc import ABC, abstractmethod
from os import path, listdir

import pygame
from pygame.locals import *
from settings import *
from sounds import Sound

# Alias
vec = pygame.math.Vector2


class Character(ABC, pygame.sprite.Sprite):
    def __init__(self, character_folder, width, height, position_x, position_y, model, layer):
        super().__init__()
        # Frames, imagems e hitbox
        self._layer = layer
        self.frames = {'idle': [],
                       'running': [],
                       'falling': [],
                       }
        self.__character_folder = character_folder
        self.load_images()
        self.__image = pygame.image.load(path.join(self.__character_folder, self.frames['idle'][0])).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (width, height))
        self.__rect = self.__image.get_rect()
        self.mask = pygame.mask.from_surface(self.__image)
        self.running = False
        self.falling = False
        self.current_frame = 0
        self.last_update = 0

        # Movimentação
        self.pos = vec(position_x, position_y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        # Model
        self.model = model
        self.model.characters.add(self)
        self.model.all_sprites.add(self)

    @property
    def rect(self):
        return self.__rect

    @property
    def image(self):
        return self.__image

    def set_image(self, filepath, flip_img=False):
        old_size = self.image.get_size()
        self.__image = pygame.image.load(path.join(self.__character_folder, filepath)).convert_alpha()
        new_size = self.image.get_size()
        self.__image = pygame.transform.scale(self.__image, (new_size[0] * old_size[1] // new_size[1], old_size[1]))
        if flip_img:
            self.__image = pygame.transform.flip(self.__image, True, False)
        self.__rect = self.__image.get_rect()

    def load_images(self):
        for frame_type in self.frames:
            for file in listdir(path.join(IMG_FOLDER, f'{self.__character_folder}/{frame_type}')):
                self.frames[frame_type].append(f'{frame_type}/{file}')

    def pick_frame(self, frame_type, frame_per_sec):
        now = pygame.time.get_ticks()
        if self.vel.x > 0:
            flip = False
        else:
            flip = True
        if now - self.last_update > frame_per_sec:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.frames[frame_type])
            self.set_image(self.frames[frame_type][self.current_frame], flip)

    @abstractmethod
    def update(self):
        # Movimento que o personagem faz
        self.wall_collisions()

    @abstractmethod
    def wall_collisions(self):
        # Movimento que o persoangem faz ao acertar a parede
        pass

    @abstractmethod
    def animate(self):
        # Animação do personagem
        self.pick_frame()

    @staticmethod
    def collided(sprite, other):
        return sprite.hitbox.colliderect(other.rect)
