"""
Created on Fri Dec 10

@author: wenjieLiu
"""

import pygame


class Menu():
    def __init__(self, game):
        self.game = game  # game class
        self.half_w, self.half_h = self.game.width / 2, self.game.height / 2
        self.menu_run = True
        self.arrow_position = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def playmusic(self):
        pygame.mixer.music.load('image/menu.mp3')
        pygame.mixer.music.play()

    def draw_arrow(self):
        arrow = pygame.image.load('image/arrow.png').convert_alpha()
        arrow = pygame.transform.scale(arrow, (30, 30))
        self.game.screen.blit(arrow, self.arrow_position)


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.half_w, self.half_h + 30
        self.creditsx, self.creditsy = self.half_w, self.half_h + 70
        self.arrow_position = (self.startx - 115, self.starty - 17)

    def display_menu(self):
        self.playmusic()
        self.menu_run = True
        while self.menu_run:
            self.game.check_events()
            self.check_input()
            menubackground = pygame.image.load('image/menu.JPG').convert_alpha()
            self.game.screen.blit(menubackground, (0, 0))
            self.game.draw_text("Main Menu", 80, self.game.width / 2, self.game.height / 3 - 20,"black")
            self.game.draw_text("Start Game", 30, self.startx, self.starty,"black")
            self.game.draw_text("Credits", 30, self.creditsx, self.creditsy,"black")
            self.draw_arrow()
            pygame.display.update()
            self.game.reset()

    def move_arrow(self):
        if self.game.down:
            if self.state == 'Start':
                self.arrow_position = (self.creditsx - 85, self.creditsy - 17)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.arrow_position = (self.startx - 115, self.starty - 17)
                self.state = 'Start'
        elif self.game.up:
            if self.state == 'Start':
                self.arrow_position = (self.creditsx - 85, self.creditsy - 17)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.arrow_position = (self.startx - 115, self.starty - 17)
                self.state = 'Start'

    def check_input(self):
        self.move_arrow()
        if self.game.enter:
            if self.state == 'Start':
                self.game.menu_run=False
                self.game.cutscenes=True
            elif self.state == 'Credits':
                self.game.curr_screen = self.game.credits
            self.menu_run = False


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.playmusic()
        self.menu_run = True
        while self.menu_run:
            self.game.check_events()
            if self.game.enter:
                self.game.curr_screen = self.game.main_menu
                self.menu_run = False
            self.game.screen.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.game.width / 2, self.game.height / 2 - 20,"white")
            self.game.draw_text('Made by us', 15, self.game.width / 2, self.game.height / 2 + 10,"white")
            pygame.display.update()
            self.game.reset()
