import menu
from menu import *
from walking import *
from battle1 import *


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing, self.walking, self.battle1,self.cutscenes,self.menu_run = True, False, False, False,False,True
        self.up, self.down, self.enter = False, False, False
        self.width, self.height = 900, 600
        self.display = pygame.Surface((self.width, self.height))
        self.screen = pygame.display.set_mode(((self.width, self.height)))  # in the whole game keep screen this one
        self.font_name = pygame.font.get_default_font()
        self.main_menu = MainMenu(self)
        self.credits = CreditsMenu(self)
        self.curr_screen = self.main_menu
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.time=1500
        self.text_colour=self.WHITE

    def game_loop(self):
        """
        check which part should run now
        first menu
        then walking
        then battle1 first
             walking
             battle1 second
             walking
             battle1 third
             walking
        """
        while self.menu_run:
            self.curr_screen.display_menu()
        while self.cutscenes:

            self.screen.fill(self.BLACK)
            self.draw_text('One day...', 80, self.width / 2, self.height / 2 - 100, "white")
            self.draw_text('Our hero weak up in a strange place', 30, self.width / 2, self.height / 2 + 10, "white")
            pygame.display.update()
            self.reset()
            self.time -= 1
            if self.time <= 0:
                self.cutscenes = False


        n=0
        while True:
            walking(self.screen)
            battlegame()



        # while self.walking:
        #     self.battle1 = walking(self.screen)
        #     if self.battle1 == True:
        #         break
        #
        # while self.battle1:
        #     battlegame(900, 600, 450, 300, "art/player.png", "art/background.png", "52309112",
        #                [1, 5, 1, 3, 3, 1, 1, "art/ghost.png"], [1, 5, 1, 3, 2, "art/heart.png"],
        #                [1, 5, 1, 3, 2, "art/debuff32x32.png"], ["art/attack.png", 2, 2, 0, 0, 32],
        #                ["art/attack.png", 2, 2, 0, 0, 32], ["art/attack.png", 2, 2, 0, 0, 32])

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_screen.run_display = False
                pygame.quit()
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.up = True
                if event.key == pygame.K_DOWN:
                    self.down = True
                if event.key == pygame.K_RETURN:
                    self.enter = True

    def reset(self):# each time set up down enter back to false
        self.up, self.down, self.enter = False, False, False

    def draw_text(self, text, size, x, y,colour):
        if colour=="white":
            self.text_colour=self.WHITE
        if colour=="black":
            self.text_colour=self.BLACK

        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.text_colour)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)
