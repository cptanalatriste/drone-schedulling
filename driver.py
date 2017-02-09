"""
This is the file that will coordinate the execution of the solution
"""
import math

import optimizer
import utils
import io
import domain
import command


def load_and_deliver(drone, warehouse, order, product_type, to_deliver, problem_context):
    turns = None
    load_turns = command.load(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                              problem_context=problem_context)

    if load_turns is not None:
        turns = load_turns
        deliver_turns = command.deliver(drone=drone, order=order, product_type=product_type, to_deliver=to_deliver)

        if deliver_turns is not None:
            turns += deliver_turns

    # print "Total cost ", turns
    # print "Warehouse ", warehouse
    # print "Drone ", drone
    # print "Order ", order

    return turns


def deliver_order(drone, turns, order, warehouses, problem_context):
    turn_stock = turns

    for product_type, pending_items in enumerate(order.pending_levels):

        to_deliver = pending_items

        if to_deliver > 0 and turn_stock > 0:
            # print "Trying to deliver ", pending_items, " of type ", product_type, " from order ", order.id, \
            #     ". Pending turns: ", turn_stock

            for warehouse in warehouses:
                current_stock = warehouse.storage_levels[product_type]

                if current_stock > 0:
                    if current_stock >= to_deliver:
                        turns = load_and_deliver(drone=drone, warehouse=warehouse, order=order,
                                                 product_type=product_type, to_deliver=to_deliver,
                                                 problem_context=problem_context)
                        to_deliver = 0
                    elif current_stock < to_deliver:
                        turns = load_and_deliver(drone=drone, warehouse=warehouse, order=order,
                                                 product_type=product_type, to_deliver=current_stock,
                                                 problem_context=problem_context)
                        to_deliver = to_deliver - current_stock

                    if turns is not None:
                        turn_stock -= turns

    if order.is_complete():
        turn_to_deliver = problem_context.total_turns - turn_stock
        order.score = math.ceil(
            (problem_context.total_turns - turn_to_deliver) / float(problem_context.total_turns) * 100)

        print "Order ", order.id, " was delivered by drone ", drone.id, " at turn ", turn_to_deliver, ". Score: ", order.score

    return turn_stock


def dispatch_in_order(drone, orders, warehouses, problem_context):
    turns_left = problem_context.total_turns
    for order in orders:
        pending_turns = deliver_order(drone=drone, turns=turns_left, order=order,
                                      warehouses=warehouses, problem_context=problem_context)
        turns_left = pending_turns

    finished_orders = [order.score for order in orders if order.score is not None]
    total_score = sum(finished_orders)
    print "Total score: ", total_score, " from ", len(finished_orders), "  orders finished. Total orders: ", len(orders)

    return total_score, drone.commands


def schedule_drones(problem_configuration):
    best_score, command_list = optimizer.random_optimizer(problem_configuration)

    print "Best Score: ", best_score
    return command_list


if __name__ == "__main__":
    problem_configuration = io.read_configuration("inputs/busy_day.in")
    # problem_configuration = io.read_configuration("inputs/mother_of_all_warehouses.in")
    # problem_configuration = io.read_configuration("inputs/redundancy.in")

    # problem_configuration = io.read_configuration("task/example_input.txt")

    solution = schedule_drones(problem_configuration)
    io.write_solution(solution)
