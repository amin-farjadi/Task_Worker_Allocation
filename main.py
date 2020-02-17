# -*- coding: utf-8 -*-
"""
Updated on Mon Feb 17 14:14:51 2020

@author: amin.farjadi
"""

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
    def __init__(self, name, job, weighting):
        JobDescription.__init__(self,job.skills)
        self.name = name
        self.job = job
        self.weighting = weighting

task1 = Task('Playing a gig', music, 3)
task2 = Task('Getting a cough', cold, 1)
task3 = Task('Going to Mars', space_travel, 10)


class Worker:
    """
    A worker performs a task.
    In this class, the strengths and weaknesses of differrent
    types of workers is defined.
    This class can also identify how well a worker can perform a task.
    This is done by calculation the "cost".
    The higher the cost, the better that worker can perform said task.
    """

    def __init__(self, name, skills, penalty):
        self.name = name
        self.skills = skills
        self.penalty = penalty
        self.task = None
        self.fatigue = 1

    def is_penalty(self, task):
        # to check if the penalty
        # (i.e. skill the worker doesn't have is required by the job)
        return self.penalty in task.skills

    def skill_score(self, task):
        # list all the matched skills
        skill_match = list(set(task.skills).intersection(self.skills))
        # testing if penalty exists
        score = len(skill_match) - self.is_penalty(task)
        return score

    def compute_cost(self, task):
        cost = (np.abs(self.skill_score(task)) ** 1.5)*np.sign(self.skill_score(task)) * task.weighting / (self.fatigue)
        return cost


worker1 = Worker('student',['drinking', 'curiosity', 'energy'], 'communication')
worker2 = Worker('engineer',['logic', 'vision', 'creativity'], 'coordination')
worker3 = Worker('lawyer',['communication', 'determination', 'vision'], 'drinking')
worker4 = Worker('mathematician',['logic', 'vision', 'determination'], 'coordination')
worker5 = Worker('artist',['creativity', 'coordination', 'drinking'], 'logic')
worker6 = Worker('barista',['coordination', 'communication', 'drinking'], 'energy')
#
import numpy as np
import pandas as pd
class Queue:
    """Queue class takes a list of jobs (i.e. of Task class) and a list of resources (i.e. of Worker class)
    and matches jobs to workers"""
    def __init__(self, tasks, resources):
        """tasks dtype: list of task objects
        resources dtype: list of resource objects"""
        self.tasks = tasks
        self.resources = resources
        self.remaining_tasks = None
        self.remaining_resources = None
    
    def allocate(self):
        tasks = self.tasks #updating array
        resources = self.resources #updating array
        row, col = (len(self.tasks), len(self.resources))
        if row == 0:
            raise ValueError('Tasks cannot be empty')
        if col == 0:
            raise ValueError('Resources cannot be empty')
        
        tasks_allocated = []
        resources_allocated = []
        
        while (row > 0) and (col > 0): 
            #-------------------------------------------------------
            costs= np.zeros((row,col))  #[ [0 for i in range(len(tasks))] for j in range(len(resources)) ]
            i=0 #counter for tasks
            for task in tasks:
                j=0 #counter for resources
                for resource in resources:
                    costs[i,j] = resource.compute_cost(task)
                    j=j+1
                i=i+1
            #------------------------------------------------------   
            #1st number of tuple: max cost, 2nd number: task index. 3rd number: resource index
            #the higher the score of worker, the better 
            df = pd.DataFrame(columns=['Cost', 'Task_idx', 'Resource_idx'])
            for j in range(col): #iterating through resources
                costs_col = list(costs[:,j])
                max_cost = max(costs_col)
                task_idx = costs_col.index(max_cost)
                df.loc[j] = [max_cost, task_idx, j]

            cost_metric = df.sort_values(by=['Cost'],ascending=False,kind='mergesort')#sorted to find resource with most cost first

            #No task repetition
            cost_metric = cost_metric.drop_duplicates(subset='Task_idx', keep='first')
            #No resource repetition
            cost_metric = cost_metric.drop_duplicates(subset='Resource_idx', keep='first')
            
            #Allocation
            for _, df_row in cost_metric.iterrows():
                task_idx = int(df_row['Task_idx'])
                resource_idx = int(df_row['Resource_idx'])
                task_obj = tasks[task_idx]
                resource_obj = resources[resource_idx]
                #
                tasks_allocated.append(task_obj)
                resources_allocated.append(resource_obj)
                #increase fatigue of resource
                resource_obj.fatigue += task_obj.weighting
                

            #Removal            
            tasks = [x for x in tasks if x not in tasks_allocated]
            resources = [x for x in resources if x not in resources_allocated]            
            #Updating                
            row, col = (len(tasks), len(resources))


        #Creating allocation dataframe
        allocation = pd.DataFrame({'Task': [x.name for x in tasks_allocated], 'Resource': [x.name for x in resources_allocated]}, columns=['Task','Resource'])
        #
        if len(tasks)==0 and len(resources)==0:
            pass
        elif len(tasks)==0:
            self.remaining_resources = resources
        elif len(resources)==0:
            self.remaining_tasks = tasks

        return allocation

tasks = [task1, task2, task3]
resources = [worker1, worker2, worker5, worker4]
q1 = Queue(tasks, resources)

print(q1.allocate())