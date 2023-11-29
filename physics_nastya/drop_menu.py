import pygame
import pygame.font

class DropDownMenu:
    def __init__(self, pos, size, options, font):
        self.pos = list(pos)
        self.bg_color = (240, 240, 240)
        self.line_color = (80, 80, 80)
        self.width = size[0]
        self.options = options
        self.expanded = False
        self.height = size[1]
        self.cur_option = self.options[0]
        self.title_font = font
        title = 'форма\nпотенциала'
        self.title_surface = self.title_font.render(title, True, (0, 0, 0))
        self.title_width = max(140, self.title_surface.get_width())
        self.title_rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.title_rect.width = self.title_width
        self.pos[0] += self.title_width
        self.lw = 2


    def draw(self, screen):
        font = pygame.font.SysFont('corbel', 3 * self.height // 5)
        pygame.draw.rect(screen, self.bg_color, (self.pos[0], self.pos[1], self.width, self.height))
        pygame.draw.line(screen, self.line_color, (self.pos[0], self.pos[1] + self.height),
                         (self.pos[0] + self.width - 1, self.pos[1] + self.height), self.lw)
        screen.blit(self.title_surface, (self.title_rect.x + 5, self.title_rect.y + 5))

        if self.expanded:
            for i in range(len(self.options)):
                pygame.draw.rect(screen, self.bg_color,
                                 (self.pos[0], self.pos[1] + self.height * (i + 1) + self.lw, self.width, self.height))
                # pygame.draw.line(screen, (0, 0, 0), (self.pos[0], self.pos[1] + self.height * (i + 1) + self.height),
                #                 (self.pos[0] + self.width, self.pos[1] + self.height * (i + 1) + self.height), 2)
                text = font.render(self.options[i], True, (0, 0, 0))
                screen.blit(text, (self.pos[0] + self.height//5, self.pos[1] + self.height * (i + 1) + self.height//5))

            for i in range(len(self.options)):
                pygame.draw.line(screen, self.line_color, (self.pos[0], self.pos[1] + self.height * (i + 1) + self.height),
                                (self.pos[0] + self.width - 1, self.pos[1] + self.height * (i + 1) + self.height), self.lw)
        else:
            text = font.render(self.cur_option, True, (0, 0, 0))
            screen.blit(text, (self.pos[0] + self.height//5, self.pos[1] + self.height//5))

    def expand(self):
        self.expanded = not self.expanded

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.pos[0] <= event.pos[0] <= self.pos[0] + self.width and\
                    self.pos[1] <= event.pos[1] <= self.pos[1] + self.height:
                self.expand()
            elif self.expanded:
                for i in range(len(self.options)):
                    if self.pos[0] <= event.pos[0] <= self.pos[0] + self.width and \
                            self.pos[1] + self.height * (i + 1) <= event.pos[1] <= self.pos[1] + self.height * (i + 1) + self.height:
                        self.cur_option = self.options[i]
                        self.expand()

    def get_option(self):
        return self.cur_option
