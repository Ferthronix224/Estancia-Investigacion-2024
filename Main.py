# Regresión simbolica usando evolucion gramatical
import numpy as np
from Fitness import Fitness_Function
import DE
import MP_CFG_BNF

# Método para hacer las operaciones dentro de la cadena dada
def Equations(equation, x):
    parts = equation.split('+')
    if "Incompleto" in parts or parts[0].find('Incompleto') != -1:
        return np.ones(len(x)) * 999_999_999_999
    if parts[0] == 'x**2':
        parts[0] = x**2
    elif parts[0] == 'x**3':
        parts[0] = x**3
    elif parts[0] == 'x**4':
        parts[0] = x**4
    elif parts[0] == 'x**5':
        parts[0] = x**5
    elif parts[0] == 'x**6':
        parts[0] = x**6
    if parts[1] == 'sen(x)':
        parts[1] = np.sin(x)
    elif parts[1] == 'cos(x)':
        parts[1] = np.cos(x)
    elif parts[1] == 'sqrt(x)':
        parts[1] = np.sqrt(x)
    elif parts[1] == 'ln(x)':
        parts[1] = np.log10(x)
    return parts[0] + parts[1]

x = np.arange(-10, 10.25, 0.25)
y = (x ** 3) + np.sin(x)
fitness = lambda x, y: Fitness_Function().mean_squared_error(x, y)
F = 0.5
CR = 0.8
size = 5
dimension = 10
low_lim = -10
up_lim = 10
generations = 50
termination_criteria = 1E-6
grammar = {
    '<Start>': [['<Variable>', '<Power>', '+', '<Equation>', '(', '<Variable>', ')']],
    '<Variable>': [['x']],
    '<Power>': [['**2'], ['**3'], ['**4'], ['**5'], ['**6']],
    '<Equation>': [['sen'], ['cos']]
}

# Población inicial
population = [DE.Individual(dimension, low_lim, up_lim).return_genotype() for _ in range(size)]

for i in range(generations):
    # Lista de fenotipos
    phenotypes = [MP_CFG_BNF.depth_first(population[ii], grammar, [['<Start>']]) for ii in range(len(population))]
    # Lista de los resultados de las operaciones
    y2 = [Equations(phenotypes[iii], x) for iii in range(len(phenotypes))]
    # Lista de los resultados de la función fitness
    fitness_value = [fitness(y, y2[iv]) for iv in range(len(population))]
    # Impresión del mejor individuo y su fitness
    print(i, fitness_value[0], phenotypes[0])
    # Criterio de paro
    if fitness_value[0] <= termination_criteria:
        break
    # Variable que almacena el resultado del método de mutación
    mutation = DE.Mutation(F, population)
    # Variable que almacena el resultado del método de cruza
    crossover = DE.Crossover(CR, population, mutation)
    # Método de selección
    DE.Selection(population, crossover, fitness, y, y2)