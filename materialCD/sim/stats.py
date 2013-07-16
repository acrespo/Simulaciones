
def after_warm_up(f):

    def ret(self, *args, **kwargs):
        if self.current_step < self.warm_up:
            return None
        return f(self, *args, **kwargs)

    return ret

def avg(l):
    return sum(l) / len(l)

class Snapshot(object):

    def __init__(self, stats):

        self.runs = stats.runs
        self.warm_up = stats.warm_up
        self.current_step = stats.current_step

        self.demand_hours = stats.demand_hours[:]
        self.demand_proyects = stats.demand_proyects[:]

        self.active_workforce = stats.active_workforce[:]

        self.hours_sold = stats.hours_sold[:]
        self.hours_declined = stats.hours_declined[:]

        self.profit = stats.profit[:]
        self.opportunity_cost = stats.opportunity_cost[:]

        self.average_workload = stats.average_workload[:]


class Stats(object):

    def __init__(self, warm_up, runs):

        self.warm_up = warm_up
        self.runs = runs

        self.demand_hours = []
        self.demand_proyects = []

        self.active_workforce = []

        self.hours_sold = []
        self.hours_declined = []

        self.profit = []
        self.opportunity_cost = []

        self.average_workload = []

        self.current_step = 0
        self.observer = None

    def set_observer(self, observer):
        print('setting observer')
        self.observer = observer

    def start_month(self):
        self.current_step += 1

        if self.current_step >= self.warm_up:
            self.demand_hours.append(0)
            self.demand_proyects.append(0)

            self.hours_sold.append(0)
            self.hours_declined.append(0)

            self.profit.append(0)
            self.opportunity_cost.append(0)

    @after_warm_up
    def end_month(self, active_workforce, average_workload):
        self.active_workforce.append(active_workforce)
        self.average_workload.append(average_workload)

        if self.observer:
            self.observer.end_month(Snapshot(self))

    @after_warm_up
    def project_accepted(self, project):
        self.hours_sold[-1] = self.hours_sold[-1] + project.hours
        self.profit[-1] = self.profit[-1] + project.cost

    @after_warm_up
    def project_declined(self, project):
        self.hours_declined[-1] = self.hours_declined[-1] + project.hours
        self.opportunity_cost[-1] = self.opportunity_cost[-1] + project.cost

    @after_warm_up
    def project_arrived(self, project):
        self.demand_hours[-1] = self.demand_hours[-1] + project.hours
        self.demand_proyects[-1] = self.demand_proyects[-1] + 1

    @after_warm_up
    def monthly_report(self):
        format_str = """Report for period %d
        Demand hours     %d
               proyects  %d

        Hours sold       %d
              declined   %d

        Profit           %d
        Opportunity cost %d

        Active workforce %f
        Average workload %f
        """

        return format_str % (
                self.current_step,
                self.demand_hours[-1],
                self.demand_proyects[-1],
                self.hours_sold[-1],
                self.hours_declined[-1],
                self.profit[-1],
                self.opportunity_cost[-1],
                self.active_workforce[-1],
                self.average_workload[-1])

    def __str__(self):
        format_str = """End Report
        Demand hours     %d
               proyects  %d

        Hours sold       %d
              declined   %d

        Profit           %d
        Opportunity cost %d

        Active workforce %f
        Average workload %f
        """

        return format_str % (
                avg(self.demand_hours),
                avg(self.demand_proyects),
                avg(self.hours_sold),
                avg(self.hours_declined),
                sum(self.profit),
                sum(self.opportunity_cost),
                avg(self.active_workforce),
                avg(self.average_workload))

    def objective(self):
        return (
                sum(self.profit),
                sum(self.opportunity_cost),
                avg(self.active_workforce)
                )

