import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
import seaborn as sns
import pygame
import matplotlib.backends.backend_agg as agg
import pylab


class Plot:

    number = 0

    def __init__(self, app, position, size, title='', xlim=None, ylim=(0, 100), directory = '', dpi=97):

        self.font = 'corbel'

        # Назначение размеров и свойств
        self.width, self.height = size
        self.plot_color = (0, 0, 0)
        self.title = title
        self.file_name = directory + str(Plot.number) + '.png'
        self.xlim = xlim
        self.ylim = ylim
        self.pos = position
        self.dpi = dpi
        self.screen = app.screen
        self.extra_y_vals = []
        self.extra_plot = []

        Plot.number += 1

    def add_y_value(self, val):
        self.extra_y_vals = [val]

    def add_plot(self, x, y):
        self.extra_plot = [[x, y]]

    def delete_y_vals(self):
        self.extra_y_vals = []

    def delete_extra_plot(self):
        self.extra_plot = []

    def set_xlim(self, t):
        self.xlim = t

    def show(self, x, y):
        # #fig, ax = plt.subplots()
        # fig = plt.figure(figsize=(self.width/self.dpi, self.height/self.dpi), dpi=self.dpi)
        # #fig = plt.figure()
        # plt.plot(x, y, lw=6)
        # plt.title(self.title)
        # #fig.savefig(self.file_name, bbox_inches='tight', dpi=self.dpi)
        # #plt.close(fig)
        #
        # #img_surface = pygame.transform.scale(pygame.image.load(self.file_name), (self.width, self.height))
        # #img_surface = pygame.image.load(self.file_name)
        # fig.canvas.draw()
        # self.screen.blit(fig, self.pos)
        # plt.close(fig)

        fig = pylab.figure(figsize=[self.width/self.dpi, self.height/self.dpi],  # Inches
                           dpi=self.dpi,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        ax = fig.gca()
        ax.plot(x, y, linewidth=4, color=(0, 0, 0))
        plt.ylim(self.ylim)
        plt.xlim(self.xlim)
        plt.title(self.title, fontsize=13)

        for extra in self.extra_y_vals:
            ax.plot(x, extra * np.ones(len(y)), 'k--', linewidth=2)

        for extra in self.extra_plot:
            ax.plot(extra[0], extra[1], 'k--', linewidth=2)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()

        plt.close(fig)

        surf = pygame.image.fromstring(raw_data, size, "RGB").convert()
        self.screen.blit(surf, self.pos)



