# -*- coding: utf-8 -*-

"""
python version: v3.5.1:37a07cee5969
pygame version:1.9.2a0
env: windows  10.0.10586 x64

author: caoliang  E-mail : i#caoliang.net
http://www.caoliang.net
"""

import pygame
from pygame.locals import *
from sys import exit
from globalvar import gv
from view import sc
from newcore import GameManager, Role


def _main():
    
    global_init()    

    btn_start = sc.Button(gv.g_btn_start_imgloc, gv.g_size_btn, gv.g_pos_btn_start)
    btn_about = sc.Button(gv.g_btn_about_imgloc, gv.g_size_btn, gv.g_pos_btn_about)

    surface_game()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        gv.g_screen.blit(gv.g_home_img, (0, 0))

        btn_start.update(surface_game)
        btn_about.update(surface_about)

        pygame.display.update()
        gv.g_clock.tick(30)


def surface_about():
        
    btn_back = sc.Button(gv.g_btn_back_imgloc, gv.g_size_btn, gv.g_pos_btn_back)
    about_bkgimg = sc.loadimg(gv.g_surfaceback_img_fileloc, gv.g_size_win)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
        gv.g_screen.blit(about_bkgimg, (-1, -1))
        if btn_back.update() == 1:
            break
        pygame.display.update()
        gv.g_clock.tick(30)


def surface_game():

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


class Game(object):
    def __init__(self, window_size, caption, icon=None):
        pygame.init()

        if caption is not None:
            pygame.display.set_caption(caption)
        if icon is not None:
            pygame.display.set_icon(pygame.image.load(icon))

        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.clock = pygame.time.Clock()

        gv.g_home_img = sc.loadimg(gv.g_home_img_fileloc, self.window_size)

        # 字体相关的载入
        gv.g_font = pygame.font.Font("sourcefile/ncsj.ttf", 18)
        gv.g_txt_w_thinking = gv.g_font.render("思考中…", True, gv.g_white)
        gv.g_txt_b_thinking = gv.g_font.render("思考中…", True, gv.g_black)

        # 棋盘步数字体
        default_font = "sourcefile/ncsj.ttf"

        max_txt = pygame.font.Font(default_font, 24)
        mid_txt = pygame.font.Font(default_font, 22)
        min_txt = pygame.font.Font(default_font, 20)
        for i in range(10):
            gv.g_num_tab += [max_txt.render(str(i), True, (180, 180, 180))]
        for i in range(10, 100):
            gv.g_num_tab += [mid_txt.render(str(i), True, (180, 180, 180))]
        for i in range(100, 256):
            gv.g_num_tab += [min_txt.render(str(i), True, (180, 180, 180))]

    def wait_start(self):
        pass

    def gaming(self):
        pass

    def about(self):
        pass


def main():
    game = Game()
    while True:
        game.wait_start()
        game.gaming()


if __name__ == "__main__":
    main()
