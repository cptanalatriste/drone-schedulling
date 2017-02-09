"""
Classes for domain representation.
"""


class ProblemContext:
    def __init__(self, total_turns, weight_catalog, max_payload):
        self.total_turns = total_turns
        self.weight_catalog = weight_catalog
        self.max_payload = max_payload


class Drone:
    def __init__(self, id, x_possition, y_possition, current_load, product_types, available_turns):
        self.id = id
        self.x_possiton = x_possition
        self.y_possition = y_possition
        self.current_load = current_load
        self.current_items = [0 for _ in range(product_types)]
        self.commands = []
        self.available_turns = available_turns

    def __str__(self):
        drone = "Drone Id " + str(self.id) + " Location: (" + str(self.x_possiton) + ", " + str(
            self.y_possition) + " Current Load: " + str(self.current_load) + ") \n"

        return drone


class OrderState:
    def __init__(self, id, x_possition, y_possition, order_product_types, product_types):
        self.id = id
        self.x_possition = x_possition
        self.y_possition = y_possition
        self.pending_levels = [0 for _ in range(product_types)]
        self.score = None

        for product_type in order_product_types:
            self.pending_levels[product_type] += 1

    def __str__(self):
        order = "Customer Id: " + str(self.id) + " Location: (" + str(self.x_possition) + ", " + str(
            self.y_possition) + ") \n"

        # order += self.get_pending_products()
        return order

    def get_pending_products(self):
        pending = ""
        for product_type, level in enumerate(self.pending_levels):
            pending += "Pending for Product Type " + str(product_type) + ": " + str(level) + "\n"

        return pending

    def is_complete(self):
        for product_type, pending in enumerate(self.pending_levels):
            if pending != 0:
                return False

        return True


class Warehouse:
    def __init__(self, id, x_possition, y_possition, storage_levels):
        self.id = id
        self.x_possition = x_possition
        self.y_possition = y_possition
        self.storage_levels = storage_levels

    def __str__(self):
        warehouse = "Warehouse Id: " + str(self.id) + " Location: (" + str(self.x_possition) + ", " + str(
            self.y_possition) + ")\n"

        # warehouse += self.get_storage_levels()
        return warehouse

    def get_storage_levels(self):
        levels = ""
        for product_type, level in enumerate(self.storage_levels):
            levels += "Level for Product Type " + str(product_type) + ": " + str(level) + "\n"

        return levels


def get_orders(problem_configuration):
    product_types = problem_configuration["product_types"]
    orders = []

    for id, destination in enumerate(problem_configuration["order_destinations"]):
        order = OrderState(id=id, x_possition=destination[0], y_possition=destination[1],
                           order_product_types=problem_configuration["order_product_types"][id],
                           product_types=product_types)
        orders.append(order)
        # print order

    return orders


def get_domain_objects(problem_configuration):
    warehouses = []
    orders = get_orders(problem_configuration)
    drone_list = []

    for id, location in enumerate(problem_configuration["warehouse_locations"]):
        warehouse = Warehouse(id=id, x_possition=location[0], y_possition=location[1],
                              storage_levels=problem_configuration["warehouse_storage"][id])
        warehouses.append(warehouse)
        # print warehouse

    intial_possition = warehouses[0].x_possition, warehouses[0].y_possition
    drones = problem_configuration["drones"]
    turns = problem_configuration["turns"]
    product_types = problem_configuration["product_types"]

    for id in range(drones):
        drone = Drone(id=id, x_possition=intial_possition[0], y_possition=warehouses[0].y_possition,
                      current_load=0, product_types=product_types, available_turns=turns)
        drone_list.append(drone)
        # print drone

    max_payload = problem_configuration["max_payload"]
    weight_catalog = problem_configuration["types_weight"]
    problem_context = ProblemContext(max_payload=max_payload, weight_catalog=weight_catalog, total_turns=turns)

    return problem_context, warehouses, drone_list, orders
