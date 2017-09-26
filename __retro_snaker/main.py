import random
import sys
import pygame
from pygame.examples.prevent_display_stretching import clock


class Snake(object):
    def __init__(self, windows=(500, 500)):
        self.color = (255, 255, 255)
        self.length = 2
        self.positon = [[5, 5], [4, 5]]
        self.position_display = [0, 0, 50, 50]
        self.position_obs = [3, 6]
        self.position_tlg = [0, 0]
        self.border = (int(windows[0]/50), int(windows[1]/50))

    def update_display(self, screen):
        for i in range(0, self.length):
            pygame.draw.rect(screen, self.color, (self.positon[i][0]*50+5, self.positon[i][1]*50+5, 40, 40), 0)
            pygame.draw.circle(screen, (100, 0, 0), (self.positon[0][0]*50+25, self.positon[0][1]*50+25), 10, 0)
        pygame.draw.rect(screen, (200, 0, 0), (self.position_obs[0]*50, self.position_obs[1]*50, 50, 50), 0)

    def update_position(self, dir):
        if dir == 'L':
            self.positon.insert(0, [self.positon[0][0]-1, self.positon[0][1]])
            self.position_tlg = self.positon.pop(self.length)
            self.not_dir = 'R'
        if dir == 'R':
            self.positon.insert(0, [self.positon[0][0]+1, self.positon[0][1]])
            self.position_tlg = self.positon.pop(self.length)
            self.not_dir = 'L'
        if dir == 'U':
            self.positon.insert(0, [self.positon[0][0], self.positon[0][1]-1])
            self.position_tlg = self.positon.pop(self.length)
            self.not_dir = 'D'
        if dir == 'D':
            self.positon.insert(0, [self.positon[0][0], self.positon[0][1]+1])
            self.position_tlg = self.positon.pop(self.length)
            self.not_dir = 'U'

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


class Player(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(player_img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y


def game_start(screen, windows=(500, 500)):
    game_font = pygame.font.Font("cl.ttf", 30)
    game_font_small = pygame.font.Font("cl.ttf", 18)
    game_start_image = game_font.render("WELCOME TO PLAY CL'S SNAKE!", True, (222, 100, 70))
    game_start_image_2 = game_font_small.render("PRESS ANY BUTTON TO START -->", True, (222, 100, 70))
    screen.blit(game_start_image, (windows[0]*0.18, windows[1]*0.7))
    screen.blit(game_start_image_2, (windows[0]*0.18+65, windows[1]*0.7+45))

    cl_player = Player(280, 120, 150, 150)
    display_img = pygame.sprite.RenderPlain(cl_player)
    display_img.draw(screen)
    pygame.display.update()

    wait_to_start = True
    while wait_to_start:        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                wait_to_start = False


def game_over(screen, windows=(500, 500), score=100):
    game_over_font = pygame.font.Font("cl.ttf", 30)
    game_over_font_small = pygame.font.Font("cl.ttf", 20)
    game_over_img = game_over_font.render("GAME OVER !", True, (222, 100, 80))
    pygame.draw.rect(screen, (100, 100, 100), (windows[0]*0.3, windows[1]*0.3, windows[0]*0.4, windows[1]*0.4), 0)
    screen.blit(game_over_img, (windows[0]*0.37, windows[1]*0.4))
    score_str = "SCORE : " + str(score)
    score_img = game_over_font_small.render(score_str, True, ((222, 100, 80)))
    screen.blit(score_img, (windows[0]*0.4, windows[1]*0.4+70))
    pygame.display.update()
    while True:
        clock.tick(20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


def main():
    direction_choice = ("L", "R", "U", "D")
    direction = random.choice(direction_choice)
    dir_need_frash = True
    timetick = 0
    game_conflict = False
    windows_size = (700, 500)

    player_img = "head.png"
    clsnake = Snake(windows_size)

    pygame.init()
    game_clock = pygame.time.Clock()

    screen = pygame.display.set_mode(resolution=windows_size)
    pygame.display.set_caption("CL's Snake !")

    # game_start(screen, windows_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    if dir != 'D' and dir_need_frash:
                        dir = 'U'
                        dir_need_frash = False
                elif event.key == pygame.K_DOWN:
                    if dir != 'U' and dir_need_frash:
                        dir = 'D'
                        dir_need_frash = False
                elif event.key == pygame.K_LEFT:
                    if dir != 'R' and dir_need_frash:
                        dir = 'L'
                        dir_need_frash = False
                elif event.key == pygame.K_RIGHT:
                    if dir != 'L' and dir_need_frash:
                        dir = 'R'
                        dir_need_frash = False

        # set speed
        speed_grade = 20 - int(clsnake.length/3)
        if speed_grade < 1:
            speed_grade = 1

        # blank screen
        screen.fill((30, 30, 30))

        # update snake_position
        if timetick == speed_grade:
            clsnake.update_position(dir)
            dir_need_frash = True
            timetick = 0

        # check conflict
        game_conflict = clsnake.confilct()
        if game_conflict == 1:
            clsnake.update_obs()
            clsnake.add_tlg()
        elif game_conflict == 2:
            clsnake.update_display(screen)
            game_over(screen, windows_size, clsnake.length*100)

        # update display
        clsnake.update_display(screen)

        pygame.display.update()

        # time tick
        game_clock.tick(20)
        timetick += 1


if __name__ == "__main__":
    main()
