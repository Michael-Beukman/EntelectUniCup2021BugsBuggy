from collections import defaultdict
import copy
import random
from typing import List

import numpy as np
from general.proper_2021.ProperProblem import ProperProblem
from general.proper_2021.ProperProblem import PATH
from general.proper_2021.ProperProblem import score_table
from general.problem.Solution import Solution


class ProperSolution(Solution):
    def __init__(self, problem: ProperProblem, ship_tasks: List[List[str]]) -> None:
        super().__init__(problem, PATH)
        # List of ships, each ship is list of string ids.
        self.ship_tasks = ship_tasks
        # self.ship_tasks = [
        #     [t for t in T if t != '0'] for T in ship_tasks
        # ]
        self.problem: ProperProblem = problem
        X = sum(self.ship_tasks, [])
        self.ids_not_used = set(problem.all_clusters.keys()) - set(X)


    def crossover(self, other: "Solution") -> "Solution":
        return self
    
    def mutate(me) -> "Solution":
        self = copy.deepcopy(me)
        if np.random.rand() < 0.5:
            # swap
            i, j = np.random.randint(0, len(self.ship_tasks)), np.random.randint(0, len(self.ship_tasks))
            l1, l2 = self.ship_tasks[i], self.ship_tasks[j]
            k = min(len(l1), len(l2)) // 2
            old = self.ship_tasks[i][:k]
            self.ship_tasks[i][:k] = self.ship_tasks[j][k:]
            self.ship_tasks[j][k:] = old
        else:
            if np.random.rand() < 0.5:
                if len(self.ids_not_used) == 0: return self
                # thing_to_add = random.choice(self.ids_not_used)
                thing_to_add = random.sample(self.ids_not_used, 1)[0]
                self.ids_not_used.remove(thing_to_add)
                i = np.random.randint(0, len(self.ship_tasks))

                if len(self.ship_tasks) <= 1:
                    K = 0
                else:
                    K = np.random.randint(0, len(self.ship_tasks[i]))

                self.ship_tasks[i].insert(K, thing_to_add)
            else:
                i = np.random.randint(0, len(self.ship_tasks))
                if len(self.ship_tasks[i]) <= 0:
                    return self
                if len(self.ship_tasks[i]) == 1:
                    K = 0
                else:
                    K = np.random.randint(0, len(self.ship_tasks[i]))

                A = self.ship_tasks[i].pop(K)
                self.ids_not_used.add(A)
            
        return self
    
    def score(self) -> float:
        # TODO
        # find nrb
        # find trc
        # find ttp
        # tdt
        space_station_capacity = 0
        space_station_batches = []
        
        collect_score = 0
        process_score = 0
        distance_score = 0 
        time_to_process = 0
        quota_bonus = 0
        
        total_resources_per_type = defaultdict(lambda: 0)
        ships_sorted = []

        new_tasks = []
        for s in self.ship_tasks:
            t = []
            for K in s:
                if K == '0' or K == 0:
                    t.append('0')
                    new_tasks.append(t)
                    t = []
                else:
                    t.append(K)


        for ship in new_tasks:
            current_pos = np.array([0, 0, 0])
            current_capacity = self.problem.capacity
            carrying_current = defaultdict(lambda: 0)
            total_dist_for_ship = 0
            for cluster_id in ship:
                if cluster_id == '0':
                    d = np.ceil(np.linalg.norm(current_pos))
                    total_dist_for_ship += d
                    continue

                cluster = self.problem.all_clusters[cluster_id]
                d = np.ceil(np.linalg.norm(cluster.pos - current_pos))
                total_dist_for_ship += d
                current_pos = cluster.pos
                
                num_resources_here = cluster.resource_count
                if current_capacity <= 0:
                    # Don't pick up
                    continue
                else:
                    current_capacity -= num_resources_here
                    carrying_current[cluster.type] += num_resources_here
            
            # now get batches for each resource type
            temp_batches = []
            for rid in carrying_current:
                if space_station_capacity >= self.problem.thresh:
                    mult = 0.5
                else:
                    mult = 1
                # This is gained by collecting
                # points = mult * carrying_current[rid] * score_table[rid]['cm']
                # collect_score += points
                # space_station_batches.append((rid, carrying_current[rid]))
                temp_batches.append((rid, carrying_current[rid]))
            # print(total_dist_for_ship)
            distance_score += total_dist_for_ship
            ships_sorted.append((total_dist_for_ship, ship, temp_batches))

            # TODO processing.

        # Here processing and quota
        # TODO batches and such 
        total = 0
        # Labs something like this
        # make first ships 
        ships_sorted = sorted(ships_sorted)
        # Time is start of first ship arrival
        current_time = ships_sorted[0][0]
        labs = np.zeros(self.problem.nlabs)
        lab_temp = [(0,(0,0)) for _ in labs]

        queue = []
        for D, S, B in ships_sorted:
            for b in B:
                queue.append((D, b))
        
        processed_things = []
        current_storage_size = 0
        queue2 = copy.deepcopy(queue)

        def adds():
            nonlocal process_score, collect_score, current_storage_size
            if current_storage_size >= self.problem.thresh:
                # lose points
                mult = -0.5
                M = 0.5
            else:
                M = 1
                mult = 1
            
            process_score += mult * amount * score_table[rid]['pm']
            collect_score += M * amount * score_table[rid]['cm']

            current_storage_size += amount

        while len(queue) > 0 or np.any(labs >= 0):
            has_lab_finished = False
            for index, lab in enumerate(labs):
                if lab < 0 and len(queue) > 0:
                    # now, this lab can get another thing.
                    min_time, (resid, num)  = queue[0]
                    if min_time <= current_time:
                        # can process now
                        queue.pop(0)
                        labs[index] = num * score_table[resid]['pt']
                        lab_temp[index] = (min_time, (resid, num))
                                                
                        rid = resid
                        amount = num
                        if resid != 0:
                            adds()
                    else:
                        # cannot now
                        labs[index] = -1
                        pass
                if lab == 0:
                    has_lab_finished = True
                    # I am just now done
                    D, (rid, amount) = lab_temp[index]
                    if rid != 0:
                        processed_things.append((rid, amount))
                        # print("PROB THRSH", self.problem.thresh, current_storage_size, amount)
                        # adds()
                        # print("Storage", current_storage_size)

                    # now, this lab can get another thing.
                    if len(queue):
                        min_time, (resid, num)  = queue[0]
                    else:
                        min_time = current_time + 10

                    if min_time <= current_time:
                        # can process now
                        queue.pop(0)
                        labs[index] = num * score_table[resid]['pt']
                        lab_temp[index] = (min_time, (resid, num))
                        
                        rid = resid
                        amount = num
                        if resid != 0:
                            adds()
                    else:
                        # cannot now
                        labs[index] = -1
                        pass
            if not has_lab_finished:
                current_time += 1
                labs -= 1
        # print("PROCCED", processed_things)
        # print("LABS", labs)
        for (resid, count) in processed_things:
            total_resources_per_type[resid] += count
            total += count
        
        # quotas
        perc_resources = {}
        for rid in total_resources_per_type:
            perc_resources[rid] = total_resources_per_type[rid] / total
            if rid in self.problem.quotas and perc_resources[rid] >= self.problem.quotas[rid] / 100:
                # print(f"Quota, {self.problem.quotas[rid]},{perc_resources[rid]} {total_resources_per_type[rid]} * {score_table[rid]['qb']}")
                quota_bonus += total_resources_per_type[rid] * score_table[rid]['qb']


        # print(f"Time = {current_time}, Quota time = {quota_bonus}, collecting = {collect_score}, distance travelled = {distance_score}, proces score = {process_score}")
        return np.ceil(quota_bonus + collect_score - distance_score * 0.5 + process_score - 0.1 * current_time)
        return 0;
        return super().score()
    
    def to_string(self) -> str:
        s = ""
        for ship in self.ship_tasks:
            r = ""
            for id in ship:
                r += f'{id},'
            if r == "" or r == ",": continue
            r = r[:-1]
            # add in final one
            if id != '0' and id != 0:
                r += ',0'
            s += r + "\n"
        return s

    @staticmethod
    def from_file(prob, name) -> "ProperSolution":
        with open(name, 'r') as f:
            alls = []
            lines = f.readlines()
            for l in lines:
                alls.append(l.strip().split(','))
            return ProperSolution(prob, alls)
        pass
    

if __name__ == '__main__':
    prob = ProperProblem('2.txt')
    sol = ProperSolution.from_file(prob, 'general/proper_2021/inputs/outs/best/2.txt__121328.0.txt')
    print("Socre", sol.score())

    exit()
    prob = ProperProblem('a_in')
    sol = ProperSolution(prob, [
        ['a1', 'a4', 'a2', 'a0', '0'],
        ['b1', 'b4', '0'],
        ['b2', 'b3', 'a3', '0']
    ])
    sol = ProperSolution(prob, [
        ['a0','a1','a2','a3','0'],
        ['a4','b0','b1','b2','0'],
        ['b3','b4','0'],
    ])
    print(sol.score())