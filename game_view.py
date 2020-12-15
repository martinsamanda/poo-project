import pygame
from settings import *


class GameView:
    def __init__(self, controller, model):
        self.__GameController = controller
        self.__GameModel = model
        self.__screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__FPS = pygame.time.Clock()
        self.__font_name = pygame.font.match_font(FONT_NAME)

    def draw_screen(self):
        pygame.display.set_caption(f"{TITLE}")
        self.__FPS.tick(FPS)
        #Fill background com imagem estatica
        background = pygame.image.load(path.join(IMG_FOLDER, BG_IMAGE)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__screen.blit(background, (0,0))

    def draw_start_screen(self):
        self.draw_screen()

        background = pygame.image.load(path.join(IMG_FOLDER, BG_START_SCREEN)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__screen.blit(background, (0,0))

        self.draw_text(24, 'Use as setas para se movimentar', BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT /50)
        self.draw_text(24, 'Pressione qualquer', BLACK, SCREEN_WIDTH * 4.6/6, SCREEN_HEIGHT * 3.2/8 )
        self.draw_text(24, ' tecla para começar', BLACK, SCREEN_WIDTH * 4.6/6, SCREEN_HEIGHT * 3.4/8 )
        self.draw_text(24, f'HIGH SCORE: {self.__GameModel.highscore.data}', BLACK, SCREEN_WIDTH /2, SCREEN_HEIGHT - 40)
        pygame.display.flip()

    def draw_win_screen(self, new_higshcore=False):
        self.draw_screen()

        background = pygame.image.load(path.join(IMG_FOLDER, BG_WIN_SCREEN)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__screen.blit(background, (0,0))

        self.draw_text(72, 'WIN', BLACK, SCREEN_WIDTH / 1.3, SCREEN_HEIGHT / 8)
        self.draw_text(28, f'SCORE: {self.__GameModel.score}', BLACK,  SCREEN_WIDTH / 1.3, SCREEN_HEIGHT /5)
        self.draw_text(24, 'Pressione qualquer', BLACK, SCREEN_WIDTH * 4.6/6, SCREEN_HEIGHT * 3.3/13 )
        self.draw_text(24, ' tecla para começar', BLACK, SCREEN_WIDTH * 4.6/6, SCREEN_HEIGHT * 3.6/13 )
        if new_higshcore:
            self.draw_text(24, f'NOVO HIGH SCORE !', BLACK,  SCREEN_WIDTH / 1.3, (SCREEN_HEIGHT /5) + 20)
        else:
            self.draw_text(28, f'HIGH SCORE: {self.__GameModel.highscore.data}', BLACK, SCREEN_WIDTH / 1.3, (SCREEN_HEIGHT /5) + 20)

        pygame.display.flip()

    def draw_game(self):
        self.draw_screen()
        self.__GameModel.all_sprites.draw(self.__screen)
        #Adiciona informações extras a tela como um grid e o hitbox dos sprites
        self.draw_dev_tools()
        #Mostra o score
        self.draw_text(22, f'Score: {self.__GameModel.score}', DARK_BLUE, SCREEN_WIDTH / 2, 15)
        pygame.display.flip()

    def draw_game_over(self, new_higshcore=False):
        self.draw_screen()
        self.__screen.fill(STRONG_RED)

        background = pygame.image.load(path.join(IMG_FOLDER, BG_GAME_OVER)).convert_alpha()
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.__screen.blit(background, (0,0))

        self.draw_text(72, 'GAME OVER', BLACK, SCREEN_WIDTH / 3, SCREEN_HEIGHT / 8)
        self.draw_text(28, f'SCORE: {self.__GameModel.score}', BLACK,  SCREEN_WIDTH / 3, SCREEN_HEIGHT /5)
        self.draw_text(22, 'Pressione qualquer tecla para jogar novamente', BLACK, SCREEN_WIDTH / 2.75, SCREEN_HEIGHT * 19/21)
        if new_higshcore:
            self.draw_text(24, f'NOVO HIGH SCORE !', BLACK,  SCREEN_WIDTH / 3, (SCREEN_HEIGHT /5) + 20)
        else:
            self.draw_text(28, f'HIGH SCORE: {self.__GameModel.highscore.data}', BLACK, SCREEN_WIDTH / 3, (SCREEN_HEIGHT /5) + 25)
        pygame.display.flip()

    def draw_dev_tools(self):
        #Mostra o FPS
        self.draw_text(15, f"FPS: {int(self.__FPS.get_fps())}", GREEN, 30, 15)

        #Mostra um grid com todos os tiles
        #for x in range(0, SCREEN_WIDTH, TILESIZE):
        #    pygame.draw.line(self.__screen, SILVER, (x, 0), (x, SCREEN_HEIGHT))
        #for y in range(0, SCREEN_HEIGHT, TILESIZE):
        #    pygame.draw.line(self.__screen, SILVER, (0, y), (SCREEN_WIDTH, y))

        #Mostra a hitbox dos personagems
        '''for sprite in self.__GameModel.all_sprites:
            pygame.draw.rect(self.__screen, RED, sprite.rect, 1)
        pygame.draw.rect(self.__screen, BLUE, self.__GameModel.princess.hitbox, 1)'''

    def draw_text(self, size, text, color, x, y):
        font = pygame.font.Font(self.__font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.__screen.blit(text_surface, text_rect)
