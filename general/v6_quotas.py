from collections import defaultdict
from math import ceil
import sys
from typing import List
from general.proper_2021.ProperSolution import ProperSolution
from general.proper_2021.ProperProblem import ProperProblem, ResourceCluster, score_table
import numpy as np


def main(prob: ProperProblem):
    """
        Basic greedy, round robin fashion thingy.
    """
    ans = [[] for s in range(prob.nships)]

    batch_size = 1000
    num_batches = ceil(len(ans) / batch_size)
    things = sorted(prob.quotas.keys(), reverse=True)
    quotas_to_take = []
    current_p = 0
    # if current_p + p > 100: break
    for t in things:
        p = prob.quotas[t]
        current_p += p
        quotas_to_take.append(t)
        # if len(quotas_to_take) >= 2: break
    quotas_to_take = set(quotas_to_take)
    w1 = 10; w2 = 1000; w3 = 1; w4 = 100000000
    def score(RC: ResourceCluster, current_pos):
        if RC.type not in quotas_to_take: return 0
        return RC.resource_count * w1 + RC.type * w4 - w2 * max(np.linalg.norm(current_pos - RC.pos), 1) + w3 * score_table[RC.type]['pm']
    all_clusters: List[ResourceCluster] = sorted([prob.all_clusters[k] for k in prob.all_clusters if prob.all_clusters[k].type in quotas_to_take], key=lambda s: -score(s, np.array([0, 0, 0])) )#np.linalg.norm(s.pos))
    

    total_weight = 0


    for index in range(num_batches):
        positions = [np.array([0, 0, 0]) for _ in range(batch_size)]
        capacities = [0 for _ in range(batch_size)]
        do_loop = True
        amounts = defaultdict(lambda: 0)
        while do_loop:
            do_loop = False
            for i in range(batch_size):
                # print(f"\rLittle index {i}", end='')
                print(f"\rCap {total_weight}/{prob.thresh}. L ={len(all_clusters)}", end='')
                I = i + batch_size * index
                # print(f"BAtCH index {i}, {I}, {i} + {batch_size} * {index}`")
                if I >= len(ans): continue
                if len(all_clusters) == 0: continue
                pos = positions[i]
                cap = capacities[i]
                if cap >= prob.capacity:
                    ans[I].append('0')
                    capacities[i] = 0
                    positions[i] = np.array([0, 0, 0])
                
                if total_weight >= prob.thresh:
                    continue
                do_loop = True
                myindex, RC = max(enumerate(all_clusters[:10]), key=lambda K: score(K[1], pos))

                all_clusters.pop(myindex)
                capacities[i] += RC.resource_count
                total_weight += RC.resource_count
                positions[i] = RC.pos
                
                amounts[RC.type] += RC.resource_count
                ans[I].append(RC.id)
                
    print(f"TOTAL WEIGHT. {prob.filename} = {total_weight} / {prob.thresh}")
    sol = ProperSolution(prob, ans)
    score = sol.score()
    print("SCORE = ",score)
    sol.write(score)



if __name__ == '__main__':
    abc = int(sys.argv[1])
    # print(abc); exit()
    for i in range(abc, abc + 1):
    # for i in range(1, 6):
        print(f"PROB {i}")
        prob = ProperProblem(f'{i}.txt')
        # prob.print()
        main(prob)
