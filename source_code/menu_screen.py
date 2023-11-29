import pygame
import sys
from button import myButton


class MenuScreen:

    def __init__(self, app, window_size):
        self.width, self.length = window_size
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, self.length//30)
        self.middle_font = pygame.font.SysFont(self.font, self.length//27, bold=True)
        self.big_font = pygame.font.SysFont(self.font, self.length//22)

        self.buttons = []
        self.msu_logo = []
        self.cmc_logo = []
        self.strings_surfaces = []
        self.strings = []

        self.create_menu_items(app)

    def _update_screen(self):
        self.screen.fill(self.bg_color)

        for index, surface in enumerate(self.strings_surfaces):
            self.screen.blit(surface, self.positions[index])

        self.screen.blit(self.cmc_logo, (8.5 * self.width // 10, self.length // 10))
        self.screen.blit(self.msu_logo, (0.5 * self.width // 10, self.length // 10))
        for button in self.buttons:
            button.draw_button()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._on_button_click(mouse_position)

    def _on_button_click(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.demo_screen
                if index == 1:
                    self.app.active_screen = self.app.theory_screen
                if index == 2:
                    self.app.active_screen = self.app.authors_screen
                elif index == 3:
                    sys.exit()

    def create_menu_items(self, app):
        msu_name = "Московский Государственный Университет им. М.В. Ломоносова"
        faculty_name = "Факультет вычислительной математики и кибернетики"
        demonstration_label = "Компьютерная демонстрация по курсу"
        subject_name = "Статистическая физика"
        demonstration_name = "Влияние взаимодействия частиц на одномерные"
        demonstration_name_2 = "случайные структуры"

        self.strings = [msu_name, faculty_name, demonstration_label, subject_name, demonstration_name,
                        demonstration_name_2]

        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(self.middle_font.render(string, True, (0, 0, 0)))
            elif index < 4:
                self.strings_surfaces.append(self.little_font.render(string, True, (0, 0, 0)))
            else:
                self.strings_surfaces.append(self.big_font.render(string, True, (0, 0, 0)))

        self.positions = []
        for index, surface in enumerate(self.strings_surfaces):
            surf_width = surface.get_width()
            x = self.width // 2 - surf_width // 2
            y = self.length // 10 + (self.length // 18) * index
            self.positions.append((x, y))

        self.cmc_logo = pygame.transform.scale(pygame.image.load("sources/cmc_logo.jpg").convert(),
                                                (self.width // 10, self.width // 10))
        self.msu_logo = pygame.transform.scale(pygame.image.load("sources/ff_logo.jpg").convert(),
                                                (self.width // 10, self.width // 10))

        button_length = self.width // 5
        button_x = self.width // 2 - button_length // 2
        button_y = self.length // 2
        button_width = self.length // 16

        button_names = ['Демонстрация', 'Теория', 'Авторы', 'Выход']

        for index, name in enumerate(button_names):
            self.buttons.append(myButton(app, name,
                                         (button_x, button_y + index * (self.length // 10)),
                                         (button_length, button_width)))

