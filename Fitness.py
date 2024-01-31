import numpy as np

class Fitness_Function:
    def sphere(self, x):
        return np.sum(x**2)

    def ackley(self, x):
        a = 20
        b = 0.2
        c = 2 * np.pi
        n = len(x)
        term1 = -a * np.exp(-b * np.sqrt((1 / n) * np.sum(x ** 2)))
        term2 = -np.exp((1 / n) * np.sum(np.cos(c * x)))
        return term1 + term2 + a + np.exp(1)

    def rosenbrock(self, x):
        sum_value = 0
        n = len(x)
        for i in range(n - 1):
            sum_value += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (1 - x[i]) ** 2
        return sum_value

    def mean_squared_error(self, x, y):
        return (np.sum((x-y)**2)) / len(x)