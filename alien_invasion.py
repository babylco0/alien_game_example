import pygame
import time
from settings import Settings
from ship import Ship
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard


def run_game():
    """运行游戏"""
    # 初始化屏幕对象
    pygame.init()

    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,
                                      ai_settings.screen_height))
    # pygame.display.toggle_fullscreen()
    # ai_settings.screen_width = pygame.display.Info().current_w
    # ai_settings.screen_height = pygame.display.Info().current_h
    pygame.display.set_caption('Alien Invasion')
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个子弹编组
    bullets = Group()
    # 创建一个外星人
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 创建一个存储游戏统计信息实例
    stats = GameStats(ai_settings)
    # 创建开始按钮
    play_button = Button(ai_settings, screen, 'Play')
    # 创建记分板
    sb = Scoreboard(ai_settings, screen, stats)
    # 开始游戏主循环
    while True:
        # 监听鼠标键盘事件
        gf.check_events(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)
        time.sleep(.1)


run_game()

