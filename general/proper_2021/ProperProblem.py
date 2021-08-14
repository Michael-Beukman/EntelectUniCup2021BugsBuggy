import os
from typing import Dict
import numpy as np
from general.problem.Problem import Problem
PATH = os.path.join(*'general/proper_2021/inputs'.split('/'))

score_table = {
    1: {'cm': 1, 'pm':  2, 'pt':  2, 'qb': 1.5 },# Adamantium
    2: {'cm': 1, 'pm':  2, 'pt':  2, 'qb': 2 },# Madamantium
    3: {'cm': 1, 'pm':  2, 'pt':  3, 'qb': 2.5 },# Sadamantium
    4: {'cm': 2, 'pm':  4, 'pt':  3, 'qb': 4 },# Gladamantium
    5: {'cm': 2, 'pm':  4, 'pt':  3, 'qb': 3 },# Radamantium
    6: {'cm': 2, 'pm':  4, 'pt':  4, 'qb': 4 },# Badamantium
    7: {'cm': 3, 'pm':  6, 'pt':  4, 'qb': 4.5 },# Chocolate
    8: {'cm': 3, 'pm':  6, 'pt':  5, 'qb': 4.5 },# Antmanium
    9: {'cm': 4, 'pm':  8, 'pt':  6, 'qb': 6 },# Vladamantium
    10: {'cm': 5, 'pm':  10, 'pt':  8, 'qb': 5 },# Vibranium
}

class ResourceCluster:
    def __init__(self, x: int, y: int, z: int, num_resources: int, id: str, type: int) -> None:
        self.id = id
        self.pos = np.array([x, y, z])
        self.resource_count = num_resources
        self.type = type
        

class ProperProblem(Problem):
    """
    Once problem instance of the 2021 main problem.

    Args:
        Problem ([type]): [description]
    """
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        
        # resource id -> percentage quota.
        self.quotas: Dict[str, int] = {}
        self.clusters: Dict[str, Dict[str, ResourceCluster]] = {}
        self.all_clusters: Dict[str, ResourceCluster] = {}
        with open(os.path.join(PATH, filename), 'r') as f:
            lines = f.readlines()
            # num unique resources, num ships, ship capacity, number of labs, threshold, number of quotas
            self.ur, self.nships, self.capacity, self.nlabs, self.thresh, self.nq = map(int, lines[0].split("|"))
            lines.pop(0)
            # Ignore line 2
            lines.pop(0)

            for i in range(self.nq):
                res_id, quota = map(int, lines.pop(0).split("|"))
                self.quotas[res_id] = quota

            for i in range(self.ur):
                things = lines.pop(0).split("|")
                res_id = int(things[0])
                things = things[1:]
                self.clusters[res_id] = {}
                for specific_cluster in things:
                    T = specific_cluster.split(",")
                    cluster_id = T[0]
                    x, y, z, count = map(int, T[1:])
                    self.clusters[res_id][cluster_id] = ResourceCluster(x, y, z, count, cluster_id, res_id)
                    self.all_clusters[cluster_id] = self.clusters[res_id][cluster_id]


    def print(self):
        for rid in self.clusters:
            total = 0
            for k, v in self.clusters[rid].items():
                total += v.resource_count
            print("RID {} = {:,}".format(rid, total))
        print("====")
        print("Quotas")
        print("====")
        for rid in self.quotas:
            print(f"RID {rid} = {self.quotas[rid]}")



    