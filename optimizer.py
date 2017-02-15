"""
Optimization algorithm collection.
"""
import math

import driver

RANDOM_SOLUTIONS = 100

import domain
import random
import io


def no_optimization(problem_configuration, strategy):
    problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)

    total_score, command_list = strategy(drones=drones, orders=orders, warehouses=warehouses,
                                         problem_context=problem_context)

    return total_score, command_list


def annealing_optimizer(problem_configuration, strategy, temperature=1000, cooling=0.90):
    best_score = 0
    best_solution = None

    order_number = len(domain.get_orders(problem_configuration))

    initial_solution = range(0, order_number)
    random.shuffle(initial_solution)

    while temperature > 0.1:
        print "Current temperature: ", temperature

        one_index, another_index = random.sample(range(0, order_number), 2)

        alternate_solution = list(initial_solution)
        alternate_solution[one_index], alternate_solution[another_index] = alternate_solution[another_index], \
                                                                           alternate_solution[one_index]

        problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)
        total_score, command_list = strategy(drones=drones, orders=[orders[index] for index in initial_solution],
                                             warehouses=warehouses,
                                             problem_context=problem_context)

        if best_solution is None:
            best_score = total_score
            best_solution = command_list
            io.write_solution(best_solution, problem_context.file_name)
            print "Better solution found for instance ", problem_context.file_name, " with score ", best_score

        problem_context, warehouses, drones, orders = domain.get_domain_objects(problem_configuration)
        new_score, new_commands = strategy(drones=drones, orders=[orders[index] for index in alternate_solution],
                                           warehouses=warehouses,
                                           problem_context=problem_context)

        probability = pow(math.e, (-new_score - total_score) / temperature)
        if new_score > total_score or random.random() < probability:
            initial_solution = list(alternate_solution)
            best_score = new_score
            best_solution = new_commands

            io.write_solution(best_solution, problem_context.file_name)
            print "Better solution found for instance ", problem_context.file_name, " with score ", best_score

        temperature = temperature * cooling

    return best_score, best_solution


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
