import pygame
from tkinter import *
from tkinter import messagebox
COLOR_INACTIVE = (60, 60, 60)
COLOR_ACTIVE = (150, 150, 150)
TEXT_COLOR_INACTIVE = (0, 0, 0)

class InputBox:
    def __init__(self, pos, size, font, text='', title='', ok=None, maxwidth=50):
        self.box_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.title_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.title = title
        self.color = COLOR_INACTIVE
        self.title_color = (0, 0, 0)
        self.text_color = TEXT_COLOR_INACTIVE
        self.text = text
        if text.isdigit():
            self.contents = int(text)
        else:
            self.contents = 50

        self.font = font
        self.FONT = pygame.font.SysFont('corbel', 3 * int(size[1]) // 5)

        self.txt_surface = self.FONT.render(text, True, self.text_color)
        self.title_surface = self.font.render(title, True, self.title_color)
        self.title_width = max(150, self.title_surface.get_width())
        self.title_rect.width = self.title_width
        self.active = False

        self.ok = ok

        self.box_rect.move_ip(self.title_width, 0)
        #self.rect = self.box_rect.union(self.title_rect)

        self.flag = False

        self.maxwidth = maxwidth


    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.box_rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                if not self.active:
                    self.flag = True
            else:
                if self.active:
                    self.flag = True
                self.active = False

            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
            self.text_color = COLOR_ACTIVE if self.active else TEXT_COLOR_INACTIVE
            if self.active:
                self.text = ''
                self.txt_surface = self.FONT.render(self.text, True, self.text_color)

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.color = COLOR_INACTIVE
                    self.text_color = TEXT_COLOR_INACTIVE

                    self._handle_error()

                elif event.key == pygame.K_BACKSPACE:
                    if self.text:
                        self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.text_color)

        # if situation has just changed
        if self.flag:
            self._handle_error()
            self.txt_surface = self.FONT.render(self.text, True, self.text_color)
            self.flag = False


    def update(self):
        # Resize the box if the text is too long.
        width = max(self.maxwidth, self.txt_surface.get_width()+10)
        #self.box_rect.width = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.box_rect.x+5, self.box_rect.y+5))
        screen.blit(self.title_surface, (self.title_rect.x + 5, self.title_rect.y + 5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.box_rect, 2)

    def get_contents(self):
        return self.contents

    def set_text(self, text):
        self.text = text

    def _handle_error(self):
        if not self.text:
            self.text = str(self.contents)
        if self.ok:
            error = self.ok(self.text)
            if error:
                self.text = str(self.contents)
                self._display_error(error)
            else:
                self.contents = int(self.text)
        else:
            self.contents = int(self.text)

    def _display_error(self, error):
        Tk().wm_withdraw()  # to hide the main window
        messagebox.showerror('Input error', error)
