"""
This is the file that will coordinate the execution of the solution
"""
import utils
import test
import io
import domain


def get_load_cost(drone, warehouse, product_type, to_deliver, weight_catalog, max_payload, available_turns):
    if warehouse.storage_levels[product_type] < to_deliver:
        print "Cannot get ", to_deliver, " items of product type ", product_type, " from warehouse ", warehouse.id
        return None

    total_weight = utils.get_load_weight(product_type, to_deliver, weight_catalog)
    if drone.current_load + total_weight > max_payload:
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

    if not utils.validate_turns(turns, available_turns):
        return None

    return turns


def get_deliver_cost(drone, order, available_turns):
    action_cost = 1
    turns = action_cost + utils.get_distance(drone.x_possiton, drone.y_possition, order.x_possition, order.y_possition)

    if not utils.validate_turns(turns, available_turns):
        return None

    for product_type, items in enumerate(drone.current_items):
        if order.pending_levels[product_type] < items:
            print "Order ", order.id, " does not require ", items, " of product ", product_type, " only ", \
                order.pending_levels[product_type]
            return None

    return turns


def load(drone, warehouse, product_type, to_deliver, weight_catalog, max_payload, available_turns):
    load_cost = get_load_cost(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                              weight_catalog=weight_catalog, max_payload=max_payload, available_turns=available_turns)
    if load_cost is not None:
        drone.commands.append({"drone_id": drone.id,
                               "command": utils.LOAD_COMMAND,
                               "target_id": warehouse.id,
                               "product_type": product_type,
                               "number_items": to_deliver})
        drone.x_possiton = warehouse.x_possition
        drone.y_possition = warehouse.y_possition
        drone.current_load = drone.current_load + utils.get_load_weight(product_type, to_deliver, weight_catalog)

        drone.current_items[product_type] += to_deliver

        warehouse.storage_levels[product_type] = warehouse.storage_levels[product_type] - to_deliver

    return load_cost


def deliver(drone, order, available_turns, product_type, to_deliver):
    deliver_cost = get_deliver_cost(drone=drone, order=order, available_turns=available_turns)
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

        order.pending_levels[product_type] = order.pending_levels[product_type] - to_deliver

    return deliver_cost


def load_and_deliver(drone, warehouse, order, product_type, to_deliver, weight_catalog, max_payload, available_turns):
    turns = None
    load_turns = load(drone=drone, warehouse=warehouse, product_type=product_type, to_deliver=to_deliver,
                      weight_catalog=weight_catalog, max_payload=max_payload, available_turns=available_turns)

    if load_turns is not None:
        deliver_turns = deliver(drone=drone, order=order, product_type=product_type, to_deliver=to_deliver,
                                available_turns=available_turns)

        if deliver_turns is not None:
            turns = load_turns + deliver_turns

    print "Total cost ", turns
    print "Warehouse ", warehouse
    print "Drone ", drone
    print "Order ", order

    return turns


def deliver_order(drone, turns, order, warehouses, weight_catalog, max_payload):
    turn_stock = turns

    for product_type, pending_items in enumerate(order.pending_levels):
        print "Trying to deliver ", pending_items, " of type ", product_type, " from order ", order.id, \
            ". Pending turns: ", turn_stock

        to_deliver = pending_items

        if to_deliver > 0 and turn_stock > 0:
            for warehouse in warehouses:
                current_stock = warehouse.storage_levels[product_type]

                if current_stock > 0:
                    if current_stock >= to_deliver:
                        turns = load_and_deliver(drone=drone, warehouse=warehouse, order=order,
                                                 product_type=product_type, to_deliver=to_deliver,
                                                 weight_catalog=weight_catalog, max_payload=max_payload,
                                                 available_turns=turn_stock)
                        to_deliver = 0
                    elif current_stock < to_deliver:
                        turns = load_and_deliver(drone=drone, warehouse=warehouse, order=order,
                                                 product_type=product_type, to_deliver=current_stock,
                                                 weight_catalog=weight_catalog, max_payload=max_payload,
                                                 available_turns=turn_stock)
                        to_deliver = to_deliver - current_stock

                    turn_stock -= turns

    return turn_stock


def schedule_drones(problem_configuration):
    warehouses = []
    orders = []
    drone_list = []

    weight_catalog = problem_configuration["types_weight"]
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
    for id in range(drones):
        drone = domain.Drone(id=id, x_possition=intial_possition[0], y_possition=warehouses[0].y_possition,
                             current_load=0, product_types=product_types)
        drone_list.append(drone)
        print drone

    turns = problem_configuration["turns"]
    max_payload = problem_configuration["max_payload"]

    lone_ranger = drone_list[0]
    turns_left = turns

    for order in orders:
        pending_turns = deliver_order(drone=lone_ranger, turns=turns_left, order=order,
                                      warehouses=warehouses, weight_catalog=weight_catalog, max_payload=max_payload)
        turns_left = pending_turns

    command_list = []
    for drone in drone_list:
        command_list += drone.commands

    return command_list


if __name__ == "__main__":
    problem_configuration = io.read_configuration(test.get_input_file())

    solution = schedule_drones(problem_configuration)

    io.write_solution(solution)
