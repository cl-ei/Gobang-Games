import sys
import random
import pygame
from pygame.locals import QUIT, KEYUP, K_UP, K_DOWN, K_LEFT, K_RIGHT

direction_choice = ("L", "R", "U", "D")


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, width, height):
        super(Player, self).__init__()

        self.player_img_path = "head.png"
        self.image = pygame.transform.scale(pygame.image.load(self.player_img_path), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y


class Snake(object):
    def __init__(self, windows_size, caption=None, icon=None, fps=20):
        self.windows_size = windows_size

        pygame.init()
        self.screen = pygame.display.set_mode(windows_size)
        self.clock = pygame.time.Clock()
        if caption is not None:
            pygame.display.set_caption("CL's Snake !")
        if icon is not None:
            pygame.display.set_icon(icon)

        self.fps = fps

        self.direction = random.choice(direction_choice)
        self.score = 0
        self.time_tick = 0
        self.dir_need_frash = False
        self.length = 2

        self.positon = [[5, 5], [4, 5]]
        self.position_display = [0, 0, 50, 50]
        self.position_obs = [3, 6]
        self.position_tlg = [0, 0]
        self.border = (int(windows_size[0]/50), int(windows_size[1]/50))

    def draw_rect(self, color, rect, width=0):
        pygame.draw.rect(self.screen, color, rect, width)

    def draw_circle(self, color, pos, radius, width=0):
        pygame.draw.circle(self.screen, color, pos, radius, width)

    def update_display(self):
        pygame.display.update()
        self.time_tick += 1
        self.clock.tick(self.fps)

    def start(self):
        game_font = pygame.font.Font("cl.ttf", 30)
        game_font_small = pygame.font.Font("cl.ttf", 18)
        game_start_image = game_font.render("WELCOME TO PLAY CL'S SNAKE!", True, (222, 100, 70))
        game_start_image_2 = game_font_small.render("PRESS ANY BUTTON TO START -->", True, (222, 100, 70))
        self.screen.blit(
            game_start_image,
            (self.windows_size[0] * 0.18, self.windows_size[1] * 0.7)
        )
        self.screen.blit(
            game_start_image_2,
            (self.windows_size[0] * 0.18 + 65, self.windows_size[1] * 0.7 + 45)
        )

        cl_player = Player(280, 120, 150, 150)
        display_img = pygame.sprite.RenderPlain(cl_player)
        display_img.draw(self.screen)
        self.update_display()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                elif event.type == KEYUP:
                    return

    def over(self):
        screen = self.screen
        windows = self.windows_size

        game_over_font = pygame.font.Font("cl.ttf", 30)
        game_over_font_small = pygame.font.Font("cl.ttf", 20)
        game_over_img = game_over_font.render("GAME OVER !", True, (222, 100, 80))
        self.draw_rect(
            color=(100, 100, 100),
            rect=(windows[0] * 0.3, windows[1] * 0.3, windows[0] * 0.4, windows[1] * 0.4),
        )
        screen.blit(
            source=game_over_img,
            dest=(windows[0] * 0.37, windows[1] * 0.4)
        )
        score_img = game_over_font_small.render("SCORE : %s" % self.score, True, (222, 100, 80))
        screen.blit(
            source=score_img,
            dest=(windows[0] * 0.4, windows[1] * 0.4 + 70)
        )
        self.update_display()

        while True:
            self.clock.tick(20)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)

    def update_position(self):
        next_position_map = {
            "L": [self.positon[0][0] - 1, self.positon[0][1]],
            "R": [self.positon[0][0] + 1, self.positon[0][1]],
            "U": [self.positon[0][0], self.positon[0][1] - 1],
            "D": [self.positon[0][0], self.positon[0][1] + 1],
        }
        self.positon.insert(0, next_position_map.get(self.direction))
        self.position_tlg = self.positon.pop(self.length)

    def add_tlg(self):
        self.positon.insert(self.length, self.position_tlg)
        self.length += 1

    def update_obs(self):
        on_snake = True
        while on_snake:
            self.position_obs = [random.randint(0, self.border[0]-1), random.randint(0, self.border[1]-1)]
            if self.positon.count(self.position_obs) == 1:
                on_snake = True
            else:
                on_snake = False

    def confilct(self):
        return_data = 3
        if self.position_obs == self.positon[0]:
            return_data = 1
        elif not (self.border[0] > self.positon[0][0] >= 0 and self.border[1] > self.positon[0][1] >= 0):
            return_data = 2

        for i in range(0, self.length):
            if self.positon.count(self.positon[i]) > 1:
                return_data = 2
        return return_data

    def parse_event(self, event):
        if event.type != KEYUP or not self.dir_need_frash:
            return

        forbidden_key_map = {
            "D": "U",
            "U": "D",
            "L": "R",
            "R": "L",
        }
        switch_key_map = {
            K_UP: "U",
            K_DOWN: "D",
            K_LEFT: "L",
            K_RIGHT: "R",
        }
        event_key_dir = switch_key_map.get(event.key)
        if event_key_dir and forbidden_key_map.get(event_key_dir) != self.direction:
            self.dir_need_frash = False
            self.direction = event_key_dir

    def update(self):
        self.screen.fill((30, 30, 30))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit(0)
                else:
                    self.parse_event(event=event)

            for i in range(self.length):
                self.draw_rect(
                    color=(255, 255, 255),
                    rect=(self.positon[i][0]*50 + 5, self.positon[i][1]*50 + 5, 40, 40)
                )
                self.draw_circle(
                    color=(100, 0, 0),
                    pos=(self.positon[0][0]*50+25, self.positon[0][1]*50+25),
                    radius=10
                )
            self.draw_rect(color=(200, 0, 0), rect=(self.position_obs[0]*50, self.position_obs[1]*50, 50, 50))

            self.update_display()


def main():
    windows_size = (700, 500)

    caption = "CL's snake !"
    ratro_snaker = Snake(windows_size=windows_size, caption=caption)

    while True:
        ratro_snaker.start()
        ratro_snaker.update()
        ratro_snaker.over()


if __name__ == "__main__":
    main()
