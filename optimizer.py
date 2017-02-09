"""
Optimization algorithm collection.
"""

RANDOM_SOLUTIONS = 100

import domain
import random
import driver


def random_optimizer(problem_configuration):
    best_score = 0
    best_solution = None

    for index in range(RANDOM_SOLUTIONS):
        print "Generating random solution ", index + 1, " Current best: ", best_score

        problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)

        random.shuffle(orders)

        lone_ranger = drones[0]
        total_score, command_list = driver.dispatch_in_order(drone=lone_ranger, orders=orders, warehouses=warehouses,
                                                             problem_context=problem_context)

        if total_score > best_score:
            best_score = total_score
            best_solution = command_list

    return best_score, best_solution
