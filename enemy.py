from character import Character
from os import path, listdir
import pygame
from pygame.locals import *
from settings import *
vec = pygame.math.Vector2

class Enemy(Character):
    def __init__(self, character_folder, width, height, position_x, position_y, model, layer):
        super().__init__(character_folder, width, height, position_x, position_y, model, layer)
        pass

    def update(self):
        self.animate()

        self.acc = vec(ENEMY_ACC * self.direction, ENEMY_GRAV).rotate(self.direction)
        self.acc.x += self.vel.x * ENEMY_FRICTION
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.rect.midbottom = self.pos

        self.wall_collisions()
        self.mask = pygame.mask.from_surface(self.image)

    def wall_collisions(self):
        self.rect.centerx = self.pos.x
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False):
            if wall.rect.y < self.rect.y:
                continue
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

    def animate(self):
        if int(self.vel.y) != 0:
            self.falling = True
        else:
            self.falling = False

        if int(self.vel.x) != 0:
            self.running = True
        else:
            self.running = False

        if self.falling:
            # Animação de cair
            self.pick_frame('falling', 15)

        if self.running:
            # Animação de corrida
            self.pick_frame('running', 30)

        if not self.running and not self.falling:
            # Animação de ficar parado
            self.pick_frame('idle', 30)
