from models import Company, Project
from stats import Stats
import sample
from math import floor

def simulate_company():

    def strategy(projects):
#TODO: Calculate TOP 20% projects and give them priority status
        return projects

    stats = Stats(12)
    company = Company(20, 4, strategy, stats)

    # A 10 year simulate_company
    for t in range(24):

        print("Step %d:" % (t, ))
        stats.start_month()

        projects = [generate_project() for _ in range(sample.project_count())]
        company.decide_projects(projects)

        used_resources = company.workflow.work()

        stats.end_month(used_resources, company.workflow.average_workload())

        print(stats.monthly_report())

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


if __name__ == "__main__":
    simulate_company()
