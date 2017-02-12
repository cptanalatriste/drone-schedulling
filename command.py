"""
This file contain the drone command implementation.
"""
import driver
import utils


def get_deliver_cost(drone, order):
    action_cost = 1
    turns = action_cost + utils.get_distance(drone.x_possiton, drone.y_possition, order.x_possition, order.y_possition)

    for product_type, items in enumerate(drone.current_items):
        if order.pending_levels[product_type] < items:
            print "Order ", order.id, " does not require ", items, " of product ", product_type, " only ", \
                order.pending_levels[product_type]
            return None

    return turns


def get_load_cost(drone, warehouse, product_type, to_deliver, problem_context):
    if warehouse.storage_levels[product_type] < to_deliver:
        print "Cannot get ", to_deliver, " items of product type ", product_type, " from warehouse ", warehouse.id
        return None

    total_weight = utils.get_load_weight(product_type, to_deliver, problem_context.weight_catalog)
    if drone.current_load + total_weight > problem_context.max_payload:
        print 'The capacity of drone was exceed. Current load: ' + str(drone.current_load) + " Intended Load: " + str(
            total_weight), " Max Payload: ", problem_context.max_payload
        return None

    if warehouse.storage_levels[product_type] < to_deliver:
        print "Warehouse ", warehouse.id, " stock of product type ", product_type, " is only ", \
            warehouse.storage_levels[product_type], " . Cannot load ", to_deliver
        return None

    action_cost = 1
    turns = action_cost + utils.get_distance(drone.x_possiton, drone.y_possition, warehouse.x_possition,
                                             warehouse.y_possition)
    return turns


def load_successfull(drone, warehouse, product_type, to_deliver, problem_context):
    drone.x_possiton = warehouse.x_possition
    drone.y_possition = warehouse.y_possition
    drone.current_load = drone.current_load + utils.get_load_weight(product_type, to_deliver,
                                                                    problem_context.weight_catalog)

    drone.current_items[product_type] += to_deliver
    warehouse.storage_levels[product_type] = warehouse.storage_levels[product_type] - to_deliver

    if driver.DEBUG:
        print "Drone ", drone.id, " loaded ", to_deliver, " items of product ", product_type, " from warehouse ", \
            warehouse.id


def deliver_successfull(drone, order, product_type, to_deliver):
    drone.x_possiton = order.x_possition
    drone.y_possition = order.y_possition
    drone.current_load = 0
    drone.current_items = [0 for _ in drone.current_items]

    order.pending_levels[product_type] = order.pending_levels[product_type] - to_deliver

    if driver.DEBUG:
        print "Drone ", drone.id, " delivered ", to_deliver, " items of product ", product_type, " for order ", order.id
