import sys
from time import sleep
import pygame

from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullet
from button import Button
from alien import Alien


class AlienInvasion:
    """Загальний клас що керує поведінкую і ресурсами гри"""

    def __init__(self):
        """iніціалізація гри"""
        pygame.init()
        self.settings = Settings()

        # Запуск у пiв екран
        self.screen = pygame.display.set_mode((
            self.settings.screen_width,
            self.settings.screen_height
        ))

        # Запуск у повний екран
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption('Alien Invasion')
        pygame.display.set_icon(self.settings.bg_image)

        # Створити екземпляр статистики та табло рахунку
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Art button Play
        self.play_button = Button(self, "Play")

        # Задати колір фону
        # self.bd_color = (230, 230, 230)

    def run_game(self):
        '''Розпочати головний цикл гри'''

        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_alien()
            self._update_screen()

    def _check_events(self):
        """Слідкувати та реагуватиза подіями миші і клавітури"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Розпочати гру після натиску на кнопку"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Аналювати статистику i налаштування швидкості
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Видалити лишні кулі і інопл
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель
            self._create_fleet()
            self.ship.center_ship()

            # Приховати курсив
            pygame.mouse.set_visible(False)

    def _start_play_button(self):
        """Розпочати гру після натиску на кнопку Enter"""
        if not self.stats.game_active:
            # Аналювати статистику i налаштування швидкості
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


            # Видалити лишні кулі і інопл
            self.aliens.empty()
            self.bullets.empty()

            # Створити новий флот та відцентрувати корабель
            self._create_fleet()
            self.ship.center_ship()

            # Приховати курсив
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        """Реагувати на натискання клавіші"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_RETURN:
            self._start_play_button()
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """Реагувати коли відпістив клавішу"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False

    def _fire_bullet(self):
        """Створити нову кулю та додати до групи"""
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Оновити позицію кулі і видалити старі """
        # Оновити позицію
        self.bullets.update()

        # Видаляти кулі які вийшли за екран з групи
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Реакція на зіткнення кль"""
        # Перевіряти чи котрась з куль не влучила в прибульця
        # якщо влучила то видалити і кулю і чужака
        # -- groupcollide групове зіткнення
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()


        # Поповнити флот
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Показати рівні
            self.stats.level += 1
            self.sb.prep_level()

    def _update_alien(self):
        '''перевірити чи флот не на краю екрана
        тоді оновити позиції всіх прибульців'''
        self._check_fleet_edges()
        self.aliens.update()

        # Шукати зіткнення інопленетяна з кораблем
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Шукати зіткнення інопленетяна з bottom screen
        self._check_aliens_bottom()

    def _create_fleet(self):
        """Створити флот прибульців"""
        # Сворити прибулців в ряд з відстанню між кожним по ширині одого прибульця
        alien = Alien(self)
        alien_height, alien_width = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Визначити, якв кількість рядів поміститься на екран
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Створити флот з рядами alien
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                # Створити прибульця і поставити його в ряд до групи
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Створити прибульця і поставити в ряд"""
        alien = Alien(self)
        alien_height, alien_width = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """Реагувати якшо прибулиць доторкнувся края екрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Спуск всого флоту та зміна напрямку"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Реагувати на зіткнення корабля"""
        if self.stats.ships_left >= 2:
            # Зменшити ships_left та оновити табло
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Видалити кулі і інопл
            self.aliens.empty()
            self.bullets.empty()
            # Створити новий флот та відцентрувати корабель
            self._create_fleet()
            self.ship.center_ship()
            # Пауза
            sleep(0.5)
        else:
            self.sb.prep_ships()
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Перівітити чи aliens dont tach bottom screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Зреагувати як до зіткнення корабля
                self._ship_hit()
                break

    def _update_screen(self):
        """Оновити нанаово зображення ы перемкнутися на новий екран"""
        # фон просто кольору
        # self.screen.fill(self.settings.bd_color)

        # фон зображення космосу
        self.screen.blit(self.settings.bg_image, [0, 0])

        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Намалювати рахунок
        self.sb.show_score()

        # Намалювати кнопку якщо гра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Показати останій елемен
        pygame.display.flip()


if __name__ == '__main__':
    # Сворити екземпляр гри і запуск
    ai = AlienInvasion()
    ai.run_game()
