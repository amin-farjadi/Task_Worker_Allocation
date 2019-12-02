# Data:
# Tasks queue is a list
# Job represented by a dictionary
# Worker repr by dictionary


class JobDescription:
    def __init__(self, skills):
        self.skills = skills


music = JobDescription(['creativity', 'coordination', 'drinking'])
kicking_ball = JobDescription(['energy', 'coordination', 'determination'])
software = JobDescription(['logic', 'determination', 'vision'])
space_travel = JobDescription(['determination', 'logic', 'curiosity'])
dig_tunnel = JobDescription(['energy', 'determination', 'curiosity'])
daydreaming = JobDescription(['creativity', 'drinking', 'communication'])
cold = JobDescription(['energy', 'drinking', 'communication'])


class Task:
    # weighting is how important/hard that task is
    # - e.g. digging 10m tunnel is harder than a 5m
    def __init__(self, jobtype, weighting):
        self.jobtype = jobtype
        self.weighting = weighting


task1 = Task(music, 3)
taks2 = Task(cold, 1)
task3 = Task(space_travel, 10)


class Worker:
    """
    A worker performs a task.
    In this class, the strengths and weaknesses of differrent
    types of workers is defined.
    This class can also identify how well a worker can perform a task.
    This is done by calculation the "cost".
    The higher the cost, the better that worker can perform said task.

    """

    def __init__(self, skills, penalty):
        self.skills = skills
        self.penalty = penalty
        self.task = None
        self.fatigue = 1

    def is_penalty(self, task):
        # to check if the penalty
        # (i.e. skill the worker doesn't have is required by the job)
        return self.penalty in task.jobtype.skills

    def skill_score(self, task):
        # list all the matched skills
        skill_match = list(set(task.jobtype.skills).intersection(self.skills))
        # testing if penalty exists
        score = len(skill_match) - self.is_penalty(task)
        return score

    def compute_cost(self, task):
        cost = (self.skill_score(task) ** 1.5) * \
            task.weighting / (self.fatigue)
        return cost


student = Worker(['drinking', 'curiosity', 'energy'], 'communication')
engineer = Worker(['logic', 'vision', 'creativity'], 'coordination')
lawyer = Worker(['communication', 'determination', 'vision'], 'drinking')
mathematician = Worker(['logic', 'vision', 'determination'], 'coordination')
artist = Worker(['creativity', 'coordination', 'drinking'], 'logic')
barista = Worker(['coordination', 'communication', 'drinking'], 'energy')
