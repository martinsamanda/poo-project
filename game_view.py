import pygame

from settings import *


class GameView:
    def __init__(self, controller, model):
        self.__GameController = controller
        self.__GameModel = model
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__FPS = pygame.time.Clock()
        self.__font = pygame.font.SysFont("Verdana", 60)

    def draw(self):
        pygame.display.set_caption(f"{int(self.__FPS.get_fps())}") #Trocar por titulo
        self.__FPS.tick(FPS)

        #Fill todo branco no fundo
        self.__screen.fill(BG_COLOR)
        #Fill background com imagem estatica
        background = pygame.image.load(path.join(IMG_FOLDER, BG_IMAGE)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__screen.blit(background, [0,0])

        self.draw_grid()
        self.__GameModel.all_sprites.draw(self.__screen)
        for sprite in self.__GameModel.all_sprites:
            pygame.draw.rect(self.__screen, RED, sprite.rect, 1)
        pygame.display.flip()

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILESIZE):
            pygame.draw.line(self.__screen, SILVER, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, TILESIZE):
            pygame.draw.line(self.__screen, SILVER, (0, y), (SCREEN_WIDTH, y))

    def end(self):
        game_over = self.__font.render('GAME OVER', True, BLACK)
        game_over_rect = game_over.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.__screen.fill(RED)
        self.__screen.blit(game_over, game_over_rect)
        pygame.display.flip()

