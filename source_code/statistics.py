import numpy as np
import scipy
from scipy import constants
import scipy.integrate as integrate


class Potential:
    def __init__(self, interval, depth):
        self.interval = interval
        self.easy_interval = np.array(interval) * 0.5
        self.depth = depth

    def get_interval(self):
        return self.easy_interval

    def f(self, x) -> int:
        pass

    def linspace(self, n: int):
        k = (self.interval[1] - self.interval[0]) // 2
        return np.linspace(self.interval[0] - k, self.interval[1] + k, n)


class Flat(Potential):
    def f(self, x: int):
        if self.interval[0] < x < self.interval[1]:
            return -self.depth

        if x in self.interval:
            return 0

        return np.inf

    def easy_f(self, x: int):
        if self.easy_interval[0] < x < self.easy_interval[1]:
            return -self.depth

        if x in self.easy_interval:
            return 0

        return np.inf


class LennardJones(Potential):
    def f(self, x: int):
        n = 3
        rmin = self.interval[1] - self.interval[0]
        mark = rmin * 2 ** (-1 / n)
        r = x + mark - self.interval[0]
        length = self.interval[1] + mark
        height = (rmin/length)**(2*n) - 2 * (rmin/length)**n
        res = (rmin/r)**(2*n) - 2 * (rmin/r)**n - height
        res = res / (1 + height) * self.depth
        if res > 0:
            return np.inf

        return res

    def easy_f(self, x: int):
        n = 3
        rmin = self.easy_interval[1] - self.easy_interval[0]
        mark = rmin * 2 ** (-1 / n)
        r = x + mark - self.easy_interval[0]
        length = self.easy_interval[1] + mark
        res = ((rmin/r)**(2*n) - 2 * (rmin/r)**n) * self.depth - ((rmin/length)**(2*n) - 2 * (rmin/length)**n) * self.depth
        if res > 0:
            return np.inf

        return res


class Parabola(Potential):
    def f(self, x: int):
        if self.interval[0] < x < self.interval[1]:
            d = self.interval[1] - self.interval[0]
            return 4*self.depth / d**2 * (x - d/2 - self.interval[0])**2 - self.depth

        return np.inf

    def easy_f(self, x: int):
        if self.easy_interval[0] < x < self.easy_interval[1]:
            d = self.easy_interval[1] - self.easy_interval[0]
            return 4 * self.depth / d ** 2 * (x - d / 2 - self.easy_interval[0]) ** 2 - self.depth

        return np.inf


class Boltzmann:
    def __init__(self, temp: int, potential: Potential):
        self.T = temp
        self.U = potential.easy_f
        self.inter = potential.get_interval()
        self.C = integrate.quad(self._unnormed_pdf, self.inter[0], self.inter[1])[0]

        self.mean = integrate.quad(lambda x: x * self.pdf(x), self.inter[0], self.inter[1])[0]
        self.dispersion = integrate.quad(lambda x: (x - self.mean) ** 2 * self.pdf(x), self.inter[0], self.inter[1])[0]

    def _unnormed_pdf(self, x: int):
        res = np.exp(-self.U(x) / self.T)
        return res

    def pdf(self, x: int):
        return self._unnormed_pdf(x) / self.C

    def draw_random(self):
        return draw_random_from_pdf(self.pdf, self.inter)

    def entropy(self):
        return - integrate.quad(self.f, self.inter[0], self.inter[1])[0]

    def f(self, x):
        if self.pdf(x) == 0:
            return 0
        return self.pdf(x) * np.log(self.pdf(x))

    def get_mean(self):
        return self.mean

    def get_dispersion(self):
        return self.dispersion

    def periodicity_lim(self):
        return 1 - self.dispersion / self.mean ** 2


def periodicity_coef(x):
    return 1 - np.std(x)**2 / np.mean(x)**2


"""
Draws a random number from given probability density function.

Parameters
----------
    pdf       -- the function pointer to a probability density function of form P = pdf(x)
    interval  -- the resulting random number is restricted to this interval
    pdfmax    -- the maximum of the probability density function
    integers  -- boolean, indicating if the result is desired as integer
    max_iterations -- maximum number of 'tries' to find a combination of random numbers (rand_x, rand_y) located below the function value calc_y = pdf(rand_x).

returns a single random number according the pdf distribution.
"""


def draw_random_from_pdf(pdf, interval=[-1, 1], pdfmax=1, integers=True, max_iterations=10000):
    for i in range(max_iterations):
        if integers == True:
            rand_x = np.random.randint(interval[0], interval[1])
        else:
            rand_x = (interval[1] - interval[0]) * np.random.random(1) + interval[0] #(b - a) * random_sample() + a

        rand_y = pdfmax * np.random.random(1)
        calc_y = pdf(rand_x)

        if(rand_y <= calc_y):
            return rand_x

    raise Exception("Could not find a matching random number within pdf in " + max_iterations + " iterations.")
