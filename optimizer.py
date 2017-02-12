"""
Optimization algorithm collection.
"""
import driver

RANDOM_SOLUTIONS = 1000

import domain
import random
import io


def no_optimization(problem_configuration, strategy):
    problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)

    total_score, command_list = strategy(drones=drones, orders=orders, warehouses=warehouses,
                                         problem_context=problem_context)

    return total_score, command_list


def random_optimizer(problem_configuration, strategy):
    best_score = 0
    best_solution = None

    for index in range(RANDOM_SOLUTIONS):
        print "Generating random solution ", index + 1, " Current best: ", best_score

        problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)

        random.shuffle(orders)

        if driver.DEBUG:
            print "Warehouses before optimization: "
            for warehouse in warehouses:
                print warehouse

        total_score, command_list = strategy(drones=drones, orders=orders, warehouses=warehouses,
                                             problem_context=problem_context)

        if total_score > best_score:
            best_score = total_score
            best_solution = command_list

            io.write_solution(best_solution, problem_context.file_name)
            print "Better solution found for instance ", problem_context.file_name, " with score ", best_score

    return best_score, best_solution
