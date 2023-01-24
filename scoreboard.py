import pygame.font
from pygame.sprite import Group

from ship import Ship


class Scoreboard:
    """Клас що виводить рахунок"""

    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Settings text
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # піднотовка зображення з початковим рахунком
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Перетворити рахунок на зображення"""
        rounder_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounder_score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bd_color)

        # Показати рахунок у верньому правому куті
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Згенерувати рекорд у зображення"""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "Best: {:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bd_color)

        # Відцентрувати зверху
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Перетворити рівні на image"""
        level_str = 'lv: -_+ ' + str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bd_color)

        # Розташувати рівні пд рахунком
        self.level_rect = self.level_image.get_rect()
        self.level_rect.centerx = self.high_score_rect.right + 200
        self.level_rect.top = self.score_rect.top

    def prep_ships(self):
        """показує скільки кораблів"""
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            ship.image = pygame.image.load('images/death_star_mini.png')

            self.ships.add(ship)

    def show_score(self):
        """Показати рахунок і рівні and ships"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Перевірити чи не встановлено нового рекорду"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

            filename = 'best_score.txt'

            with open(filename, 'w') as f:
                f.write(str(self.stats.high_score))
