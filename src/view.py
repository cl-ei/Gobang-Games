"""
#此文件包含部分按钮、进度条等组件的绘制和事件处理

"""
import pygame
from typing import *
from src import config as gv


def loadimg(file_loc, size=(0, 0)):
    img = pygame.image.load(file_loc).convert_alpha()
    return pygame.transform.smoothscale(img, size)


class Button:
    def __init__(self, btn_file_loc=(None, None, None), size=(0, 0), position=(0, 0)):
        self.screen = gv.g_screen
        self.position = position
        self.button_pushed = 0
        self.border_x = (position[0], position[0] + size[0])
        self.border_y = (position[1], position[1] + size[1])

        self.static_img = loadimg(btn_file_loc[0], size)
        self.focus_img = loadimg(btn_file_loc[1], size)
        self.down_img = loadimg(btn_file_loc[2], size)

    def ptr_not_in_border(self, pos):
        if self.border_x[0] <= pos[0] <= self.border_x[1] and \
                self.border_y[0] <= pos[1] <= self.border_y[1]:
            return False
        else:
            return True

    def update(self, cb: Callable = None):
        mouse_pos = pygame.mouse.get_pos()
        event_happen = 0

        # 如果指针未在按钮区域内，按钮状态置0
        if self.ptr_not_in_border(mouse_pos) == True:
            self.screen.blit(self.static_img, self.position)
            self.button_pushed = 0

        else:
            # 指针在区域内，且已按下
            # 绘制按下图像，状态置1
            if pygame.mouse.get_pressed()[0] == 1:
                self.screen.blit(self.down_img, self.position)
                self.button_pushed = True

            else:

                if self.button_pushed == False:
                    self.screen.blit(self.focus_img, self.position)
                else:
                    self.button_pushed = False
                    event_happen = 1
                    if cb is not None:
                        cb()
        return event_happen


class ProgressBar:
    def __init__(self, file_loc, size, pos, len):
        self.screen = gv.g_screen
        self.img = loadimg(file_loc, size)
        self.border = [pos[0], pos[0] + len]
        self.vertical_position = pos[1]
        self.level_position = self.border[0]
        self.direction = 1

    def draw(self):
        if self.direction == 1:
            self.level_position += 1
            if self.level_position > self.border[1]:
                self.level_position = self.border[1]
                self.direction = 0
            self.screen.blit(self.img, (self.level_position, self.vertical_position))
        else:
            self.level_position -= 1
            if self.level_position < self.border[0]:
                self.level_position = self.border[0]
                self.direction = 1
            self.screen.blit(self.img, (self.level_position, self.vertical_position))


def pixpos_to_table(pos=(0, 0)):
    """
    返回坐标元祖
    · → x
    ↓
    y

    """
    x = (pos[0] - gv.g_pos_grid_start[0] + 5) // gv.g_width_grid
    y = (pos[1] - gv.g_pos_grid_start[1] + 5) // gv.g_width_grid
    return x, y


def table_to_pix(x, y):
    """将坐标转换成像素位置 """
    return [x * gv.g_width_grid + gv.g_pos_grid_start[0] - 2,
            y * gv.g_width_grid + gv.g_pos_grid_start[1] - 2]


def draw_table(table: List[Tuple[int, int]], w_img, b_img):
    """
    绘制棋子

    """
    for i, pos in enumerate(table):
        x, y = table_to_pix(pos[0], pos[1])
        img = w_img if i % 2 == 0 else b_img
        gv.g_screen.blit(img, (x, y))

        i += 1
        if i == len(table):
            break
        if i < 10:
            gv.g_screen.blit(gv.g_num_tab[i], (x + 8, y))
        elif i < 100:
            gv.g_screen.blit(gv.g_num_tab[i], (x + 4, y + 1))
        else:
            gv.g_screen.blit(gv.g_num_tab[i], (x + 1, y + 2))

    # 绘制最后一步棋子上的红点
    if table:
        last = table[-1]
        circle_pos = table_to_pix(last[0], last[1])
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12
        pygame.draw.circle(gv.g_screen, (200, 0, 0), (x, y), 4)


def draw_five(core):
    for i in range(5):
        circle_pos = teble_to_pixpos(core.five_pcs[i])
        x = circle_pos[0] + 12
        y = circle_pos[1] + 12
        pygame.draw.circle(gv.g_screen, (200, 0, 0), (x, y), 4)


class GetInput():
    def __init__(self):
        # error 鼠标可以偏移竖线的距离
        self.border_x = (gv.g_pos_grid_start[0], gv.g_size_grid + gv.g_pos_grid_start[0])
        self.border_y = (gv.g_pos_grid_start[1], gv.g_size_grid + gv.g_pos_grid_start[1])

        self.last_position = [0, 0]
        self.mouse_kdown = 0

    def scan(self):
        return_data = (-1, 0, 0)
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
                if self.ptr_in_border(pos) == 1:
                    return_data = (1, pos[0], pos[1])
                else:
                    # 移出边界，无效
                    pass

        return return_data

    def ptr_in_border(self, pos):
        if (self.border_x[0] - 4) <= pos[0] <= (self.border_x[1] + 4) and \
                (self.border_y[0] - 4) <= pos[1] <= (self.border_y[1] + 4):
            return 1
        else:
            return 0
