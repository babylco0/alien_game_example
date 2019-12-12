
class GameStats:
    """跟踪游戏的统计信息"""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.ships_left = ai_settings.ship_limit
        self.score = 0
        self.high_score = 0
        self.level = 1
        self.reset_stats()
        # 默认游戏未开始
        self.game_active = False

    def reset_stats(self):
        """初始化游戏统计信息"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
