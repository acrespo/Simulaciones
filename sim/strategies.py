from operator import attrgetter

def hours_price(projects):
    projects.sort(key = attrgetter('hours'), reverse = True)
    projects.sort(key = attrgetter('price_per_hour'), reverse = True)

    if projects:
        projects[0].is_awesome = True

    return projects

def cost_price(projects):
    projects.sort(key = attrgetter('cost'), reverse = True)
    projects.sort(key = attrgetter('price_per_hour'), reverse = True)

    if projects:
        projects[0].is_awesome = True

    return projects
