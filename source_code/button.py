import pygame.font

class myButton():
    
    def __init__(self, app, msg, position, button_size, radius=0, lines=1, font='corbel'):
        """Инициализирует атрибуты кнопки."""
        self.screen = app.screen
        self.screen_rect = self.screen.get_rect()
        self.font = font
        # Назначение размеров и свойств кнопок.
        self.width, self.height = button_size
        self.button_color = (240, 240, 240)
        self.text_color = (0, 0, 0)
        self.radius = radius
        self.font = pygame.font.SysFont(self.font, 7 * self.height // 10 // lines)

        # Построение объекта rect кнопки и выравнивание по центру экрана.
        self.rect = pygame.Rect(*position, self.width, self.height)
        
        # Сообщение кнопки создается только один раз.
        self._prep_msg(msg)
    
    def _prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color,
                                            self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw_button(self):
        # Отображение пустой кнопки и вывод сообщения.
        pygame.draw.rect(self.screen, self.button_color, self.rect, border_radius=self.radius)
        pygame.draw.rect(self.screen, self.text_color, self.rect, 1, border_radius=self.radius)
        #self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)