import pygame
from menu_screen import MenuScreen
from authors_screen import AuthorsScreen
from demo_screen import DemoScreen
from theory import TheoryScreen


class App:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        window_size = (1000, 630)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        window_size = self.screen.get_size()
        self.menu_screen = MenuScreen(self, window_size)
        self.authors_screen = AuthorsScreen(self, window_size)
        self.demo_screen = DemoScreen(self, window_size)
        self.theory_screen = TheoryScreen(self, window_size)

        self.active_screen = self.menu_screen

    def run(self):
        clock = pygame.time.Clock()
        """Запуск основного цикла игры."""
        while True:
            clock.tick(30)
        # Отслеживание событий клавиатуры и мыши.
            self.active_screen._check_events()
            self.active_screen._update_screen()
            # Отображение последнего прорисованного экрана.
            pygame.display.flip()
