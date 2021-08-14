import numpy as np
from general.problem.Problem import Problem
from general.problem.Solution import Solution


class SimulatedAnnealing:
    def __init__(self, problem: Problem, init_sol: Solution) -> None:
        self.problem = problem
        self.sol = init_sol
        self.temperature = 1000
        self.sign = 1

    def solve(self, iterations: int = 1000) -> Solution:
        """Solves the problem by doing some number of iterations

        Args:
            iterations (int, optional): [description]. Defaults to 1000.

        Returns:
            Solution: 
        """
        # Negative as SA minimises
        current_score = self.sign * self.sol.score()
        for iter in range(iterations):
            print(f"\r{iter}/{iterations}", end='')
            next = self.sol.mutate()
            next_score = self.sign * next.score()

            if self.should_swap(current_score, next_score):
                current_score = next_score
                self.sol = next
            
            self.decay()
        return self.sol
    
    def should_swap(self, current_score: float, next_score: float) -> bool:
        """Returns true if should swap according to the SA equation.

        Args:
            current_score (float): [description]
            next_score (float): [description]

        Returns:
            bool: [description]
        """
        if next_score < current_score: return True
        diff = np.exp(-(next_score - current_score)/self.temperature)
        return diff < np.random.rand()
    
    def decay(self):
        """Decays temperature. This does it simply by multiplying T by 0.995, but you can do more complex things here.
        """
        self.temperature *= 0.995

