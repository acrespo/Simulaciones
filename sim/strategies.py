from operator import attrgetter

def hours_price(projects):
    projects.sort(key = attrgetter('hours'), reverse = True)
    projects.sort(key = attrgetter('price_per_hour'), reverse = True)

    if projects:
        projects[0].is_awesome = True

    return projects

