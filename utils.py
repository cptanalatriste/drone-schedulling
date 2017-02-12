"""
General-purpose utilities.
"""
import math

from scipy.spatial import distance

LOAD_COMMAND = "L"
DELIVER_COMMAND = "D"
LONE_RANGER = 0


def get_schedule_results(drones, orders):
    finished_orders = [order.score for order in orders if order.score is not None]
    total_score = sum(finished_orders)
    print "Total score: ", total_score, " from ", len(finished_orders), "  orders finished. Total orders: ", len(orders)

    commands = []
    for drone in drones:
        commands += drone.commands

    return total_score, commands


def get_load_weight(product_type, to_deliver, weight_catalog):
    return weight_catalog[product_type] * to_deliver


def get_distance(from_x, from_y, to_x, to_y):
    return math.ceil(
        distance.euclidean((from_x, from_y), (to_x, to_y)))


def split_and_cast(line):
    return [int(string_value) for string_value in line.split(" ")]
