from math import ceil
from typing import List
from general.proper_2021.ProperSolution import ProperSolution
from general.proper_2021.ProperProblem import ProperProblem, ResourceCluster
import numpy as np


def main(prob: ProperProblem):
    """
        Basic greedy, 
    """
    ans = [[] for s in range(prob.nships)]
    all_clusters: List[ResourceCluster] = sorted([prob.all_clusters[k] for k in prob.all_clusters], key=lambda s: s.resource_count, reverse=True)
    for s in range(prob.nships):
        cap = prob.capacity
        if cap <=0 : continue
        for c in all_clusters:
            ans[s].append(c.id)
            cap -= c.resource_count

    sol = ProperSolution(prob, ans)
    score = sol.score()
    print("SCORE = ",score)
    # sol.write(score)



if __name__ == '__main__':
    for i in range(1, 6):
        print(f"PROB {i}")
        main(ProperProblem(f'{i}.txt'))
