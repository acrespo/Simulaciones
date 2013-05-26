from numpy import random
from math import floor, ceil

def project_count():
    return int(floor(random.poisson(2.0)))

def project_size():
    seed = random.sample()
    if seed < 0.1:
        return 0
    elif seed < 0.85:
        return 1
    else:
        return 2

def project(hours_min, hours_max, hours_mode, price_min, price_max, price_mode, delivery_min, delivery_max, delivery_mode):
    hours = int(random.triangular(hours_min, hours_mode, hours_mode))
    price = int(random.triangular(price_min, price_mode, price_max))

    delivery = ceil(random.triangular(hours / (4 * 40.0 * delivery_min), hours / (4 * 40.0 * delivery_mode), hours / (4 * 40.0 * delivery_max)))

    return (hours, price, delivery)

def small_project():
    return project(500, 2000, 1400, 242, 308, 286, 2.0, 1.0, 1.2)

def medium_project():
    return project(2000, 4500, 3200, 198, 242, 220, 4.5, 2.0, 2.5)

def big_project():
    return project(4500, 8000, 5300, 176, 308, 226, 6.0, 3.0, 4.0)

