from math import ceil, floor

class Company(object):

    def __init__(self, resources, reserved_resources, strategy, stats):

        self.workflow = Workflow(resources, reserved_resources)
        self.strategy = strategy

        self.opportunity_cost = 0
        self.earnings = 0

        self.accepted = 0
        self.declined = 0

        self.stats = stats

    def decide_projects(self, projects):

        print('\t' + '\n\t'.join([repr(p) for p in projects]))
#TODO: Calculate TOP 20% projects and give them priority status

        for p in projects:
            self.decide_project(p)

    def decide_project(self, project):
        self.stats.project_arrived(project)

        new_workflow = self.workflow.add_project(project)
        can_be_delivered = new_workflow.is_deliverable()

# TODO: Consider adding extra workforce if project has priority status
        if can_be_delivered and self.strategy(self, project, new_workflow):
            print("Accepted project " + str(project))
            self.workflow = new_workflow
            self.stats.project_accepted(project)
        else:
            print(("Declined project " if can_be_delivered else "Cant deliver ") + str(project))
            self.stats.project_declined(project)

class Project(object):

    def __init__(self, hours, price_per_hour, ideal_devs):

        self.hours = hours
        self.price_per_hour = price_per_hour
        self.ideal_devs = ideal_devs

        self.hours_left = self.hours
        self.periods_to_delivery = int(ceil(self.hours / (4.0 * 40 * self.ideal_devs)))

        self.cost = self.hours * self.price_per_hour

    def __repr__(self):
        return "Project(%d [h] * %d [$/h] = $ %d) = (%d [mes], %d [h], %d [devs]) " % (
                self.hours, self.price_per_hour, self.cost, self.periods_to_delivery, self.hours_left, self.ideal_devs)

class Workflow(object):

    def __init__(self, resources, reserved_resources, projects = []):
        self.resources = resources
        self.reserved_resources = reserved_resources

        self.projects = projects[:]
        self.projects.sort(key = lambda p: p.periods_to_delivery)

    def add_project(self, project):
        return Workflow(self.resources, self.reserved_resources, self.projects + [project])

    def is_deliverable(self):
        # How do we get a project to engage a reserved dev?

        unused = 0
        last_period = 0

        usable_resources = self.resources - self.reserved_resources
        hours_per_period = 40 * 4 * usable_resources

        for p in self.projects:
            hours_since_last = (p.periods_to_delivery - last_period) * hours_per_period
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
            if p.periods_to_delivery == 1:
                hours = p.hours_left
            else:
                hours = floor(p.hours_left / p.periods_to_delivery)
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

        return self.resources * total_hours / float(hours_in_period)

    def average_workload(self):
        # TODO: Stub
        return 0
