"""
This is the file that will coordinate the execution of the solution
"""
import math

import utils
import io
import domain


def get_deliver_cost(drone, order):
    action_cost = 1
    turns = action_cost + utils.get_distance(drone.x_possiton, drone.y_possition, order.x_possition, order.y_possition)

    if not utils.validate_turns(turns, drone.available_turns):
        return None

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
            total_weight)
        return None

    if warehouse.storage_levels[product_type] < to_deliver:
        print "Warehouse ", warehouse.id, " stock of product type ", product_type, " is only ", \
            warehouse.storage_levels[product_type], " . Cannot load ", to_deliver
        return None

    action_cost = 1
    turns = action_cost + utils.get_distance(drone.x_possiton, drone.y_possition, warehouse.x_possition,
                                             warehouse.y_possition)

    if not utils.validate_turns(turns, drone.available_turns):
        return None

    return turns


def load(drone, warehouse, product_type, to_deliver, problem_context):
    load_cost = get_load_cost(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                              problem_context=problem_context)
    if load_cost is not None:
        drone.commands.append({"drone_id": drone.id,
                               "command": utils.LOAD_COMMAND,
                               "target_id": warehouse.id,
                               "product_type": product_type,
                               "number_items": to_deliver})
        drone.x_possiton = warehouse.x_possition
        drone.y_possition = warehouse.y_possition
        drone.current_load = drone.current_load + utils.get_load_weight(product_type, to_deliver,
                                                                        problem_context.weight_catalog)

        drone.current_items[product_type] += to_deliver
        drone.available_turns -= load_cost

        warehouse.storage_levels[product_type] = warehouse.storage_levels[product_type] - to_deliver

    return load_cost


def deliver(drone, order, product_type, to_deliver):
    deliver_cost = get_deliver_cost(drone=drone, order=order)
    if deliver_cost is not None:
        drone.commands.append({"drone_id": drone.id,
                               "command": utils.DELIVER_COMMAND,
                               "target_id": order.id,
                               "product_type": product_type,
                               "number_items": to_deliver})
        drone.x_possiton = order.x_possition
        drone.y_possition = order.y_possition
        drone.current_load = 0
        drone.current_items = [0 for _ in drone.current_items]
        drone.available_turns -= deliver_cost

        order.pending_levels[product_type] = order.pending_levels[product_type] - to_deliver

    return deliver_cost


def load_and_deliver(drone, warehouse, order, product_type, to_deliver, problem_context):
    turns = None
    load_turns = load(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                      problem_context=problem_context)

    if load_turns is not None:
        turns = load_turns
        deliver_turns = deliver(drone=drone, order=order, product_type=product_type, to_deliver=to_deliver)

        if deliver_turns is not None:
            turns += deliver_turns

    print "Total cost ", turns
    print "Warehouse ", warehouse
    print "Drone ", drone
    print "Order ", order

    return turns


def deliver_order(drone, turns, order, warehouses, problem_context):
    turn_stock = turns

    for product_type, pending_items in enumerate(order.pending_levels):

        to_deliver = pending_items

        if to_deliver > 0 and turn_stock > 0:
            print "Trying to deliver ", pending_items, " of type ", product_type, " from order ", order.id, \
                ". Pending turns: ", turn_stock

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


def schedule_drones(problem_configuration):
    warehouses = []
    orders = []
    drone_list = []

    product_types = problem_configuration["product_types"]

    for id, location in enumerate(problem_configuration["warehouse_locations"]):
        warehouse = domain.Warehouse(id=id, x_possition=location[0], y_possition=location[1],
                                     storage_levels=problem_configuration["warehouse_storage"][id])
        warehouses.append(warehouse)
        print warehouse

    for id, destination in enumerate(problem_configuration["order_destinations"]):
        order = domain.OrderState(id=id, x_possition=destination[0], y_possition=destination[1],
                                  order_product_types=problem_configuration["order_product_types"][id],
                                  product_types=product_types)
        orders.append(order)
        print order

    intial_possition = warehouses[0].x_possition, warehouses[0].y_possition
    drones = problem_configuration["drones"]
    turns = problem_configuration["turns"]

    for id in range(drones):
        drone = domain.Drone(id=id, x_possition=intial_possition[0], y_possition=warehouses[0].y_possition,
                             current_load=0, product_types=product_types, available_turns=turns)
        drone_list.append(drone)
        print drone

    max_payload = problem_configuration["max_payload"]
    weight_catalog = problem_configuration["types_weight"]

    lone_ranger = drone_list[0]
    turns_left = turns

    problem_context = domain.ProblemContext(max_payload=max_payload, weight_catalog=weight_catalog, total_turns=turns)

    for order in orders:
        pending_turns = deliver_order(drone=lone_ranger, turns=turns_left, order=order,
                                      warehouses=warehouses, problem_context=problem_context)
        turns_left = pending_turns

    finished_orders = [order.score for order in orders if order.score is not None]
    total_score = sum(finished_orders)
    print "Total score: ", total_score, " from ", len(finished_orders), "  orders finished. Total orders: ", len(orders)

    command_list = []
    for drone in drone_list:
        command_list += drone.commands

    return command_list


if __name__ == "__main__":
    problem_configuration = io.read_configuration("inputs/redundancy.in")

    # problem_configuration = io.read_configuration("task/example_input.txt")

    solution = schedule_drones(problem_configuration)

    io.write_solution(solution)
