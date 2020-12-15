import pygame
from enemy import Enemy
from os import path, listdir
from pygame.locals import *
from settings import *
vec = pygame.math.Vector2


class Golem(Enemy):
    def __init__(self, position_x, position_y, model):
        super().__init__(GOLEM_FOLDER, 30, 85, position_x * TILESIZE, position_y * TILESIZE, model, ENEMY_LAYER)
        self.direction = 1
        self.model.enemies.add(self)
