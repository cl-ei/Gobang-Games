# -*- coding: utf-8 -*-

"""
python version: v3.5.1:37a07cee5969
pygame version:1.9.2a0
env: windows  10.0.10586 x64

author: caoliang  E-mail : i#caoliang.net
http://www.caoliang.net
"""

import sys

import pygame
from pygame.locals import QUIT

from source import *
from newcore import GameManager, Role


class Game(object):
    def __init__(self, window_size, caption, icon=None, fps=30):
        pygame.init()

        if caption is not None:
            pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

        self.fps = fps
        self.source = pygame.image.load("./source/ui").convert_alpha()

        self.home_img = pygame.transform.scale(
            self.source.subsurface(CLIP_HOME_PAGE),
            self.window_size
        )
        self.about_img = None

        default_font = "./source/ncsj.ttf"

        self.font = pygame.font.Font(default_font, 18)
        self.white_thinking_txt = self.font.render("思考中…", True, WHITE)
        self.black_thinking_txt = self.font.render("思考中…", True, BLACK)

        self.table_txt_max = pygame.font.Font(default_font, 24)
        self.table_txt_mid = pygame.font.Font(default_font, 22)
        self.table_txt_min = pygame.font.Font(default_font, 20)

        self.grid_img = pygame.transform.scale(
            self.source.subsurface(CLIP_GRID_PAGE),
            self.window_size
        )
        self.think_img = pygame.transform.scale(
            self.source.subsurface(CLIP_THINK),
            self.window_size
        )
        self.w_img = pygame.image.load("img/round_white.png").convert_alpha()  # (24, 24))
        self.b_img = pygame.image.load("img/round_black.png").convert_alpha()  # (24, 24))

        self.__sources = []

    def create_button(self, style, callback):
        button = Button(style, callback=callback)
        self.__sources.append(button)

    def update_display(self):
        for widget_ in self.__sources:
            widget_.update(self.screen)

        pygame.display.update()
        self.clock.tick(30)

    def release_dynamic_created_widget(self):
        self.__sources = []

    def wait_start(self):
        self.release_dynamic_created_widget()

        start_btn = {
            "style": {
                "width": 120,
                "heigth": 50,
                "left": self.window_size[0] * 0.5 - 140,
                "top": self.window_size[1] * 0.75,
                "default_img": self.source.subsurface(CLIP_BTN_START[0]),
                "hovered_img": self.source.subsurface(CLIP_BTN_START[1]),
                "pushed_img": self.source.subsurface(CLIP_BTN_START[2]),
            },
            "callback": self.gaming
        }
        about_btn = {
            "style": {
                "width": 120,
                "heigth": 50,
                "left": self.window_size[0] * 0.5 + 20,
                "top": self.window_size[1] * 0.75,
                "default_img": self.source.subsurface(CLIP_BTN_ABOUT[0]),
                "hovered_img": self.source.subsurface(CLIP_BTN_ABOUT[1]),
                "pushed_img": self.source.subsurface(CLIP_BTN_ABOUT[2]),
            },
            "callback": self.about
        }
        self.create_button(**start_btn)
        self.create_button(**about_btn)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

            self.screen.blit(self.home_img, (0, 0))
            self.update_display()

    def parse_gaming_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            else:
                pass
        input_data = self.get_table_input()
        return input_data

    def get_table_input(self):
        return 0, 0

    def draw_table(self, table):
        pass

    def gaming(self):
        self.release_dynamic_created_widget()

        dynamic_create_btns = [
            {
                "style": {
                    "width": 120,
                    "heigth": 50,
                    "left": self.window_size[0] * 0.5 - 140,
                    "top": self.window_size[1] * 0.75,
                    "default_img": self.source.subsurface(CLIP_BTN_START[0]),
                    "hovered_img": self.source.subsurface(CLIP_BTN_START[1]),
                    "pushed_img": self.source.subsurface(CLIP_BTN_START[2]),
                },
                "callback": self.gaming
            },
            {
                "style": {
                    "width": 120,
                    "heigth": 50,
                    "left": self.window_size[0] * 0.5 + 20,
                    "top": self.window_size[1] * 0.75,
                    "default_img": self.source.subsurface(CLIP_BTN_ABOUT[0]),
                    "hovered_img": self.source.subsurface(CLIP_BTN_ABOUT[1]),
                    "pushed_img": self.source.subsurface(CLIP_BTN_ABOUT[2]),
                },
                "callback": self.about
            },
            {
                "style": {
                    "width": 120,
                    "heigth": 50,
                    "left": self.window_size[0] * 0.5 + 20,
                    "top": self.window_size[1] * 0.75,
                    "default_img": self.source.subsurface(CLIP_BTN_ABOUT[0]),
                    "hovered_img": self.source.subsurface(CLIP_BTN_ABOUT[1]),
                    "pushed_img": self.source.subsurface(CLIP_BTN_ABOUT[2]),
                },
                "callback": self.about
            }
        ]
        for btn_args in dynamic_create_btns:
            self.create_button(**btn_args)

        # computer_pgsbar = sc.ProgressBar("img/round_white.png", (12, 12), (675, 50), 40)
        # player_pgsbar = sc.ProgressBar("img/round_black.png", (12, 12), (720, 440), 40)

        gobang_mgr = GameManager()
        while True:
            events = self.parse_gaming_event()
            # distribute events
            # for e in events:
            #   react = gobang_mgr.do(e)
            #   self.response_game_mgr_event(e)

            self.screen.blit(self.grid_img, (0, 0))
            self.draw_table(table=gobang_mgr.table)
            self.update_display()

    def about(self):
        self.release_dynamic_created_widget()
        if self.about_img is None:
            self.about_img = pygame.transform.scale(
                self.source.subsurface(CLIP_ABOUT_PAGE),
                self.window_size
            )

        back_btn = {
            "style": {
                "width": 120,
                "heigth": 50,
                "left": self.window_size[0] * 0.5 - 60,
                "top": self.window_size[1] * 0.85,
                "default_img": self.source.subsurface(CLIP_BTN_BACK[0]),
                "hovered_img": self.source.subsurface(CLIP_BTN_BACK[1]),
                "pushed_img": self.source.subsurface(CLIP_BTN_BACK[2]),
            },
            "callback": self.wait_start
        }
        self.create_button(**back_btn)

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()

            self.screen.blit(self.about_img, (0, 0))
            self.update_display()


def main():
    game = Game(window_size=(800, 600), caption="CL的五子棋")
    while True:
        game.wait_start()
        game.gaming()


if __name__ == "__main__":
    main()
