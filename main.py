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

from view import Button

# --------------------------------- Global var -------------------------------------- #
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)

# source file clip
CLIP_HOME_PAGE = (0, 0, 1024, 768)
CLIP_ABOUT_PAGE = (1024, 0, 1024, 768)
CLIP_GRID_PAGE = (2048, 0, 800, 600)
CLIP_THINK = (600, 767, 118, 80)
CLIP_ONE_MORE_TIME = (718, 767, 374, 203)
CLIP_VICTORY = (718 + 374, 767, 160, 38)
CLIP_DEFEAT = (718 + 374 + 160, 767, 446, 77)
CLIP_BTN_ABOUT = (
    (0, 767, 120, 60),
    (0, 767 + 60, 120, 60),
    (0, 767 + 120, 120, 60),
)
CLIP_BTN_BACK = (
    (120, 767, 120, 60),
    (120, 767 + 60, 120, 60),
    (120, 767 + 120, 120, 60),
)
CLIP_BTN_GOAHEAD = (
    (240, 767, 120, 60),
    (240, 767 + 60, 120, 60),
    (240, 767 + 120, 120, 60),
)
CLIP_BTN_GOBACK = (
    (360, 767, 120, 60),
    (360, 767 + 60, 120, 60),
    (360, 767 + 120, 120, 60),
)
CLIP_BTN_START = (
    (480, 767, 120, 60),
    (480, 767 + 60, 120, 60),
    (480, 767 + 120, 120, 60),
)


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

        self.__sources = []
        # for i in range(10):
        #     gv.g_num_tab += [max_txt.render(str(i), True, (180, 180, 180))]
        # for i in range(10, 100):
        #     gv.g_num_tab += [mid_txt.render(str(i), True, (180, 180, 180))]
        # for i in range(100, 256):
        #     gv.g_num_tab += [min_txt.render(str(i), True, (180, 180, 180))]

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

    def gaming(self):
        grid_img = sc.loadimg("img/grid.png", gv.g_size_win)
        w_img = sc.loadimg("img/round_white.png", (24, 24))
        b_img = sc.loadimg("img/round_black.png", (24, 24))
        think_img = sc.loadimg("img/think.png", (120, 60))

        back_btn = sc.Button(gv.g_btn_gameback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_gameback)
        goback_btn = sc.Button(gv.g_btn_goback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goback)
        goahead_btn = sc.Button(gv.g_btn_goahead_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goahead)

        computer_pgsbar = sc.ProgressBar("img/round_white.png", (12, 12), (675, 50), 40)
        player_pgsbar = sc.ProgressBar("img/round_black.png", (12, 12), (720, 440), 40)

        gobang_mgr = GameManager()
        input_info = sc.GetInput()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit()

            gv.g_screen.blit(grid_img, (0, 0))
            sc.draw_table(table=gobang_mgr.table, w_img=w_img, b_img=b_img)

            # 不为0时，已分胜负
            if gobang_mgr.winner is not None:
                one_more_img = sc.loadimg("img/one_more_time.png", (100, 80))
                win_img = sc.loadimg(
                    file_loc="img/win.png" if gobang_mgr.winner == Role.player else "img/win_2.png",
                    size=(130, 45)
                )
                gv.g_screen.blit(win_img, (300, 495))
                gv.g_screen.blit(one_more_img, (20, 420))

            # 未分胜负
            else:
                # 电脑落子
                if gobang_mgr.busy:
                    # 显示 思考
                    gv.g_screen.blit(gv.g_txt_w_thinking, (670, 27))
                    computer_pgsbar.draw()

                # 玩家落子
                else:
                    pressed, pos = input_info.scan()
                    if pressed:
                        tab_pos = sc.pixpos_to_table(pos)
                        print("tab_pos: ", tab_pos)
                        gobang_mgr.player_take(tab_pos)

                    # 绘制进度条
                    gv.g_screen.blit(think_img, (680, 420))
                    player_pgsbar.draw()

            if not gobang_mgr.busy and gobang_mgr.step:
                goback_btn.update(gobang_mgr.go_back)
                goahead_btn.update(gobang_mgr.go_ahead)

            event_happend = back_btn.update()
            if event_happend:
                break

            pygame.display.update()
            gv.g_clock.tick(30)

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
