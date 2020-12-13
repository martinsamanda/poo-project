import pygame
from enemy import Enemy
from character import Character
from os import path, listdir
from pygame.locals import *
from settings import *
from attack import Attack
vec = pygame.math.Vector2


class Orc(Enemy):
    def __init__(self, position_x, position_y, model):
        Character.__init__(self, ORC_FOLDER, 30, 90, position_x * TILESIZE, position_y * TILESIZE, model, ENEMY_LAYER)
        self.direction = 1
        self.model.enemies.add(self)
