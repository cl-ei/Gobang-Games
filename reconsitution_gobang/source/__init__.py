"""
This module contains operations of drawring of bottons, progress bars and source files.

"""
import pygame

# --------------------------------- clip infp -------------------------------------- #
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


def loadimg(file_loc, size=None):
    image = pygame.transform.smoothscale(
        pygame.image.load(file_loc).convert_alpha(),
        size
    )
    return image


class StandardButton(object):
    def __init__(self, text, style, callback=None):
        self.text = text
        self.callback = callback

        self.width = style.get("width", 10)
        self.heigth = style.get("heigth", 10)
        self.top = style.get("top", 0)
        self.left = style.get("left", 0)

        self.rect = (
            self.left,
            self.top,
            self.width,
            self.heigth
        )

        color = style.get("color", (30, 30, 30))
        background = style.get("background", (250, 250, 250))
        font_family = style.get("font_family", "./source/ncsj.ttf")
        font_size = style.get("font_size", 30)
        self.default_img = pygame.font.Font(font_family, font_size).render(
            text, True, color, background
        )

        hoverd_style = style.get("hover", {})
        hoverd_font_size = hoverd_style.get("font_size", 34)
        hoverd_color = hoverd_style.get("color", (40, 40, 40))
        hoverd_background = hoverd_style.get("background", (230, 230, 230))
        self.hoverd_img = pygame.font.Font(font_family, hoverd_font_size).render(
            text, True, hoverd_color, hoverd_background
        )

        pushed_style = style.get("pushed", {})
        pushed_font_size = pushed_style.get("font_size", 24)
        pushed_color = pushed_style.get("color", (90, 90, 90))
        pushed_background = pushed_style.get("background", (200, 200, 200))
        self.pushed_img = pygame.font.Font(font_family, pushed_font_size).render(
            text, True, pushed_color, pushed_background
        )

        self._pushed_last_scan = False

    def is_mouseover(self, pos):
        x, y = pos
        return (
            self.left <= x <= self.left + self.width
            and self.top <= y <= self.top + self.heigth
        )

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        event_happen = False
        surface = screen.subsurface(self.rect)

        if not self.is_mouseover(mouse_pos):
            surface.blit(self.default_img, (0, 0))
            self._pushed_last_scan = False
            return event_happen

        surface.blit(self.hoverd_img, (0, 0))
        self._pushed_last_scan = False
        return event_happen


class Button(object):
    def __init__(self, style, callback=None):

        self.callback = callback

        self.width = style.get("width", 10)
        self.heigth = style.get("heigth", 10)
        self.top = style.get("top", 0)
        self.left = style.get("left", 0)

        self.rect = (
            self.left,
            self.top,
            self.width,
            self.heigth
        )

        self.default_img, self.hovered_img, self.pushed_img = [
            pygame.transform.scale(style.get(img_name), (self.width, self.heigth))
            for img_name in ("default_img", "hovered_img", "pushed_img")
        ]

        self._pushed_just_now = False

    def is_mouseover(self, pos):
        x, y = pos
        return (
            self.left <= x <= self.left + self.width
            and self.top <= y <= self.top + self.heigth
        )

    def update(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if not self.is_mouseover(mouse_pos):
            screen.blit(self.default_img, self.rect)
            self._pushed_just_now = False
            return False

        if pygame.mouse.get_pressed()[0]:
            screen.blit(self.pushed_img, self.rect)
            self._pushed_just_now = True
            return False

        if self._pushed_just_now:
            self._pushed_just_now = False
            if callable(self.callback):
                self.callback()
            return True

        screen.blit(self.hovered_img, self.rect)
        self._pushed_just_now = False
        return False


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
