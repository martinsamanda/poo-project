from os import path, listdir

import pygame
from pygame.locals import *
from settings import *
vec = pygame.math.Vector2

class Explosion:
    def __init__(self):
        pass

'''explosion_animation = {}
explosion_animation['lg'] = []
explosion_animation['sm'] = []
for i in range(9):
  filename = 'regularExplosion0{}.png'.format(i)
  img = pygame.image.load(path.join('explosions', filename))
  # img.set_colorkey('black')
  img_lg = pygame.transform.scale(img, (256, 256))
  explosion_animation['lg'].append(img_lg)
  img_sm = pygame.transform.scale(img, (128, 128))
  explosion_animation['sm'].append(img_sm)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_animation[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50 

    def update(self):
      now = pygame.time.get_ticks()
      if now - self.last_update > self.frame_rate:
        self.last_update = now
        self.frame += 1
        if self.frame == len(explosion_animation[self.size]):
          self.kill()
        else:
          center = self.rect.center
          self.image = explosion_animation[self.size][self.frame]
          self.rect = self.image.get_rect()
          self.rect.center = center'''
    