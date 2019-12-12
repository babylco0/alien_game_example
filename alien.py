import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """外星人类"""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        # 加载图像并设置rect属性
        self.image = pygame.image.load('images/alien_s.png')
        self.rect = self.image.get_rect()
        # 设置初始位置为屏幕左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # 准确位置
        self.x = float(self.rect.x)

    def update(self):
        """移动外星人"""
        self.x += (self.ai_settings.alien_speed_factor *
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """检测外星人是否位于屏幕边缘"""
        scree_rect = self.screen.get_rect()
        if self.rect.right >= scree_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
        return False

    def blitme(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)
