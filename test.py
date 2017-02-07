"""
Test input for program verification
"""
import utils


def get_input_file():
    return "example_input.txt"


def get_solution():
    return [{"drone_id": 0,
             "command": utils.LOAD_COMMAND,
             "target_id": 0,
             "product_type": 0,
             "number_items": 1},
            {"drone_id": 0,
             "command": utils.LOAD_COMMAND,
             "target_id": 0,
             "product_type": 1,
             "number_items": 1},
            {"drone_id": 0,
             "command": utils.DELIVER_COMMAND,
             "target_id": 0,
             "product_type": 0,
             "number_items": 1},
            {"drone_id": 0,
             "command": utils.LOAD_COMMAND,
             "target_id": 1,
             "product_type": 2,
             "number_items": 1},
            {"drone_id": 0,
             "command": utils.DELIVER_COMMAND,
             "target_id": 0,
             "product_type": 2,
             "number_items": 1},
            {"drone_id": 1,
             "command": utils.LOAD_COMMAND,
             "target_id": 1,
             "product_type": 2,
             "number_items": 1},
            {"drone_id": 1,
             "command": utils.DELIVER_COMMAND,
             "target_id": 2,
             "product_type": 2,
             "number_items": 1},
            {"drone_id": 1,
             "command": utils.LOAD_COMMAND,
             "target_id": 0,
             "product_type": 0,
             "number_items": 1},
            {"drone_id": 1,
             "command": utils.DELIVER_COMMAND,
             "target_id": 1,
             "product_type": 0,
             "number_items": 1}
            ]
