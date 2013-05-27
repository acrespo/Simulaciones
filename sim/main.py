from models import Company, Project
import sample
from math import floor

def run():

    company = Company(20, lambda c, p, w: w.is_deliverable(int(floor(w.resources * 0.8))))

    # A 10 year run
    for t in range(120):

        print("Step %d:" % (t, ))

        project_count = sample.project_count()
        print("Incoming projects %d" % (project_count, ))

        projects = [generate_project() for _ in range(project_count)]
        print('\t' + '\n\t'.join([repr(p) for p in projects]))
# TODO: Sort projects

        for p in projects:
            company.decide_project(p)

        company.workflow.work()

        print("\tEarnings: %d" % (company.earnings, ))
        print("\tOpportunity cost: %d" % (company.opportunity_cost, ))

        print("")

    print("")
    print("Things to know:")
    print("\taccepted: " + str(company.accepted))
    print("\tdeclined: " + str(company.declined))
    print("\tEarnings: %d" % (company.earnings, ))
    print("\tOpportunity cost: %d" % (company.opportunity_cost, ))


def generate_project():

    size = sample.project_size()

    if size == 0:
        return Project(*sample.small_project())
    elif size == 1:
        return Project(*sample.medium_project())
    else:
        return Project(*sample.big_project())


if __name__ == "__main__":
    run()
