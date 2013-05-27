from math import ceil

class Company(object):

    def __init__(self, resources, strategy):

        self.workflow = Workflow(resources)
        self.strategy = strategy

        self.opportunity_cost = 0
        self.earnings = 0

        self.accepted = 0
        self.declined = 0

    def decide_project(self, project):

        new_workflow = self.workflow.add_project(project)

        if new_workflow.is_deliverable() and self.strategy(self, project):
            print("Accepted project " + str(project))
            self.accepted += 1
            self.workflow = new_workflow
            self.earnings += project.cost
        else:
            print("Declined project " + str(project))
            self.declined += 1
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
        self.projects = projects[:]
        self.projects.sort(key = lambda p: p.periods_to_delivery)

    def add_project(self, project):
        return Workflow(self.resources, self.projects + [project])

    def is_deliverable(self):

        unused = 0
        last_period = 0

        for p in self.projects:
            hours_since_last = (p.periods_to_delivery - last_period) * 40 * 4 * self.resources

            if p.hours_left > hours_since_last + unused:
                return False

            unused += hours_since_last - p.hours_left
            last_period = p.periods_to_delivery

        return True

    def work(self):

        print("Working this period")
        print('\t' + '\n\t'.join([repr(p) for p in self.projects]))

        hours_in_period = self.resources * 4 * 40

        hours_left = hours_in_period
        assigned_hours = []

        for p in self.projects:
            hours = int(ceil(float(p.hours_left) / p.periods_to_delivery))
            to_assign = min(hours, hours_left)

            hours_left -= to_assign

            assigned_hours.append(to_assign)

        total_hours = sum(assigned_hours)
        if total_hours > hours_in_period:
            print("PANIC")
            print(self.projects)
            print(assigned_hours)
            assert(False)

        for p, h in zip(self.projects, assigned_hours):
            p.hours_left -= h
            p.periods_to_delivery -= 1

        finished = [p for p in self.projects if p.hours_left == 0]

        if finished:
            print("Delivered this period")
            print('\t' + '\n\t'.join([repr(p) for p in finished]))

        self.projects = [p for p in self.projects if p.hours_left > 0]
        if [p for p in self.projects if p.periods_to_delivery == 0]:
            print("HOLTY SHIT WE DOOMED")
            print(finished)
            print(self.projects)
            print(assigned_hours)
            assert(False)
