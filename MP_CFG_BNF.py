import numpy as np
import copy

genotype = np.array([233, 20, 88, 3, 78, 34, 67, 20, 35, 57])
genotype_count = 0
grammar = {
    '<Start>': [['<MP>', '(', '<Expr>', ')']],
    '<MP>': [['MP2'], ['MP4'], ['MP6'], ['MP8'], ['MP10']],
    '<Expr>': [['(', '<Expr>', '<Op>', '<Expr>', ')'], ['<Filter>', '(', '<Expr>', ')'], ['<Terminal>']],
    '<Filter>': [['<Gau>'], ['<Lap>'], ['<GFB>'], ['<Arith>']],
    '<Gau>': [['Gau1'], ['Gau2'], ['GauDX>'], ['GauDY']],
    '<Lap>': [['LapG1'], ['LapG2'], ['Lap']],
    '<GFB>': [['GFB0'], ['GFB45'], ['GFB90'], ['GFB135']],
    '<Arith>': [['AverF'], ['MedianF'], ['HEq'], ['AbsY'], ['Sqr'], ['Sqrt'], ['Log'], ['T0.5']],
    '<Op>': [['+'], ['-'], ['a-'], ['*'], ['/']],
    '<Terminal>': [['lg']]
}
phenotype = [['<Start>']]

def no_terminal_search(lista):  # Método para buscar simbolos no terminales dentro del fenotipo
    cantidad = 0
    for elemento in lista:
        if isinstance(elemento, list):
            cantidad += no_terminal_search(elemento)
        elif elemento[0] == '<' and elemento[-1] == '>':
            cantidad += 1
    return cantidad

def depth_first(genotype, grammar, phenotype):  # Método de mapeo Depth First
    global genotype_count
    # Condición de que si el fenotipo tiene el simbolo de inicio que el contador del genotipo valga 0
    if phenotype[0][0] == '<Start>':
        genotype_count = 0
    phenotype_str = ''
    # Ciclo que se itera el número del tamaño que tenga el fenotipo
    for i in range(len(phenotype)):
        no_terminal_search_count = no_terminal_search(phenotype)
        # Criterio de paro en caso de que se acaben los codones de del genotipo y aun halla simbolos no terminales
        if genotype_count == len(genotype) and no_terminal_search_count > 0:
            phenotype_str = 'Incompleto'
            genotype_count = 0
            return phenotype_str
        grammar_copy = copy.deepcopy(grammar)
        # Cuando el fenotipo sólo tenga un objeto que se evalue el mismo
        if len(phenotype[i]) == 1:
            if type(phenotype[i][0]) is str:
                phenotype_str += phenotype[i][0]
            if phenotype[i][0][0] == '<' and phenotype[i][0][-1] == '>':
                phenotype[i] = grammar_copy[phenotype[i][0]][int(genotype[genotype_count] % len(grammar_copy[phenotype[i][0]]))]
                genotype_count += 1
                return depth_first(genotype, grammar_copy, phenotype)
        # Cuando el fenotipo tiene más objetos que se haga un barrido de los mismos
        elif len(phenotype[i]) > 1:
            for ii in range(len(phenotype[i])):
                if type(phenotype[i][ii]) is list:
                    phenotype[i][ii] = depth_first(genotype, grammar_copy, [phenotype[i][ii]])
                if type(phenotype[i][ii]) is str:
                    phenotype_str += phenotype[i][ii]
                if phenotype[i][ii][0] == '<' and phenotype[i][ii][-1] == '>':
                    phenotype[i][ii] = grammar_copy[phenotype[i][ii]][int(genotype[genotype_count] % len(grammar_copy[phenotype[i][ii]]))]
                    genotype_count += 1
                    return depth_first(genotype, grammar_copy, phenotype)
    return phenotype_str