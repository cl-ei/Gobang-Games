import pygame
import random
import math
import time

class ConfettiEffect:
    def __init__(self, screen_width, screen_height, num_particles=200):
        """
        彩纸特效类

        参数:
        screen_width - 屏幕宽度
        screen_height - 屏幕高度
        num_particles - 彩纸粒子数量(默认200)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.start_time = time.time()
        self.active = True

        # 初始化彩纸粒子
        for _ in range(num_particles):
            self.particles.append(self._create_particle())

    def _create_particle(self):
        """创建一个彩纸粒子"""
        # 粒子基础属性
        particle = {
            'x': random.randint(0, self.screen_width),
            'y': random.randint(-100, -10),  # 从屏幕上方开始
            'speed': random.uniform(1, 5),
            'size': random.randint(5, 15),
            'rotation': random.uniform(0, 360),
            'rotation_speed': random.uniform(-5, 5),
            'color': (
                random.randint(180, 255),
                random.randint(180, 255),
                random.randint(180, 255)
            ),
            # 物理属性
            'gravity': random.uniform(0.05, 0.15),
            'wobble_speed': random.uniform(0.05, 0.2),
            'wobble_amplitude': random.uniform(1, 3),
            # 生命周期
            'lifetime': random.uniform(5, 15),
            'birth_time': time.time()
        }
        return particle

    def update(self):
        """更新所有粒子状态"""
        if not self.active:
            return

        current_time = time.time()

        for p in self.particles:
            # 计算摆动偏移
            wobble = math.sin(current_time * p['wobble_speed']) * p['wobble_amplitude']

            # 更新位置
            p['x'] += wobble
            p['y'] += p['speed']
            p['speed'] += p['gravity']
            p['rotation'] += p['rotation_speed']

            # 重置掉出屏幕的粒子
            if (p['y'] > self.screen_height or
                p['x'] < -20 or
                p['x'] > self.screen_width + 20 or
                current_time - p['birth_time'] > p['lifetime']):
                self.particles.remove(p)
                self.particles.append(self._create_particle())

    def draw(self, screen):
        """在屏幕上绘制所有粒子"""
        if not self.active:
            return

        # 绘制透明背景（暗色半透明覆盖层）
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 40))  # 半透明黑色
        screen.blit(overlay, (0, 0))

        # 绘制胜利文字
        font = pygame.font.Font("src/sourcefile/ncsj.ttf", 80)
        win_text = font.render("恭喜获胜><!", True, (255, 255, 100))
        text_rect = win_text.get_rect(center=(self.screen_width//2, self.screen_height//3))
        screen.blit(win_text, text_rect)

        # 绘制所有彩纸粒子
        for p in self.particles:
            # 创建旋转的矩形
            rect = pygame.Rect(0, 0, p['size'], p['size'])
            surface = pygame.Surface((p['size'], p['size']), pygame.SRCALPHA)
            pygame.draw.rect(surface, p['color'], rect)

            # 旋转图形
            rotated = pygame.transform.rotate(surface, p['rotation'])

            # 绘制到屏幕
            screen.blit(rotated, (p['x'] - rotated.get_width()//2,
                                 p['y'] - rotated.get_height()//2))

    def stop(self):
        """停止特效"""
        self.active = False

    def restart(self):
        """重启特效"""
        self.active = True
        self.start_time = time.time()

        # 重置所有粒子
        self.particles = []
        for _ in range(len(self.particles) or 200):
            self.particles.append(self._create_particle())
