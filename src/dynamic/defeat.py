import pygame
import random
import math
import time

class DefeatEffect:
    def __init__(self, screen_width, screen_height, num_particles=150):
        """
        失败特效类 - 破碎棋子灰烬效果

        参数:
        screen_width - 屏幕宽度
        screen_height - 屏幕高度
        num_particles - 粒子数量(默认150)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.particles = []
        self.active = True
        self.create_time = time.time()

        # 创建主破碎棋子
        self.main_pieces = []
        for i in range(5):
            self.main_pieces.append({
                'x': screen_width / 2,
                'y': screen_height / 2,
                'size': random.randint(15, 25),
                'rotation': 0,
                'rotation_speed': random.uniform(-2, 2),
                'velocity_x': random.uniform(-4, 4),
                'velocity_y': random.uniform(-6, -2),
                'gravity': random.uniform(0.1, 0.2),
                'color': (80, 80, 80),
                'alpha': 255
            })

        # 初始化灰烬粒子
        for _ in range(num_particles):
            self.particles.append(self._create_particle())

    def _create_particle(self):
        """创建一个灰烬粒子"""
        # 使用灰黑色调
        gray_value = random.randint(40, 100)
        color = (gray_value, gray_value, gray_value)

        # 创建粒子
        particle = {
            'x': self.screen_width / 2,
            'y': self.screen_height / 2,
            'size': random.randint(2, 6),
            'size_decay': random.uniform(0.95, 0.99),
            'color': color,
            'alpha': random.randint(200, 255),
            'alpha_decay': random.uniform(0.98, 0.995),
            'velocity_x': random.uniform(-3, 3),
            'velocity_y': random.uniform(-3, 3),
            'gravity': random.uniform(0.05, 0.1),
            'rotation': random.uniform(0, 360),
            'rotation_speed': random.uniform(-3, 3),
            'lifetime': random.uniform(2, 4),
            'birth_time': time.time()
        }
        return particle

    def update(self):
        """更新所有粒子状态"""
        if not self.active:
            return

        current_time = time.time()

        # 更新主破碎棋子
        for piece in self.main_pieces:
            piece['x'] += piece['velocity_x']
            piece['y'] += piece['velocity_y']
            piece['velocity_y'] += piece['gravity']
            piece['rotation'] += piece['rotation_speed']
            piece['alpha'] *= 0.98  # 逐渐消失

            # 当棋子掉出屏幕或透明度太低时停止更新
            if (piece['y'] > self.screen_height + 50 or
                piece['alpha'] < 10 or
                piece['x'] < -50 or
                piece['x'] > self.screen_width + 50):
                continue

        # 更新灰烬粒子
        for p in self.particles[:]:
            # 更新位置
            p['x'] += p['velocity_x']
            p['y'] += p['velocity_y']
            p['velocity_y'] += p['gravity']

            # 更新属性
            p['rotation'] += p['rotation_speed']
            p['alpha'] *= p['alpha_decay']
            p['size'] *= p['size_decay']

            # 移除过期粒子
            if (current_time - p['birth_time'] > p['lifetime'] or
                p['alpha'] < 5 or
                p['size'] < 0.5):
                self.particles.remove(p)
                self.particles.append(self._create_particle())

    def draw(self, screen):
        """在屏幕上绘制所有元素"""
        if not self.active:
            return

        # 绘制半透明覆盖层（暗淡色调）
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 40))  # 深色半透明
        screen.blit(overlay, (0, 0))

        # 绘制失败文字
        font = pygame.font.Font("src/sourcefile/ncsj.ttf", 80)
        defeat_text = font.render("失败TAT", True, (255, 255, 100))
        text_rect = defeat_text.get_rect(center=(self.screen_width//2, self.screen_height//3))
        screen.blit(defeat_text, text_rect)

        # 绘制主破碎棋子
        for piece in self.main_pieces:
            if piece['alpha'] > 10:
                # 创建棋子表面
                size = piece['size']
                piece_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)

                # 绘制圆形棋子
                pygame.draw.circle(piece_surface, (*piece['color'], piece['alpha']),
                                   (size, size), size)

                # 添加裂痕效果
                pygame.draw.line(piece_surface, (30, 30, 30),
                                (size * 0.2, size * 0.2),
                                (size * 0.8, size * 0.8), 2)

                # 旋转
                rotated = pygame.transform.rotate(piece_surface, piece['rotation'])

                # 绘制到屏幕
                screen.blit(rotated, (piece['x'] - rotated.get_width()//2,
                                      piece['y'] - rotated.get_height()//2))

        # 绘制灰烬粒子
        for p in self.particles:
            if p['alpha'] > 5:
                # 创建粒子表面
                particle_surface = pygame.Surface((p['size']*2, p['size']*2), pygame.SRCALPHA)

                # 绘制粒子（小方块）
                pygame.draw.rect(particle_surface, (*p['color'], p['alpha']),
                                [0, 0, p['size'], p['size']])

                # 旋转
                rotated = pygame.transform.rotate(particle_surface, p['rotation'])

                # 绘制到屏幕
                screen.blit(rotated, (p['x'] - rotated.get_width()//2,
                                     p['y'] - rotated.get_height()//2))

    def stop(self):
        """停止特效"""
        self.active = False

    def restart(self):
        """重启特效"""
        self.active = True
        self.create_time = time.time()

        # 重置主破碎棋子
        self.main_pieces = []
        for i in range(5):
            self.main_pieces.append({
                'x': self.screen_width / 2,
                'y': self.screen_height / 2,
                'size': random.randint(15, 25),
                'rotation': 0,
                'rotation_speed': random.uniform(-2, 2),
                'velocity_x': random.uniform(-4, 4),
                'velocity_y': random.uniform(-6, -2),
                'gravity': random.uniform(0.1, 0.2),
                'color': (80, 80, 80),
                'alpha': 255
            })

        # 重置灰烬粒子
        self.particles = []
        for _ in range(len(self.particles) or 150):
            self.particles.append(self._create_particle())
