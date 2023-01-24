import pygame


class Settings:
    """Клас для васіх налаштувань гри"""

    def __init__(self):
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bd_color = (189, 136, 85)
        self.bg_image = pygame.image.load('images/space.png')

        # Налаштування корабля
        self.ship_limit = 3

        # Налаштування кулі
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (223, 12, 80)
        self.bullet_allowed = 5

        # Налаштування прибульця
        self.fleet_drop_speed = 10

        # Як буде збільшуватися ціна прибцльця
        self.score_scale = 1.5

        self.speed_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Ініціалізація зміних налаштувань"""
        self.ship_speed = 2
        self.bullet_speed = 1.8
        self.alien_speed = 1.0

        # fleet_direction рух в право -1 -- рух в ліво 1
        self.fleet_direction = 1

        # Отримання балів
        self.alien_points = 50

    def increase_speed(self):
        """Збільшити налаштування швидкості i ціни прибулбця"""
        self.ship_speed *= self.speed_scale
        self.bullet_speed *= self.speed_scale
        self.alien_speed *= self.speed_scale
        self.alien_points = int(self.alien_points * self.score_scale)


    
