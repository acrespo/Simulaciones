import sample
import strategies

from models import Company, Project

from time import sleep
from math import floor
from operator import attrgetter

def simulate_company(stats):

    company = Company(20, 4, strategies.hours_price, stats)

    # A 2 year run
    for t in range(stats.runs):

        print("Step %d:" % (t, ))
        stats.start_month()

        projects = [generate_project() for _ in range(sample.project_count())]
        company.decide_projects(projects)

        used_resources = company.workflow.work()

        stats.end_month(used_resources, company.workflow.average_workload())


        sleep(0.2)

        #print(stats.monthly_report())

    print("")
    print(stats)

def generate_project():

    size = sample.project_size()

    if size == 0:
        return Project(*sample.small_project())
    elif size == 1:
        return Project(*sample.medium_project())
    else:
        return Project(*sample.big_project())

