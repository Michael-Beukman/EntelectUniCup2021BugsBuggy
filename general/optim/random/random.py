
import copy
import numpy as np
from general.problem.Problem import Problem
from general.problem.Solution import Solution

class Random:
    """
        Randomly solves problem by just perturbing randomly and storing best sol.
    """
    def __init__(self, problem: Problem, init_sol: Solution) -> None:
        self.problem = problem
        self.sol = init_sol

        self.best_sol = copy.deepcopy(init_sol)
        self.best_score = init_sol.score
    
    def solve(self, iterations: int = 1000) -> Solution:
        for i in range(iterations):
            self.sol = self.sol.mutate()
            score = self.sol.score()
            if score > self.best_score:
                self.best_score = score
                self.best_sol = copy.deepcopy(self.sol)
        return self.best_sol