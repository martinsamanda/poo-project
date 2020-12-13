from character import Character
from os import path, listdir

import pygame
from pygame import mixer
from pygame.locals import *
from settings import *
from attack import Attack

vec = pygame.math.Vector2


class Princess(Character):
    def __init__(self, position_x, position_y, model):
        super().__init__(PRINCESS_FOLDER, 40, 85, position_x * TILESIZE, position_y * TILESIZE, model, PRINCESS_LAYER)
        self.frames['attacking'] = []
        self.load_images()
        self.last_attack = 0
        self.attacking = False
        self.hitbox = self.rect.copy()

    def update(self):
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        pressed_key = pygame.key.get_pressed()

        if pressed_key[K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if pressed_key[K_LEFT]:
            self.acc.x = -PLAYER_ACC

        #Aplica fricção
        self.acc.x += self.vel.x * PLAYER_FRICTION
        #Equações de velocidade e deslocamento
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        self.hitbox.midbottom = self.pos

        self.wall_collisions()
        self.mask = pygame.mask.from_surface(self.image)

    def wall_collisions(self):
        self.rect.centerx = self.pos.x
        self.hitbox.centerx = self.pos.x
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False, self.collided):
            if wall.rect.y < self.hitbox.y:
                continue
            if self.vel.x > 0:
                self.vel.x = 0.001
                self.hitbox.right = wall.rect.left
            elif self.vel.x < 0:
                self.vel.x = 0
                self.hitbox.left = wall.rect.right
            self.pos.x = self.hitbox.centerx

        self.rect.centery = self.pos.y
        self.hitbox.centery = self.pos.y
        for wall in pygame.sprite.spritecollide(self, self.model.tiles, False, self.collided):
            if self.vel.y > 0:
                self.vel.y = 0
                self.hitbox.bottom = wall.rect.top
            elif self.vel.y < 0:
                self.vel.y = 0
                self.hitbox.top = wall.rect.bottom
            self.pos.y = self.hitbox.centery

    def animate(self):
        if int(self.vel.y) != 0:
            self.falling = True
        else:
            self.falling = False

        if int(self.vel.x) != 0:
            self.running = True
        else:
            self.running = False

        if self.attacking:
            self.pick_frame('attacking', 30)

        if self.falling:
            #Animação de cair
            self.pick_frame('falling', 15)

        if self.running:
            #Animação de corrida
            self.pick_frame('running', 30)

        if not self.running and not self.falling:
            # Animação de ficar parado
            self.pick_frame('idle', 30)

    def attack(self, x, y):
        now = pygame.time.get_ticks()
        if now - self.last_attack > ATTACK_RATE:
            self.last_attack = now
            self.attacking = True
            dir = self.pos + vec(x, y)
            Attack(dir, self.model)
