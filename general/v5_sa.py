import glob
from general.optim.sa.sa import SimulatedAnnealing
from math import ceil
from typing import List
from general.proper_2021.ProperSolution import ProperSolution
from general.proper_2021.ProperProblem import ProperProblem, ResourceCluster, score_table
import numpy as np


def main(prob: ProperProblem, sol_file):
    """
        Basic greedy, round robin fashion thingy.
    """
    ans = [[] for s in range(prob.nships)]
    init_sol = ProperSolution.from_file(prob, sol_file)
    optim = SimulatedAnnealing(prob, init_sol)
    optim.sign = -1
    sol = optim.solve(1)

    # sol = ProperSolution(prob, ans)
    score = sol.score()
    print("SCORE = ",score)
    sol.write(score)



if __name__ == '__main__':
    ans = [
        glob.glob(f'general/proper_2021/inputs/outs/best/{i}*')[0]
        for i in range(5, 6)
    ]
    for i in range(5, 6):
        print(f"PROB {i}")
        main(ProperProblem(f'{i}.txt'), ans[-1])
