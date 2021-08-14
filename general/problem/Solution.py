import datetime
import glob
import os
from general.problem.Problem import Problem


class Solution:
    """
    General solution. 
    """
    def __init__(self, problem: Problem, path: str) -> None:
        self.problem = problem
        self.path = path

    def score(self) -> float:
        """Returns a score for this solution. Higher scores are better

        Returns:
            float: [description]
        """
        pass

    def mutate(self) -> "Solution":
        """
            Returns a neighbouring or mutated solution. Should not change this one.
        """

        pass

    def crossover(self, other: "Solution") -> "Solution":
        """Returns another solution that is obtained by performing crossover with the other solution.
        """
        pass

    def to_string(self) -> str:
        raise NotImplementedError()
    
    def write(self, score=None):
        s = self.to_string()
        if score is None:
            score = self.score()
        today = datetime.datetime.now()
        date = today.strftime('%y-%m-%d_%H-%M-%S')
        dir = os.path.join(self.path, f'outs/{self.problem.filename}')
        dir2 = os.path.join(self.path, 'outs/all')
        dir3 = os.path.join(self.path, 'outs/best')
        for d in [dir, dir2, dir3]:
            if not os.path.exists(d):
                os.makedirs(d)

        with open(f"{dir}/{date}_{score}.txt", 'w+') as f:
            f.write(s)

        with open(f"{dir2}/{self.problem.filename}_{date}_{score}.txt", 'w+') as f:
            f.write(s)

        # now update the best directory
        thing = glob.glob(f'{dir3}/{self.problem.filename}*')
        
        if len(thing) == 0:
            best_score = -1e10
        else:
            thing = thing[0]
            name, best_score = thing.split('/')[-1].split('__')
            best_score = float(best_score.split(".txt")[0])
            if 1 or score > best_score:
                os.unlink(thing)
        if 1 or score > best_score:
            # now rewrite it:
            print(f"New Best Score ({score} >= {best_score})")
            with open(f'{dir3}/{self.problem.filename}__{score}.txt', 'w+') as f:
                f.write(s)
