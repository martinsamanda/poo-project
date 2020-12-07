from os import path

# Arquivo para guardar variaveis constantes
GAME_FOLDER = path.dirname(__file__)
IMG_FOLDER = path.join(GAME_FOLDER, 'images')

# Cores RGB
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SILVER = (192,192,192)
STRONG_RED = (194,59,34)
SOFT_BLUE = (135, 206, 250)
BRIGHT_BLUE = (44,62,80)
DARK_BLUE = (52,152,219)


# Frames per second. Velocidade em que a tela atualiza.
FPS = 30

# Titulo da janela do jogo.
TITLE = 'A TORRE'

# Fonte Usada
FONT_NAME = 'Raleway Bold'

# Tamanho da janela do jogo. Largura e altura.
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 768


# Arquivos de imagem
PRINCESS_FOLDER = path.join(IMG_FOLDER, 'princess\\')
ORC_FOLDER = path.join(IMG_FOLDER, 'orc\\')
GOLEM_FOLDER = path.join(IMG_FOLDER, 'golem\\')
GOLEM_IMG = 'enemy_2.png'
UNBREAKABLE_IMG = 'unbreakable_tile.png'
BREAKABLE_IMG = 'breakable_tile.png'
BG_IMAGE = 'background.png'
BG_START_SCREEN = 'start_screen.png'
BG_GAME_OVER = 'game_over_screen.png'
COIN_TILE_IMG = 'coin_tile.png'

# Ordem da layer de cada sprite
PRINCESS_LAYER = 3
ENEMY_LAYER = 2
TILE_LAYER = 1

# Variaveis que compoem a fisica da princesa
PLAYER_ACC = 2
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.8

ENEMY_ACC = 1
ENEMY_FRICTION = -0.15
ENEMY_GRAV= 0.8

ATTACK_LIFETIME = 300
ATTACK_RATE = 400
ATTACK_RANGE = 52

#Tamanho dos blocos
TILESIZE = 64
GRIDWIDTH = SCREEN_HEIGHT / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE
