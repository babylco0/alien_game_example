import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """飞船类"""
    def __init__(self, ai_settings, screen):
        """初始化飞船并设置飞船初始位置"""
        super(Ship, self).__init__()
        self.screen = screen
        # 加载飞船图像
        self.image = pygame.image.load('images/ship_s.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        # 将飞船放置在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 飞船中心
        self.center = float(self.rect.centerx)
        self.high = float(self.rect.y)
        # 飞船持续移动标识
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False
        self.ai_settings = ai_settings

    def update(self):
        """更新飞船位置"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.center -= self.ai_settings.ship_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.high -= self.ai_settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.high += self.ai_settings.ship_speed_factor
        self.rect.centerx = self.center
        self.rect.y = self.high

    def center_ship(self):
        """将飞船放置于屏幕底部中央"""
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.high = float(self.rect.y)

    def blitme(self):
        """在指定位置绘制飞船"""
        self.screen.blit(self.image, self.rect)
