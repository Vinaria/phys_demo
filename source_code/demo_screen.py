import random
from random import randrange
from time import sleep

import pygame
import sys

import matplotlib
from matplotlib import pyplot as plt

from button import myButton
from particle import Particle
from input_box import InputBox
from statistics import *
from statistics import Flat
from drop_menu import DropDownMenu
from plot import Plot
import scipy.stats as stats
from diapasons import *
from screenshot import *
from output_box import OutputBox

#matplotlib.use('module://pygame_matplotlib.backend_pygame')
matplotlib.use("Agg")


class DemoScreen():
    def __init__(self, app, window_size):
        self.app = app
        self.screen = app.screen
        self.speed = 1
        self.bg_color = (255, 255, 255)
        self.line_color = (100, 100, 100)
        self.font = 'arial'
        self.width, self.length = window_size
        self.tick = 0
        self.stop_flag = True
        self.particle_size = self.length // 110
        self.line_width = 2

        self.little_font = pygame.font.SysFont(self.font, self.length // 32)
        self.middle_font = pygame.font.SysFont(self.font, self.length // 27)
        self.middle_font_bold = pygame.font.SysFont(self.font, self.length // 27, bold=True)
        self.big_font = pygame.font.SysFont(self.font, self.length // 22)

        # параметры линии
        self.circle_radius = self.length // 24
        # self.circle_center = (11 * self.width // 12, self.line_height + self.circle_radius)
        self.line_height = self.length // 24
        self.line_length = 10 * self.width // 12

        width1 = self.width // 24
        width2 = 4 * self.width // 24 + self.width // 6
        width3 = 3 * self.width // 5

        height11 = self.length // 12 + 6 * self.circle_radius + self.length // 24
        height21 = self.length // 24 + 6 * self.circle_radius + self.length // 24
        height32 = height11 + self.length // 2.5

        param_height = self.length // 16
        param_hm = ((self.length - height11) - 6*param_height) / 7

        # self.graphics_pos = (0, 0)
        #
        # self.graphics_names = ['Cкорость', 'Смещение', 'Кинетическая энергия', 'Ускорение']
        #
        # self.graph_size = (self.width // 4, self.length // 8)

        button_back = { 'size': (self.width // 15, self.length // 17),
                        'pos': (22 * self.width // 24, 22 * self.length // 24)}

        button_stop = {'size': (self.width // 6, self.length // 19),
                       'pos': (width3 * 1.03, 21 * self.length // 24)}

        button_start = {'size': (self.width // 8, self.length // 19),
                        'pos': (width3 * 1.03, 19 * self.length // 24)}

        button_photo = {'size': (self.width // 15, self.length // 17),
                        'pos': (20 * self.width // 24, 22 * self.length // 24)}

        input_box_temp = {'size': (3 * self.width // 22, param_height),
                          'pos': (width1, height11 + param_hm + param_height)}

        input_box_width = {'size': (3 * self.width // 22, param_height),
                           'pos': (width1, height11 + 2 * param_hm + 2 * param_height)}

        input_box_depth = {'size': (3 * self.width // 22, param_height),
                           'pos': (width1, height11 + 3 * param_hm + 3 * param_height)}

        input_box_jump = {'size': (3 * self.width // 22, param_height),
                           'pos': (width1, height11 + 4 * param_hm + 4 * param_height)}

        input_box_size = {'size': (3 * self.width // 22, param_height),
                          'pos': (width1, height11 + 5 * param_hm + 5 * param_height)}

        output_box_entropy = {'size': (1.5 * self.width // 20, 1.2 * param_height),
                              'pos': (self.width - 1.5 * self.width // 20 * 3, height32)}

        menu = {'size': (self.width // 5, param_height),
                'pos': (width1, height11),
                'options': ['плоский', 'параболический', 'Леннарда-Джонса']}

        width_input = InputBox(input_box_width['pos'], input_box_width['size'], self.little_font,
                               '50', 'ширина\nямы', width_diap)
        temp_input = InputBox(input_box_temp['pos'], input_box_temp['size'], self.little_font,
                              '50', 'температура', temp_diap)
        depth_input = InputBox(input_box_depth['pos'], input_box_depth['size'], self.little_font,
                               '50', 'глубина\nямы', depth_diap)
        jump_input = InputBox(input_box_jump['pos'], input_box_jump['size'], self.little_font,
                              '25', 'расстояние\nмежду ямами', jump_diap)
        size_input = InputBox(input_box_size['pos'], input_box_size['size'], self.little_font,
                              str(self.particle_size), 'размер\nчастицы', size_diap)

        self.entropy_output = OutputBox(output_box_entropy['pos'], output_box_entropy['size'], self.middle_font,
                                        '', 'Энтропия')

        self.buttons = [myButton(app, "Назад", button_back['pos'], button_back['size']),
                        myButton(app, "Следующая частица", button_stop['pos'], button_stop['size'],
                                 radius=10, lines=1, font=self.font),
                        myButton(app, "Старт", button_start['pos'], button_start['size'],
                                 radius=10, lines=1, font=self.font),
                        myButton(app, "Фото", button_photo['pos'], button_photo['size'])
                        ]
        self.boxes = [temp_input, width_input, depth_input, jump_input, size_input, self.entropy_output]

        self.menu = DropDownMenu(menu['pos'], menu['size'], options=menu['options'], font=self.little_font)

        self.lines = [
            {'height': self.length // 24,
             'start': (self.width // 12, self.line_height),
             'end': (self.width // 12 + self.line_length, self.line_height)},
            {'height': self.length // 24 + 2 * self.circle_radius,
             'start': (self.width // 12, self.line_height + 2 * self.circle_radius),
             'end': (self.width // 12 + self.line_length, self.line_height + 2 * self.circle_radius)},
            {'height': self.length // 24 + 4 * self.circle_radius,
             'start': (self.width // 12, self.line_height + 4 * self.circle_radius),
             'end': (self.width // 12 + self.line_length, self.line_height + 4 * self.circle_radius)},
            {'height': self.length // 24 + 6 * self.circle_radius,
             'start': (self.width // 12, self.line_height + 6 * self.circle_radius),
             'end': (self.width // 12 + self.line_length, self.line_height + 6 * self.circle_radius)}
        ]

        self.circles = [(11 * self.width // 12, self.line_height + self.circle_radius),
                        (self.width // 12, self.line_height + 3 * self.circle_radius),
                        (11 * self.width // 12, self.line_height + 5 * self.circle_radius)]

        self.line_start = (self.width // 12, self.line_height)
        self.line_end = (11 * self.width // 12, self.line_height)


        self.second_line_height = self.line_height + 2 * self.circle_radius
        self.second_line_start = (self.width // 12, self.second_line_height)
        self.second_line_end = (11 * self.width // 12, self.second_line_height)

        # Создаем графики
        self.periodicity_plot = Plot(self.app, position=(width3, height21),
                                     size=(self.width // 2.5, self.length // 2.5),
                                     ylim=(0, 1.1),
                                     title='Коэффициент периодичности')

        self.potential_plot = Plot(self.app, position=(width2, height21),
                                   size=((width3 * 1.03 - width2) * 1, self.length // 1.5),
                                   xlim=(-10, 210),
                                   ylim=(-210, 10),
                                   title='Форма потенциала')

        #параметры демонстрации
        self._set_to_start()


    def _update_screen(self):
        self.tick = (self.tick + 1) % 4
        self.screen.fill(self.bg_color)

        pt_name = self.menu.get_option()
        temp = float(self.boxes[0].get_contents())
        well_size = float(self.boxes[1].get_contents())
        depth = float(self.boxes[2].get_contents())
        jump = float(self.boxes[3].get_contents())
        size = int(self.boxes[4].get_contents())
        Particle.set_size(size)
        if pt_name == 'плоский':
            graph_potential = Flat(interval=[jump, well_size + jump], depth=depth)
        elif pt_name == 'параболический':
            graph_potential = Parabola(interval=[jump, well_size + jump], depth=depth)
        elif pt_name == 'Леннарда-Джонса':
            graph_potential = LennardJones(interval=[jump, well_size + jump], depth=depth)

        self.entropy_val = Boltzmann(temp=temp, potential=graph_potential).entropy()


        for each in self.lines:
            pygame.draw.line(self.screen, self.line_color, each['start'], each['end'], self.line_width)


        for i in range(len(self.circles)):
            pygame.draw.circle(
                surface=self.screen,
                color=self.line_color,  # Color in RGB Fashion
                center=self.circles[i],  # Center
                radius=self.circle_radius,  # Radius
                width=self.line_width,
                draw_top_right=(i % 2 == 0),
                draw_bottom_right=(i % 2 == 0),
                draw_top_left=(i % 2 == 1),
                draw_bottom_left=(i % 2 == 1),
            )

        for button in self.buttons:
            button.draw_button()

        for box in self.boxes:
            box.update()
            box.draw(self.screen)

        self.menu.draw(self.screen)

        # Рисуем графики
        self.periodicity_plot.show(y=self.periodicity_vals, x=np.arange(1, len(self.periodicity_vals) + 1))
        self.entropy_output.set_text("{:.3f}".format(self.entropy_val))

        x_vals = np.arange((well_size + jump + 1) * 10) * 0.1
        np.append(x_vals, [jump - 1, well_size + jump + 1])
        y_vals = [graph_potential.f(x) for x in x_vals]
        self.potential_plot.show(y=y_vals, x=x_vals)


        if not self.stop_flag:
            self.cur_particle.move()
            self.cur_particle.show(self.screen)

        for particle in self.particles:
            particle.show(self.screen)

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                self._check_buttons(mouse_position)
            for box in self.boxes[:-1]:
                box.handle_event(event)

            self.menu.handle_event(event)


    def _check_buttons(self, mouse_position):
        for index, button in enumerate(self.buttons):
            if button.rect.collidepoint(mouse_position):
                if index == 0:
                    self.app.active_screen = self.app.menu_screen
                elif index == 1:
                    if not self.stop_flag:
                        self._next_step()
                elif index == 2:
                    self.stop_flag = False
                    self._set_to_start()
                #elif index == 3:
                    #screenshot()

    def _next_step(self):
        self.particles.append(self.cur_particle)
        self.cur_particle = self.cur_particle.create_next(self.jump_dist)
        if self.cur_particle:
            x_vals = Particle.get_intervals()
            self.periodicity_vals.append(periodicity_coef(x_vals))
            self.changed = True
        else:
            self.stop_flag = True

    def _set_to_start(self):
        self.periodicity_plot.delete_y_vals()
        # параметры демонстрации
        self.temp = float(self.boxes[0].get_contents())
        self.well_size = float(self.boxes[1].get_contents())
        self.depth = float(self.boxes[2].get_contents())
        self.jump_dist = float(self.boxes[3].get_contents())
        self.particle_size = int(self.boxes[4].get_contents())
        pt_name = self.menu.get_option()

        self.cur_interval = [self.jump_dist, self.well_size + self.jump_dist]

        if pt_name == 'плоский':
            self.potential = Flat(interval=self.cur_interval, depth=self.depth)
        elif pt_name == 'параболический':
            self.potential = Parabola(interval=self.cur_interval, depth=self.depth)
        elif pt_name == 'Леннарда-Джонса':
            self.potential = LennardJones(interval=self.cur_interval, depth=self.depth)

        self.dist = Boltzmann(temp=self.temp, potential=self.potential)
        self.pdf = self.dist.pdf
        self.entropy_val = self.dist.entropy()
        self.dispersion_val = self.dist.get_dispersion()

        self.particles = []
        Particle.positions = []
        self.particle_y = self.line_height

        if not self.stop_flag:
            self.cur_particle = Particle(interval=[0, self.well_size],
                                         r=self.particle_size,
                                         dist=self.dist,
                                         y=[line['height'] for line in self.lines],
                                         length=self.line_length,
                                         start=self.line_start[0])


        self.periodicity_vals = []

        self.changed = False

        self.entropy_output.set_text("{:.3f}".format(self.entropy_val))
        self.periodicity_plot.add_y_value(self.dist.periodicity_lim())


