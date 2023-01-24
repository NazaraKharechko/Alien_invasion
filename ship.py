import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    """Клас для керуваня літака"""

    def __init__(self, ai_game):
        """Початкова позиція і ініціалізація"""
        super().__init__()

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Завантажити зображення та отримати його rect
        self.image = pygame.image.load('images/death_star.png')
        self.rect = self.image.get_rect()

        # Створювати кожен корабе внизу екрана по центрі
        self.rect.midbottom = self.screen_rect.midbottom

        # Зберегти значення почиції корабля ро горизинталі не ціле число == 1.5
        self.x = float(self.rect.x)

        # Зберегти значення почиції корабля ро вертикалі не ціле число == 1.5
        self.y = float(self.rect.y)

        # Індикатор руху в право
        self.moving_right = False

        # Індикатор руху в ліво
        self.moving_left = False

        # Індикатор руху в низ
        self.moving_down = False

        # Індикатор руху в верх
        self.moving_up = False

    def update(self):
        """Оновити поточну позицію коробля на основі індикатиру руху"""

        # Оновити значення ship.x
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed

        #  Оновити обєкт rect з self.x
        self.rect.x = self.x

        #  Оновити обєкт rect з self.y
        self.rect.y = self.y

    def blitme(self):
        """Намалювати корабель у поточному розташувані"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """відцентрувати ship on screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

