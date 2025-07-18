"""
#python版本：v3.5.1:37a07cee5969
#pygame版本：1.9.2a0
#运行环境：windows  10.0.10586 x64
#编译器： Visual Studio Community 2015 14.0.24720.00 Update 1
#Python Tools for Visual Studio： 2.2.31124.00

#author: caoliang  E-mail : i@caoliang.net
#http://www.caoliang.net

"""


import pygame
from pygame.locals import *
from sys import exit

from src import config as gv
from src import view as sc
from src import flow
from src.dynamic import effects
from src.dynamic import defeat


def main():
    global_init()
    btn_start = sc.Button(gv.g_btn_start_imgloc, gv.g_size_btn, gv.g_pos_btn_start)
    btn_about = sc.Button(gv.g_btn_about_imgloc, gv.g_size_btn, gv.g_pos_btn_about)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        gv.g_screen.blit(gv.g_home_img, (0, 0))

        btn_start.update(surface_game)
        btn_about.update(surface_about)

        pygame.display.update()
        gv.g_clock.tick(30)


def global_init():
    """加载一些全局资源"""
    pygame.init()

    # load icon & title
    pygame.display.set_icon(pygame.image.load(gv.g_icon_fileloc))
    pygame.display.set_caption(gv.g_wintitle)

    gv.g_screen = pygame.display.set_mode(gv.g_size_win)
    gv.g_clock = pygame.time.Clock()
    gv.g_home_img = sc.loadimg(gv.g_home_img_fileloc, gv.g_size_win)

    # 字体相关的载入
    gv.g_font = pygame.font.Font("src/sourcefile/ncsj.ttf", 18)
    gv.g_txt_w_thinking = gv.g_font.render("思考中…", True, gv.g_white)
    gv.g_txt_b_thinking = gv.g_font.render("思考中…", True, gv.g_black)

    # 棋盘步数字体
    default_font = "src/sourcefile/ncsj.ttf"

    max_txt = pygame.font.Font(default_font, 24)
    mid_txt = pygame.font.Font(default_font, 22)
    min_txt = pygame.font.Font(default_font, 20)
    for i in range(10):
        gv.g_num_tab += [max_txt.render(str(i), True, (180, 180, 180))]
    for i in range(10, 100):
        gv.g_num_tab += [mid_txt.render(str(i), True, (180, 180, 180))]
    for i in range(100, 256):
        gv.g_num_tab += [min_txt.render(str(i), True, (180, 180, 180))]


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
    confetti = effects.ConfettiEffect(gv.g_size_win[0], gv.g_size_win[1])
    defeat_effect = defeat.DefeatEffect(gv.g_size_win[0], gv.g_size_win[1])

    grid_img = sc.loadimg("src/img/grid.png", gv.g_size_win)
    w_img = sc.loadimg("src/img/round_white.png", (24, 24))
    b_img = sc.loadimg("src/img/round_black.png", (24, 24))
    think_img = sc.loadimg("src/img/think.png", (120, 60))
    
    back_btn = sc.Button(gv.g_btn_gameback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_gameback)
    goback_btn = sc.Button(gv.g_btn_goback_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goback)
    goahead_btn = sc.Button(gv.g_btn_goahead_imgloc, gv.g_size_btn_gameback, gv.g_pos_btn_goahead)

    computer_pgsbar = sc.ProgressBar("src/img/round_white.png", (12, 12), (675, 50), 40)
    player_pgsbar = sc.ProgressBar("src/img/round_black.png", (12, 12), (720, 440), 40)
    
    ctl = flow.FlowController()
    input_info = sc.GetInput()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

        # 绘制背景
        gv.g_screen.blit(grid_img, (0, 0))

        status = ctl.fresh_status()
        sc.draw_table(ctl.table, w_img, b_img)

        if back_btn.update() == 1:
            break

        if status == ctl.STATUS_PLAYER:
            # 玩家走子
            # 绘制进度条
            gv.g_screen.blit(think_img, (680, 420))
            player_pgsbar.draw()

            input_status = input_info.scan()
            if input_status[0] == 1:
                x, y = sc.pixpos_to_table((input_status[1], input_status[2]))
                ctl.player_take(x, y)

            if len(ctl.table) > 1:
                goback_btn.update(ctl.go_back)
                goahead_btn.update(ctl.go_ahead)

        elif status == ctl.STATUS_PC:
            gv.g_screen.blit(gv.g_txt_w_thinking, (670, 27))
            computer_pgsbar.draw()

        elif status == ctl.STATUS_OVER:
            one_more_img = sc.loadimg("src/img/one_more_time.png", (100, 80))
            gv.g_screen.blit(one_more_img, (20, 420))

            if ctl.winner == ctl.ROLE_PLAYER:
                # win_img = sc.loadimg("src/img/win.png", (130, 45))
                confetti.update()
                confetti.draw(gv.g_screen)
            else:
                # win_img = sc.loadimg("src/img/win_2.png", (130, 45))
                defeat_effect.update()
                defeat_effect.draw(gv.g_screen)
            # gv.g_screen.blit(win_img, (300, 495))

        pygame.display.update()
        gv.g_clock.tick(60)


if __name__ == "__main__":
    main()
