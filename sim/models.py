class Company(object):

    def __init__(self, resources, strategy):

        self.workflow = Workflow(resources)
        self.strategy = strategy

        self.opportunity_cost = 0
        self.earnings = 0

    def decide_project(self, project):

        new_workflow = self.workflow.add_project(project)

        if new_workflow.is_deliverable() and self.strategy(self, project):
            print("Accepted project " + str(project))
            self.workflow = new_workflow
            self.earnings += project.cost
        else:
            print("Declined project " + str(project))
            self.opportunity_cost += project.cost

class Project(object):

    def __init__(self, hours, price_per_hour, periods_to_delivery):

        self.hours = hours
        self.price_per_hour = price_per_hour

        self.hours_left = self.hours
        self.periods_to_delivery = periods_to_delivery

        self.cost = self.hours * self.price_per_hour

    def __repr__(self):
        return "Project(%d [h] * %d [$/h] = $ %d) = (%d [mes], %d [h]) " % (self.hours, self.price_per_hour, self.cost, self.periods_to_delivery, self.hours_left)

class Workflow(object):

    def __init__(self, resources, projects = []):
        self.resources = resources
        self.projects = projects

    def add_project(self, project):
        return Workflow(self.resources, self.projects + [project])

    def is_deliverable(self):

        projects = self.projects[:]
        projects.sort(key = lambda p: p.periods_to_delivery)

        unused = 0
        last_period = 0

        for p in projects:
            hours_since_last = (p.periods_to_delivery - last_period) * 40 * 4 * self.resources

            if p.hours_left > hours_since_last + unused:
                return False

            unused += hours_since_last - p.hours_left
            last_period = p.periods_to_delivery


        return True

