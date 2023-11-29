import pygame
import sys
from button import myButton


class AuthorsScreen():
    def __init__(self, app, window_size):
        self.app = app
        self.screen = app.screen
        self.bg_color = (255, 255, 255)
        self.width, self.length = window_size
        self.font = 'corbel'
        self.little_font = pygame.font.SysFont(self.font, self.length//30)
        self.middle_font = pygame.font.SysFont(self.font, self.length//27, bold=True)
        self.big_font = pygame.font.SysFont(self.font, self.length//22)

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
        self.strings = ["Московский Государственный Университет им. М.В. Ломоносова",
                        "Факультет вычислительной математики и кибернетики",
                        "Лектор: Андреев Анатолий Васильевич",
                        "Руководитель: Чичигина Ольга Александровна",
                        "Фунтикова Анастасия",
                        "Гервиц Виктория"]

        self.strings_surfaces = []
        for index, string in enumerate(self.strings):
            if index < 2:
                self.strings_surfaces.append(self.middle_font.render(string, True, (0, 0, 0)))
            else:
                self.strings_surfaces.append(self.little_font.render(string, True, (0, 0, 0)))

        for index, surface in enumerate(self.strings_surfaces[:-2]):
            surf_width = surface.get_width()
            x = self.width // 2 - surf_width // 2
            y = self.length // 10 + (self.length // 18) * index
            self.text_positions.append((x, y))

        msu_logo_pos = (0.5 * self.width // 10, self.length // 10)
        cmc_logo_pos = (8.5 * self.width // 10, self.length // 10)
        creator_1_pos = (self.width // 5, 2 * self.length // 5)
        creator_2_pos = (3 * self.width // 5, 2 * self.length // 5)

        self.text_positions.append((creator_1_pos[0],
                                    creator_1_pos[1] + 4 * self.width // 5.4 // 3 + self.length//20))
        self.text_positions.append((creator_2_pos[0] + self.width // 80,
                                    creator_2_pos[1] + 4 * self.width // 5.4 // 3 + self.length//20))

        self.pictures = [pygame.transform.scale(pygame.image.load("sources/ff_logo.jpg"),
                                                (self.width // 10, self.width // 10)),
                         pygame.transform.scale(pygame.image.load("sources/cmc_logo.jpg"),
                                                (self.width // 10, self.width // 10)),
                         pygame.transform.scale(pygame.image.load("sources/creator_1.jpg"),
                                                (self.width // 5.4, 4 * self.width // 5.4 // 3)),
                         pygame.transform.scale(pygame.image.load("sources/creator_2.jpg"),
                                                (self.width // 5.4, 4 * self.width // 5.4 // 3))]

        self.pictures_positions = [msu_logo_pos, cmc_logo_pos, creator_1_pos, creator_2_pos]

        button_size = (self.width // 15, self.length // 17)
        button_pos = (22 * self.width // 24, 22 * self.length // 24)

        self.buttons = [myButton(app, "Назад", button_pos, button_size)]
        