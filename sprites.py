from abc import ABC, abstractmethod
from os import path, listdir

import pygame
from pygame.locals import *
from settings import *

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
            for file in listdir(path.join(IMG_FOLDER, f'{self.__character_folder}\\{frame_type}')):
                self.frames[frame_type].append(f'{frame_type}\\{file}')

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

class Princess(Character):
    def __init__(self, position_x, position_y, model):
        super().__init__(PRINCESS_FOLDER, 64, 90, position_x * TILESIZE, position_y * TILESIZE, model, PRINCESS_LAYER)
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


# TODO - Criar classe Enemy
class Orc(Character):
    def __init__(self, position_x, position_y, model):
        super().__init__(ORC_FOLDER, 64, 102, position_x * TILESIZE, position_y * TILESIZE, model, ENEMY_LAYER)
        self.direction = 1

        self.model.enemies.add(self)

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
        
    def load_images(self):
        for frame_type in self.frames:
            for file in listdir(path.join(IMG_FOLDER, f'{ORC_FOLDER}\\{frame_type}')):
                self.frames[frame_type].append(f'{frame_type}\\{file}')

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
            #Animação de cair
            self.pick_frame('falling', 15)

        if self.running:
            #Animação de corrida
            self.pick_frame('running', 30)

        if not self.running and not self.falling:
            # Animação de ficar parado
            self.pick_frame('idle', 30)

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

class Tile(ABC, pygame.sprite.Sprite):
    def __init__(self, image_link, position_x, position_y, model):
        super().__init__()
        self._layer = TILE_LAYER
        self.__image = pygame.image.load(path.join(IMG_FOLDER, image_link)).convert_alpha()
        self.__image = pygame.transform.scale(self.__image, (TILESIZE, TILESIZE))
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


class Breakable(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(BREAKABLE_IMG, position_x, position_y, model)
        # Adiciona o bloco como se fosse um inimigo para poder ser destrutivel
        self.model.destructive_tiles.add(self)

class Coin(Tile):
    def __init__(self, position_x, position_y, model):
        super().__init__(COIN_TILE_IMG, position_x, position_y, model)
        #Igual o breakable porém um dia, se tudo der certo, vai aumentar os pontos
        self.model.coin_tiles.add(self)

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
            self.__model.controller.score += 10
        # Checa se o ataque acertou um bloco destrutivel
        pygame.sprite.spritecollide(self, self.__model.destructive_tiles, True)
        #se o destrutivel for do tipo coin, aumenta score
        broken_coin_tiles = pygame.sprite.spritecollide(self, self.__model.coin_tiles, True)
        for broke in broken_coin_tiles:
            self.__model.controller.score += 5
        # Destroi o attaque apos certo tempo
        if pygame.time.get_ticks() - self.__spawn_time > ATTACK_LIFETIME:
            self.kill()
            self.__model.princess.attacking = False
