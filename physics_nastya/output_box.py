import pygame
from tkinter import *
from tkinter import messagebox
COLOR_INACTIVE = (60, 60, 60)
COLOR_ACTIVE = (150, 150, 150)
TEXT_COLOR_INACTIVE = (0, 0, 0)

class OutputBox:
    def __init__(self, pos, size, font, text='', title='', ok=None):
        self.box_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.title_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.title = title
        self.color = COLOR_INACTIVE
        self.title_color = (0, 0, 0)
        self.text_color = TEXT_COLOR_INACTIVE
        self.text = text
        self.FONT = pygame.font.SysFont('corbel', 3 * int(size[1]) // 5)
        self.font = font
        self.txt_surface = self.FONT.render(text, True, self.text_color)
        self.title_surface = self.font.render(title, True, self.title_color)
        self.title_width = max(150, self.title_surface.get_width())
        self.title_rect.width = self.title_width
        self.active = False

        self.ok = ok

        self.box_rect.move_ip(self.title_width, 0)
        #self.rect = self.box_rect.union(self.title_rect)

        self.flag = False


    def update(self):
        # Resize the box if the text is too long.
        self.txt_surface = self.FONT.render(self.text, True, self.text_color)
        width = max(50, self.txt_surface.get_width() + 20)
        self.box_rect.width = width

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), self.box_rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.box_rect.x+5, self.box_rect.y+5))
        screen.blit(self.title_surface, (self.title_rect.x + 5, self.title_rect.y + 5))

    def set_text(self, text):
        self.text = text
        self.update()

