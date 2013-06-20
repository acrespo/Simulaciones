from operator import attrgetter
from numpy import percentile

def price_hours(company, projects):
    if not projects:
        return projects

    projects.sort(key = attrgetter('hours'), reverse = True)
    projects.sort(key = attrgetter('price_per_hour'), reverse = True)

    company.project_history.extend([p.price_per_hour for p in projects])
    awesome_threshold = percentile(company.project_history, 80)

    awesome = [p for p in projects if p.price_per_hour > awesome_threshold]
    for p in awesome:
        p.is_awesome = True

    return projects

def cost_price(company, projects):
    if not projects:
        return projects

    projects.sort(key = attrgetter('price_per_hour'), reverse = True)
    projects.sort(key = attrgetter('cost'), reverse = True)

    company.project_history.extend([p.cost for p in projects])
    awesome_threshold = percentile(company.project_history, 80)

    awesome = [p for p in projects if p.cost > awesome_threshold]
    for p in awesome:
        p.is_awesome = True

    return projects
