class Settings:
    """设置类"""
    def __init__(self):
        """初始化游戏设置"""
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.ship_speed_factor = 20
        self.ship_limit = 3
        # 子弹设置
        self.bullet_speed_factor = 20
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_allowed = 100
        self.auto_fire = False  # 自动发射子弹
        # 外星人设置
        self.alien_speed_factor = 10
        self.fleet_drop_speed = 10
        self.fleet_direction = 1  # 右移为1 左移为-1
        self.alien_points = 50
        # 游戏节奏加速率
        self.speedup_scale = 1.2
        self.score_scale = 1.5

    def initialize_dynamic_settings(self):
        """初始化游戏变化设置"""
        self.ship_speed_factor = 30
        self.bullet_speed_factor = 20
        self.alien_speed_factor = 5
        self.alien_points = 50

        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
