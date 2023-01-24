import pygame
from pygame.sprite import Sprite

from ship import Ship


class Bullet(Sprite):
    """Клос для керування куль випущенишх від корабля"""

    def __init__(self, ai_game):
        """Створити обєкт Bullet у поточній позиції корабля"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color
        self.ship = Ship(self)

        # Cтворити рект кулі у 0, 0 та затати позицію відносно корабля

        # Куля з зображення
        self.image = pygame.image.load('images/shoot.png')
        self.rect = self.image.get_rect()

        # Куля проста риска
        # self.rect = pygame.Rect(0, 0, self.settings.bullet_width, self.settings.bullet_height)

        # Позиція відносно корабля
        self.rect.midtop = ai_game.ship.rect.midtop

        # Позиція кулі не ціле число
        self.y = float(self.rect.y)

        # Позиція кулі не ціле число
        self.x = float(self.rect.x)

    def update(self):
        """Посунути кулю в гору"""
        # Оновити десяткову позицію кулі
        self.y -= self.settings.bullet_speed

        # Оновити позицію rect
        self.rect.y = self.y

    def draw_bullet(self):
        """Намалювати кулю на екрані"""
        self.screen.blit(self.image, self.rect)
        # Куля проста риска
        # pygame.draw.rect(self.screen, self.color, self.rect)
