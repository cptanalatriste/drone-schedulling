"""
File operations module
"""

import utils

INPUT_DIR = "inputs/"
INPUT_EXTENSION = ".in"


def read_configuration(file_name):
    warehouse_data_items = 2
    order_data_items = 3

    warehouse_locations = []
    warehouse_storage = []
    order_destinations = []

    order_items = []
    order_product_types = []

    warehouse_section_start = None
    warehouse_section_end = None

    path = INPUT_DIR + file_name + INPUT_EXTENSION
    with open(path) as file:
        for line_number, line in enumerate(file):

            if line_number == 0:
                rows, columns, drones, turns, max_payload = utils.split_and_cast(line)
                print "rows ", rows, " columns ", columns, " drones ", drones, " turns ", \
                    turns, " max_payload ", max_payload
            elif line_number == 1:
                product_types = int(line)
                print "product_types ", product_types
            elif line_number == 2:
                types_weight = utils.split_and_cast(line)
                print "types_weight ", types_weight
            elif line_number == 3:
                warehouses = int(line)
                print "warehouses ", warehouses
                warehouse_section_start = 4
                warehouse_section_end = line_number + warehouses * 2
                order_section_start = warehouse_section_end + 1
            elif warehouse_section_start <= line_number <= warehouse_section_end:

                if line_number % warehouse_data_items == 0:
                    warehouse_locations.append(utils.split_and_cast(line))
                else:
                    warehouse_storage.append(utils.split_and_cast(line))
            elif line_number == order_section_start:
                orders = int(line)
                print "orders ", orders
            elif line_number > order_section_start:
                relative_possition = line_number - order_section_start

                if relative_possition % order_data_items == 1:
                    order_destinations.append(utils.split_and_cast(line))
                elif relative_possition % order_data_items == 2:
                    order_items.append(int(line))
                elif relative_possition % order_data_items == 0:
                    order_product_types.append(utils.split_and_cast(line))

    print "warehouse_locations ", warehouse_locations
    print "warehouse_storage ", warehouse_storage
    print "order_destinations ", order_destinations
    print "order_items ", order_items
    print "order_product_types ", order_product_types

    return {"file_name": file_name,
            "rows": rows,
            "columns": columns,
            "drones": drones,
            "turns": turns,
            "max_payload": max_payload,
            "product_types": product_types,
            "types_weight": types_weight,
            "warehouses": warehouses,
            "orders": orders,
            "warehouse_locations": warehouse_locations,
            "warehouse_storage": warehouse_storage,
            "order_destinations": order_destinations,
            "order_items": order_items,
            "order_product_types": order_product_types}


def write_solution(solution, output_file="solution"):
    solution_as_string = str(len(solution)) + "\n"

    for command in solution:
        solution_as_string += " ".join([str(int_value) for int_value in [command["drone_id"], command["command"],
                                                                         command["target_id"], command["product_type"],
                                                                         command["number_items"]]]) + "\n"

    # print "solution_as_string: \n", solution_as_string

    path = output_file + ".out"
    with open(path, "w") as file:
        file.write(solution_as_string)

    print "Solution written to file ", path
