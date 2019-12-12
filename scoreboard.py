import pygame
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """显示得分信息类"""

    def __init__(self, ai_settings, screen, stats):
        """初始化得分板属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats
        # 得分信息字体
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # 初始得分图像
        self.score_image = None
        self.score_rect = None
        self.prep_score()

        # 最高分图像
        self.high_score_image = None
        self.high_score_rect = None
        self.prep_high_score()

        # 等级图像
        self.level_image = None
        self.level_rect = None
        self.prep_level()

        # 显示剩余飞船数
        self.ships = None
        self.prep_ships()

    def prep_score(self):
        """将得分渲染为图像"""
        # score_str = str(self.stats.score)
        rounded_score = int (round(self.stats.score, -1))
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.ai_settings.bg_color)

        # 将得分放置于屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高分渲染为图像"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.ai_settings.bg_color)
        # 将最高分置于屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.screen_rect.top

    def prep_level(self):
        """将等级渲染为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.ai_settings.bg_color)
        # 将最高分置于得分下方
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """渲染剩余飞船数"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        """显示得分, 最高分, 等级"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)
