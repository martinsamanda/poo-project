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
        pygame.display.set_caption(f"{TITLE}") #Trocar por titulo
        self.__FPS.tick(FPS)
        self.draw_background(BRIGHT_BLUE, DARK_BLUE) # TODO - Remover caso for adicionar um background

    def draw_start_screen(self):
        self.draw_screen()
        self.__screen.fill(SOFT_BLUE)
        self.draw_text(48, TITLE, WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT /4)
        self.draw_text(22, 'Use as setas para se movimentar', WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
        self.draw_text(22, 'Pressione qualquer tecla para começar', WHITE, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 /4)
        pygame.display.flip()

    def draw_game(self):
        self.draw_screen()
        self.__GameModel.all_sprites.draw(self.__screen)
        #Adiciona informações extras a tela como um grid e o hitbox dos sprites
        self.draw_dev_tools()
        #Mostra o score
        self.draw_text(22, f'{self.__GameController.score}', WHITE, SCREEN_WIDTH / 2, 15)
        pygame.display.flip()

    def draw_game_over(self):
        self.draw_screen()
        self.__screen.fill(STRONG_RED)
        self.draw_text(48, 'GAME OVER', BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
        self.draw_text(22, f'SCORE: {self.__GameController.score}', BLACK,  SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
        self.draw_text(22, 'Pressione qualquer tecla para jogar novamente', BLACK, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
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
        for sprite in self.__GameModel.characters:
            pygame.draw.rect(self.__screen, RED, sprite.rect, 1)
        pygame.draw.rect(self.__screen, BLUE, self.__GameModel.princess.hitbox, 1)

    def draw_text(self, size, text, color, x, y):
        font = pygame.font.Font(self.__font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.__screen.blit(text_surface, text_rect)

    def draw_background(self, color, gradient, vertical=True, forward=True):
        rect = self.__screen.get_rect()
        x1, x2 = rect.left, rect.right
        y1, y2 = rect.top, rect.bottom
        if vertical:
            h = y2 - y1
        else:
            h = x2 - x1
        if forward:
            a, b = color, gradient
        else:
            b, a = color, gradient
        rate = (
            float(b[0] - a[0]) / h,
            float(b[1] - a[1]) / h,
            float(b[2] - a[2]) / h
        )
        fn_line = pygame.draw.line
        if vertical:
            for line in range(y1, y2):
                color = (
                    min(max(a[0] + (rate[0] * (line - y1)), 0), 255),
                    min(max(a[1] + (rate[1] * (line - y1)), 0), 255),
                    min(max(a[2] + (rate[2] * (line - y1)), 0), 255)
                )
                fn_line(self.__screen, color, (x1, line), (x2, line))
        else:
            for col in range(x1, x2):
                color = (
                    min(max(a[0] + (rate[0] * (col - x1)), 0), 255),
                    min(max(a[1] + (rate[1] * (col - x1)), 0), 255),
                    min(max(a[2] + (rate[2] * (col - x1)), 0), 255)
                )
                fn_line(self.__screen, color, (col, y1), (col, y2))