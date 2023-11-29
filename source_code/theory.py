import pygame
import sys
from button import myButton


class TheoryScreen():
    def __init__(self, app, window_size):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.width, self.length = window_size
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, self.length // 30)
        self.middle_font = pygame.font.SysFont(self.font, self.length // 27, bold=True)
        self.big_font = pygame.font.SysFont(self.font, self.length // 22)

        self.buttons = []
        self.pictures_positions = []
        self.pictures = []
        self.text_positions = []
        self.strings_surfaces = []
        self.strings = []

        self.create_menu_items(app)

    def _update_screen(self):
        self.screen.fill(self.bg_color)
        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.text_positions[index])

        for index, picture in enumerate(self.pictures):
            self.screen.blit(picture, self.pictures_positions[index])

        for button in self.buttons:
            button.draw_button()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)

    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen

    def create_menu_items(self, app):
        self.strings = ["Теория"]

        self.strings_surfaces = []
        self.strings_surfaces.append(self.middle_font.render(self.strings[0], True, (0, 0, 0)))

        x = (self.width // 4) + (self.width // 19)
        y = self.length // 10 + (self.length // 18)
        self.text_positions.append((x, y))

        self.pictures = [
            pygame.image.load("sources/2021-12-09_001.jpg"),
            pygame.image.load("sources/2021-12-09_002.jpg")]

        self.pictures_positions = [(0, 0), (0, 1000)]

        button_size = (self.width // 12, self.length // 12)
        button_pos = (10 * self.width // 12, 10 * self.length // 12)

        self.buttons = [myButton(app, "Назад", button_pos, button_size)]