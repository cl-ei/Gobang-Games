# -*- coding: utf-8 -*-

"""
This file contains operations of drawring of bottons, progress bars and so on.

"""
import pygame
from globalvar import gv


def loadimg(file_loc, size):
    return pygame.transform.smoothscale(
        pygame.image.load(file_loc).convert_alpha(),
        size
    )


class Button(object):
    def __init__(self, btn_file_loc=(None, None, None), size=(0, 0), position=(0, 0)):
        self.screen = gv.g_screen
        self.position = position
        self.button_pushed = 0
        self.border_x = (position[0], position[0]+size[0])
        self.border_y = (position[1], position[1]+size[1])

        self.static_img = loadimg(btn_file_loc[0], size)
        self.focus_img = loadimg(btn_file_loc[1], size)
        self.down_img = loadimg(btn_file_loc[2], size)

    def ptr_not_in_border(self, pos):
        return not (
            (self.border_x[0] <= pos[0] <= self.border_x[1]) and
            (self.border_y[0] <= pos[1] <= self.border_y[1])
        )

    def update(self, callback=None, callback_args=None, callback_kwargs=None):
        mouse_pos = pygame.mouse.get_pos()
        event_happen = False

        # 如果指针未在按钮区域内，按钮状态置0
        if self.ptr_not_in_border(mouse_pos):
            self.screen.blit(self.static_img, self.position)
            self.button_pushed = 0

        else:
            # 指针在区域内，且已按下
            # 绘制按下图像，状态置1
            if pygame.mouse.get_pressed()[0] == 1:
                self.screen.blit(self.down_img, self.position)
                self.button_pushed = True       
                   
            else:
                if not self.button_pushed:
                    self.screen.blit(self.focus_img, self.position)
                else:
                    self.button_pushed = False
                    event_happen = True
                    if callable(callback):
                        callback_args = callback_args or ()
                        callback_kwargs = callback_kwargs or {}
                        callback(*callback_args, **callback_kwargs)
        return event_happen


class ProgressBar(object):
    def __init__(self, file_loc, size, pos, length):
        self.screen = gv.g_screen
        self.img = loadimg(file_loc, size)
        self.border = [pos[0], pos[0] + length]
        self.vertical_position = pos[1]
        self.level_position = self.border[0]
        self.direction = 1

    def draw(self):
        if self.direction == 1:
            self.level_position += 1
            if self.level_position > self.border[1]:
                self.level_position = self.border[1]
                self.direction = 0
            self.screen.blit(self.img,(self.level_position,self.vertical_position))

        else:
            self.level_position -= 1
            if self.level_position < self.border[0]:
                self.level_position = self.border[0]
                self.direction = 1
            self.screen.blit(self.img,(self.level_position,self.vertical_position))


def pixpos_to_table(pos):
    return (
        (pos[0] - gv.g_pos_grid_start[0] + 5)//gv.g_width_grid,
        (pos[1] - gv.g_pos_grid_start[1] + 5)//gv.g_width_grid,
    )


def teble_to_pixpos(pos):
    return (
        pos[0]*gv.g_width_grid + gv.g_pos_grid_start[0] - 2,
        pos[1]*gv.g_width_grid + gv.g_pos_grid_start[1] - 2,
    )


def draw_table(table, w_img, b_img):
    for __ in range(len(table)):
        table_pos = table[__]
        pix_pos = teble_to_pixpos(table_pos)
        blit_image = w_img if __ % 2 == 0 else b_img
        gv.g_screen.blit(blit_image, pix_pos)

        if __ == len(table) - 1:
            continue

        # draw index number
        if __ < 10:
            index_pos = pix_pos[0] + 8, pix_pos[1]
        elif __ < 100:
            index_pos = pix_pos[0] + 4, pix_pos[1] + 1
        else:
            index_pos = pix_pos[0] + 1, pix_pos[1] + 2
        num_surface = gv.g_num_tab[__ + 1]
        gv.g_screen.blit(num_surface, index_pos)

    # draw last position
    if table:
        last_step_pos = teble_to_pixpos(table[-1])
        last_step_pix_pos = last_step_pos[0] + 12, last_step_pos[1] + 12
        pygame.draw.circle(gv.g_screen, (200, 0, 0), last_step_pix_pos, 4)
    return


def draw_five(core):
    for i in range(5):
        circle_pos = teble_to_pixpos(core.five_pcs[i])
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12
        pygame.draw.circle(gv.g_screen, (200, 0, 0), (x, y), 4)


class GetInput(object):
    def __init__(self):
        # error 鼠标可以偏移竖线的距离
        self.border_x = (gv.g_pos_grid_start[0], gv.g_size_grid + gv.g_pos_grid_start[0])
        self.border_y = (gv.g_pos_grid_start[1], gv.g_size_grid + gv.g_pos_grid_start[1])

        self.last_position = [0, 0]
        self.mouse_kdown = 0

    def scan(self):
        return_data = False, (0, 0)
        mouse_status = pygame.mouse.get_pressed()[0]

        # 当鼠标按下的时候
        if mouse_status == 1:
            self.mouse_kdown = 1
            self.last_position = pygame.mouse.get_pos()

        # 鼠标未按下
        else:
            # 从按下的瞬间抬起
            if self.mouse_kdown == 1:
                self.mouse_kdown = 0
                pos = pygame.mouse.get_pos()
                if self.ptr_in_border(pos):
                    return_data = True, pos
                else:
                    # 移出边界，无效
                    pass

        return return_data

    def ptr_in_border(self, pos):
        return (
            (self.border_x[0] - 4) <= pos[0] <= (self.border_x[1] + 4) and
            (self.border_y[0] - 4) <= pos[1] <= (self.border_y[1] + 4)
        )
