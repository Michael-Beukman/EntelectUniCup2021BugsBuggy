from math import ceil
from general.proper_2021.ProperSolution import ProperSolution
from general.proper_2021.ProperProblem import ProperProblem
import numpy as np


def main(prob: ProperProblem):
    """
        Most simple -> Spread out evenly.
    """
    ans = [[] for s in range(prob.nships)]
    all_clusters = [k for k in prob.all_clusters]
    N = ceil(len(all_clusters) / len(ans))
    for s in range(prob.nships):
        ans[s] = all_clusters[s * N: (s + 1) * N] + ['0']

    sol = ProperSolution(prob, ans)
    sol.write()



if __name__ == '__main__':
    for i in range(1, 6):
        main(ProperProblem(f'{i}.txt'))
