"""
This is the file that will coordinate the execution of the solution
"""

import utils
import test
import io

import math
from scipy.spatial import distance


def get_load_weight(product_type, to_deliver, weight_catalog):
    print "weight_catalog ", weight_catalog

    return weight_catalog[product_type] * to_deliver


def load(drone, warehouse, product_type, to_deliver, weight_catalog, max_payload):
    total_weight = get_load_weight(product_type, to_deliver, weight_catalog)

    if drone.current_load + total_weight > max_payload:
        raise ValueError(
            'The capacity of drone was exceed. Current load: ' + str(drone.current_load) + " Intended Load: " + str(
                total_weight))

    action_cost = 1
    turns = action_cost + math.ceil(
        distance.euclidean((drone.x_possiton, drone.y_possition), (warehouse.x_possition, warehouse.y_possition)))
    command = {"drone_id": drone.id,
               "command": utils.LOAD_COMMAND,
               "target_id": warehouse.id,
               "product_type": product_type,
               "to_deliver": to_deliver}

    drone.x_possiton = warehouse.x_possition
    drone.y_possition = warehouse.y_possition
    drone.current_load = drone.current_load + total_weight

    warehouse.storage_levels[product_type] = warehouse.storage_levels[product_type] - to_deliver

    return turns, command


def load_and_deliver(drone, warehouse, order, product_type, to_deliver, weight_catalog, max_payload):
    turns = 0
    commands = []

    load_turns, load_command = load(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                                    weight_catalog=weight_catalog, max_payload=max_payload)
    commands.append(load_command)

    print "load_turns ", load_turns
    print "load_command ", load_command
    print "warehouse ", warehouse
    print "drone ", drone

    return turns, commands


def deliver_order(drone, turns, order, warehouses, weight_catalog, max_payload):
    commands = []
    turn_stock = turns

    for product_type, pending_items in enumerate(order.pending_levels):
        print "Trying to deliver ", pending_items, " of type ", product_type

        to_deliver = pending_items

        if to_deliver > 0:
            for warehouse in warehouses:
                current_stock = warehouse.storage_levels[product_type]

                if current_stock > 0:
                    if current_stock >= to_deliver:
                        turns = load_and_deliver(drone=drone, warehouse=warehouse, order=order,
                                                 product_type=product_type, to_deliver=to_deliver,
                                                 weight_catalog=weight_catalog, max_payload=max_payload)
                    elif current_stock < to_deliver:
                        pass

    return commands


def schedule_drones(problem_configuration):
    warehouses = []
    orders = []
    drone_list = []

    weight_catalog = problem_configuration["types_weight"]
    max_payload = problem_configuration["max_payload"]
    product_types = problem_configuration["product_types"]

    for id, location in enumerate(problem_configuration["warehouse_locations"]):
        warehouse = utils.Warehouse(id=id, x_possition=location[0], y_possition=location[1],
                                    storage_levels=problem_configuration["warehouse_storage"][id])
        warehouses.append(warehouse)
        print warehouse

    for id, destination in enumerate(problem_configuration["order_destinations"]):
        order = utils.OrderState(id=id, x_possition=location[0], y_possition=location[1],
                                 order_product_types=problem_configuration["order_product_types"][id],
                                 product_types=product_types)
        orders.append(order)
        print order

    intial_possition = warehouses[0].x_possition, warehouses[0].y_possition
    drones = problem_configuration["drones"]
    for id in range(drones):
        drone = utils.Drone(id=id, x_possition=intial_possition[0], y_possition=warehouses[0].y_possition,
                            current_load=0)
        drone_list.append(drone)
        print drone

    turns = problem_configuration["turns"]
    max_payload = problem_configuration["max_payload"]

    deliver_order(drone=drone_list[0], turns=turns, order=orders[0],
                  warehouses=warehouses, weight_catalog=weight_catalog, max_payload=max_payload)


if __name__ == "__main__":
    problem_configuration = io.read_configuration(test.get_input_file())

    solution = schedule_drones(problem_configuration)

    solution = test.get_solution()
    io.write_solution(solution)

    print "problem_configuration ", problem_configuration
