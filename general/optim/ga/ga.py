import numpy as np
from general.problem.Problem import Problem
from general.problem.Solution import Solution
  
class Pop:
    def __init__(self, problem: Problem, init_x: Solution, pop_size: int = 100) -> None:
        self.pops = [init_x] + [init_x.mutate() for _ in range(pop_size - 1)]
        self.pop_count = pop_size
        self.gen_count = 0
        self.problem = problem
    
    def one_gen(self):
        self.gen_count += 1
        probs = self.eval()
        self.breed(probs)
        pass

    def eval(self):
        func = []
        total_fit = 0
        max_fit = -1
        min_fit = 1e7
        KK = 0 # min value as to not get negatives.
        for idx, val in enumerate(self.pops):
            func.append(val.score())
            val.fitness = func[-1] + KK
            val.fitness = max(val.fitness, 0)
            max_fit = max(max_fit, val.fitness)
            total_fit += val.fitness
            min_fit = min(min_fit, val.fitness)

        self.best_fit = max_fit
        print(f"For gen {self.gen_count}: Max Fit = {max_fit - KK}. Average = {total_fit/(max(1, self.pop_count)) - KK}. Min = {min_fit - KK}")
        probs = [
            a.fitness / total_fit for a in self.pops
        ]
        return probs

    def breed(self, probs):
        best_agent = np.argmax(probs)
        self.best_agent = self.pops[best_agent]
        new_pop = [self.best_agent]
        while len(new_pop) < self.pop_count:
            a1 = np.random.choice(self.pops, p=probs)
            a2 = np.random.choice(self.pops, p=probs)
            c = 0
            while a2 == a1 and c < 5:
                c += 1
                a2 = np.random.choice(self.pops, p=probs)

            # print(a1)
            if (a1 == a2):print(" # ", end='')
            child = a1.crossover(a2)
            child.mutate()
            new_pop.append(child)
        self.pops = new_pop
        

    def solve(self, iterations: int = 1000) -> Solution:
        for i in range(iterations):
            self.one_gen()
        return self.best_agent
