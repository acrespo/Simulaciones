import sample
import strategies

from models import Company, Project
from stats import Stats, Snapshot

from time import sleep
from math import floor

class Simulation(object):

    def __init__(self, aggregator, strategy, reserved_resources, sleep_time=0):

        self.aggregator = aggregator

        self.strategy = strategy
# 2 year warm up, and 10 year run
        self.stats = Stats(24, 120)
        self.company = Company(20, reserved_resources, self.strategy, self.stats)
        self.sleep_time = sleep_time
        self.reserved_resources = reserved_resources

    def run(self):

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

        self.aggregator.add_result(self)
        print("")
        print(self.stats)


def sim_to_key(sim):
    return sim.strategy.__name__ + "-" + str(sim.reserved_resources)

class ResultAggregator(object):

    def __init__(self):
        self.observer = None
        self.results = {}

    def add_result(self, sim):
        # TODO: Compute the output functions on this and store only that
        results = self.results.get(sim_to_key(sim), [])
        results.append(Snapshot(sim.stats))
        self.results[sim_to_key(sim)] = results

        if self.observer:
            self.observer.update(self)

    def set_observer(self, observer):
        self.observer = observer

def batch_run(aggregator):
    print("Starting batch...")
    batch_with_strategy(aggregator, strategies.hours_price)
    batch_with_strategy(aggregator, strategies.cost_price)
    print("Batch done")

def batch_with_strategy(aggregator, strategy):

    for reserved in (0, 2, 4, 6):
        print("Args %s %d" % (strategy.__name__, reserved))
        Simulation(aggregator, strategy, reserved).run()


def generate_project():

    size = sample.project_size()

    if size == 0:
        return Project(*sample.small_project())
    elif size == 1:
        return Project(*sample.medium_project())
    else:
        return Project(*sample.big_project())

