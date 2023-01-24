class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        # Start game in activ stane
        self.game_active = False

        # рекорд не анулювати і витягнути з файлу
        filename = 'best_score.txt'
        with open(filename) as f:
            content = f.read()
            x = content.rsplit()
        self.high_score = int(x[0])

        self.reset_stats()

    def reset_stats(self):
        """Статистика що може змінюватися під час гри"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
