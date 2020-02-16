class JobDescription:
    """
    Job description provides the skills required
    for that instance
    Output: job
    """
    def __init__(self, skills):
        self.skills = skills

music = JobDescription(['creativity', 'coordination', 'drinking'])
kicking_ball = JobDescription(['energy', 'coordination', 'determination'])
software = JobDescription(['logic', 'determination', 'vision'])
space_travel = JobDescription(['determination', 'logic', 'curiosity'])
dig_tunnel = JobDescription(['energy', 'determination', 'curiosity'])
daydreaming = JobDescription(['creativity', 'drinking', 'communication'])
cold = JobDescription(['energy', 'drinking', 'communication'])


class Task(JobDescription):
    # weighting is how important/hard that task is
    # - e.g. digging 10m tunnel is harder than a 5m
    """
    A task 
    """
    def __init__(self, job, weighting):
        JobDescription.__init__(self,job.skills)
        self.job = job
        self.weighting = weighting

task1 = Task(music, 3)
task2 = Task(cold, 1)
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
        return self.penalty in task.job.skills

    def skill_score(self, task):
        # list all the matched skills
        skill_match = list(set(task.job.skills).intersection(self.skills))
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

# jobs = [task1, task2]
# resources = [student, engineer]
# q1 = Queue([task1, task2], [student, engineer])
# cost_q1 = q1.total_cost
import numpy as np
class Queue:
    """Queue class takes a list of jobs (i.e. of Task class) and a list of resources (i.e. of Worker class)
    and matches jobs to workers """
    def __init__(self, tasks, resources):
        self.tasks = tasks
        self.resources = resources

    row, col = (len(tasks), len(resources))
    costs= np.zeros((row,col))  #[ [0 for i in range(len(tasks))] for j in range(len(resources)) ]
    i=0 #counter for tasks
    j=0 #counter for resources
    for task in tasks:
        for resource in self.resources:
            costs[i,j] = resource.compute_cost(task)
            j=j+1
        i=i+1
    
    #1st number of tuple: min cost, 2nd number: task index. 3rd number: resource index
    #the higher the score of worker, the better
    resources_fit = [(0,0,0) for i in range(col)] 
    for j in range(col):
        costs_col = list(costs[:,j])
        max_cost = max(costs_col)
        task_idx = costs_col.index(max_cost)
        resources_fit[j] = (max_cost, task_idx, j)
    
    best_resource_info = sorted(resources_fit, reverse=True) #sorted to find resource with most cost first

