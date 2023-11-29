import pygame
from statistics import *
import numpy as np


class Particle:

    positions = []
    screen_positions = []
    probabilities = []
    radius = 5

    def __init__(self, interval, r, dist, y, length, start):
        Particle.radius = r
        self.dist = dist
        self.index = len(Particle.positions)
        self.line_length = length

        self.interval = interval

        self.width = self.interval[1] - self.interval[0]
        self.y = y

        self.line_start = start

        self.x = self.dist.draw_random() * 2 + self.interval[0]
        Particle.screen_positions.append(self.to_screen_position())
        Particle.positions.append(self.x)
        Particle.probabilities.append(self.dist.pdf(self.x // 2))

    def show(self, screen):
        pygame.draw.circle(screen, (0, 0, 0), self.to_screen_position(), Particle.radius)

    def move(self):
        self.x = self.x = self.dist.draw_random() * 2 + self.interval[0]
        Particle.screen_positions[self.index] = self.to_screen_position()
        Particle.positions[self.index] = self.x
        Particle.probabilities.append(self.dist.pdf(self.x // 2))

    def get_x(self):
        return self.x

    def to_screen_position(self):
        i = int(self.x // self.line_length)
        if i % 2 == 0:
            screen_x = self.x % self.line_length
        else:
            screen_x = self.line_length - self.x % self.line_length

        if i > len(self.y) - 1:
            screen_x = self.line_length * len(self.y)
            i = len(self.y) - 1

        screen_x += self.line_start

        return [screen_x, self.y[i]]

    def create_next(self, jump_dist):
        if self.x + jump_dist + self.width > self.line_length * len(self.y):
            return 0

        new_interval = [self.x + jump_dist, self.x + jump_dist + self.width]
        new_particle = Particle(interval=new_interval, r=Particle.radius, dist=self.dist, y=self.y, length=self.line_length, start=self.line_start)
        return new_particle

    @staticmethod
    def set_size(r: int):
        Particle.radius = r

    @staticmethod
    def get_intervals():
        return np.diff(Particle.positions)

    @staticmethod
    def convert_positions(length):
        new_positions = []
        y = np.unique(np.array(Particle.positions)[:, 1])
        start = np.min(np.array(Particle.positions)[:, 0])

        for pos in Particle.positions:
            i = np.where(y == pos[1])[0][0]
            if i % 2 == 1:
                new_pos = (length - (pos[0] - start)) + length * i
            else:
                new_pos = (pos[0] - start) + length * i
            new_positions.append(new_pos)
        return new_positions


