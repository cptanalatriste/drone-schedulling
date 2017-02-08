"""
General-purpose utilities.
"""
import math

from scipy.spatial import distance

LOAD_COMMAND = "L"
DELIVER_COMMAND = "D"


def get_load_weight(product_type, to_deliver, weight_catalog):
    return weight_catalog[product_type] * to_deliver


def get_distance(from_x, from_y, to_x, to_y):
    return math.ceil(
        distance.euclidean((from_x, from_y), (to_x, to_y)))


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]


def validate_turns(turns, available_turns):
    if turns > available_turns:
        print "No more available turns. Action requires ", turns, " but ", available_turns, " are available"
        return False

    return True
