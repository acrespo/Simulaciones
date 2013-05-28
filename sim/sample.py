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

def workforce_sample(min):
    u = random.uniform()
    if u < 0.30:
        return min
    elif u < 0.8:
        return min + 1
    else:
        return min + 2

def project(hours_min, hours_max, hours_mode, price_min, price_max, price_mode, delivery_min):
    hours = int(random.triangular(hours_min, hours_mode, hours_mode))
    price = int(random.triangular(price_min, price_mode, price_max))


    delivery = ceil(hours / (4 * 40.0 * workforce_sample(delivery_min)))

    return (hours, price, delivery)

def small_project():
    return project(500, 2000, 1400, 260, 310, 280, 1)

def medium_project():
    return project(2000, 4500, 3200, 200, 290, 240, 3)

def big_project():
    return project(4500, 8000, 5300, 180, 250, 200, 5)

