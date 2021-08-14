from math import ceil
from typing import List
from general.proper_2021.ProperSolution import ProperSolution
from general.proper_2021.ProperProblem import ProperProblem, ResourceCluster, score_table
import numpy as np


def main(prob: ProperProblem):
    """
        Basic greedy, round robin fashion thingy.
    """
    ans = [[] for s in range(prob.nships)]

    batch_size = 5
    num_batches = ceil(len(ans) / batch_size)
    all_clusters: List[ResourceCluster] = [prob.all_clusters[k] for k in prob.all_clusters]
    print("Num batches = ", num_batches)
    for index in range(num_batches):
        print(f"BATCH {index}")
        positions = [np.array([0, 0, 0]) for _ in range(batch_size)]
        capacities = [0 for _ in range(batch_size)]
        do_loop = True
        while do_loop:
            do_loop = False
            for i in range(batch_size):
                I = i + batch_size * index
                # print(f"BAtCH index {i}, {I}, {i} + {batch_size} * {index}`")
                if I >= len(ans): continue
                if len(all_clusters) == 0: continue
                pos = positions[i]
                cap = capacities[i]
                if cap >= prob.capacity:
                    continue
                do_loop = True
                # myindex, RC = max(enumerate(all_clusters), key=lambda K: -np.linalg.norm(K[1].pos - pos))
                # myindex, RC = max(enumerate(all_clusters), key=lambda K: K[1].resource_count)
                myindex, RC = max(enumerate(all_clusters), key=lambda K: score_table[K[1].type]['cm'] * K[1].resource_count)
                all_clusters.pop(myindex)
                capacities[i] += RC.resource_count
                positions[i] = RC.pos
                # print(I, len(ans))
                ans[I].append(RC.id)
                # print("INDEX", index, ans[I])
                # print('cap', capacities[i])
                

    sol = ProperSolution(prob, ans)
    score = sol.score()
    # print("SCORE = ",score)
    sol.write(0)



if __name__ == '__main__':
    for i in range(1, 2):
        print(f"PROB {i}")
        main(ProperProblem(f'{i}.txt'))
