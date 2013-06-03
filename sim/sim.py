import sample
import strategies

from models import Company, Project
from stats import Stats

from time import sleep
from math import floor

class Simulation(object):

    def __init__(self, strategy, used_resources, sleep_time=0):

        self.strategy = strategy
# 2 year warm up, and 10 year run
        self.stats = Stats(24, 120)
        self.company = Company(20, used_resources, self.strategy, self.stats)
        self.sleep_time = sleep_time

    def run(self):

        # A 2 year run
        for t in range(self.stats.runs):

            print("Step %d:" % (t, ))
            self.stats.start_month()

            projects = [generate_project() for _ in range(sample.project_count())]
            self.company.decide_projects(projects)

            used_resources = self.company.workflow.work()

            self.stats.end_month(used_resources, self.company.workflow.average_workload())

            if self.sleep_time > 0:
                sleep(self.sleep_time)

            print(self.stats.monthly_report())

        print("")
        print(self.stats)

def generate_project():

    size = sample.project_size()

    if size == 0:
        return Project(*sample.small_project())
    elif size == 1:
        return Project(*sample.medium_project())
    else:
        return Project(*sample.big_project())

