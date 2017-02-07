"""
General-purpose utilities.
"""

LOAD_COMMAND = "L"
DELIVER_COMMAND = "D"


class Drone:
    def __init__(self, id, x_possition, y_possition, current_load):
        self.id = id
        self.x_possiton = x_possition
        self.y_possition = y_possition
        self.current_load = current_load

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

        for product_type in order_product_types:
            self.pending_levels[product_type] += 1

    def __str__(self):
        order = "Customer Id: " + str(self.id) + " Location: (" + str(self.x_possition) + ", " + str(
            self.y_possition) + ") \n"

        for product_type, level in enumerate(self.pending_levels):
            order += "Pending for Product Type " + str(product_type) + ": " + str(level) + "\n"

        return order


class Warehouse:
    def __init__(self, id, x_possition, y_possition, storage_levels):
        self.id = id
        self.x_possition = x_possition
        self.y_possition = y_possition
        self.storage_levels = storage_levels

    def __str__(self):
        warehouse = "Warehouse Id: " + str(self.id) + " Location: (" + str(self.x_possition) + ", " + str(
            self.y_possition) + ")\n"

        for product_type, level in enumerate(self.storage_levels):
            warehouse += "Level for Product Type " + str(product_type) + ": " + str(level) + "\n"

        return warehouse


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]
