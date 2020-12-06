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
SILVER =(192,192,192)


# Frames per second. Velocidade em que a tela atualiza.
FPS = 30


# Titulo da janela do jogo.
TITLE = 'Jogo'


# Tamanho da janela do jogo. Largura e altura.
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 768


# Arquivos de imagem
PRINCESS_FOLDER = path.join(IMG_FOLDER, 'princess\\')
ORC_IMG = 'enemy_1.png'
UNBREAKABLE_IMG = 'unbreakable_tile.png'
BREAKABLE_IMG = 'breakable_tile.png'
BG_COLOR = WHITE
BG_IMAGE = 'background.png'

# Variaveis que compoem a fisica da princesa
PLAYER_ACC = 2
PLAYER_FRICTION = -0.15
PLAYER_GRAV = 0.8

ENEMY_ACC = 1
ENEMY_FRICTION = -0.15
ENEMY_GRAV= 0.8

ATTACK_LIFETIME = 300
ATTACK_RATE = 300
ATTACK_RANGE = 64

#Tamanho dos blocos
TILESIZE = 64
GRIDWIDTH = SCREEN_HEIGHT / TILESIZE
GRIDHEIGHT = SCREEN_HEIGHT / TILESIZE
