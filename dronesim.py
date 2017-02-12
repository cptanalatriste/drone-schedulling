"""
Simulating drone delivery
"""

import collections
import Queue

import math

import command
import driver
import utils

START_ACTION = "start"
TO_WAREHOUSE_ACTION = "to warehouse"
TO_CLIENT_ACTION = "to client"

Event = collections.namedtuple("Event", "time drone action turns")


def drone_process(drone, orders, warehouses, problem_context, start_time=0):
    time = yield Event(start_time, drone.id, START_ACTION, 0)

    for order in orders:
        if driver.DEBUG:
            print "Drone ", drone.id, " trying to deliver order ", order

        for product_type, pending_items in enumerate(order.pending_levels):
            to_deliver = pending_items

            if to_deliver > 0:

                for warehouse in warehouses:
                    current_stock = warehouse.storage_levels[product_type]

                    if current_stock > 0:
                        if current_stock >= to_deliver:
                            items_to_transport = to_deliver
                        elif current_stock < to_deliver:
                            items_to_transport = current_stock

                        load_turns = command.get_load_cost(drone=drone, warehouse=warehouse, product_type=product_type,
                                                           to_deliver=items_to_transport,
                                                           problem_context=problem_context)
                        if load_turns is not None:
                            drone.load(warehouse=warehouse, product_type=product_type, to_deliver=to_deliver)
                            time = yield Event(time, drone.id, TO_WAREHOUSE_ACTION, load_turns)
                            command.load_successfull(drone=drone, warehouse=warehouse, product_type=product_type,
                                                     to_deliver=items_to_transport,
                                                     problem_context=problem_context)

                            deliver_turns = command.get_deliver_cost(drone=drone, order=order)
                            if deliver_turns is not None:
                                drone.deliver(order=order, product_type=product_type, to_deliver=to_deliver)
                                time = yield Event(time, drone.id, TO_CLIENT_ACTION, deliver_turns)
                                command.deliver_successfull(drone=drone, order=order, product_type=product_type,
                                                            to_deliver=items_to_transport)

                                to_deliver -= items_to_transport

        if order.is_complete():
            order.score = math.ceil(
                (problem_context.total_turns - time) / float(problem_context.total_turns) * 100)
            print "Order ", order.id, " was delivered by drone ", drone.id, " at turn ", time, ". Score: ", order.score


class Simulator:
    def __init__(self, process_list):
        self.events = Queue.PriorityQueue()
        self.process_list = process_list

    def run(self, total_turns):
        for drone in self.process_list:
            start_event = next(drone)
            self.events.put(start_event)

        current_turn = 0
        while current_turn < total_turns:
            if self.events.empty():
                print "No more events! At turn ", current_turn
                break

            current_event = self.events.get()
            current_turn, drone_id, removed_event, event_turns = current_event

            if driver.DEBUG:
                print "Drone: ", drone_id, " Event ", removed_event, " at turn ", current_turn

            active_drone_process = self.process_list[drone_id]
            next_event_turn = current_turn + event_turns

            try:
                next_event = active_drone_process.send(next_event_turn)
            except StopIteration:
                print "No more events for drone ", drone_id
                # del self.process_list[drone_id]
            else:
                self.events.put(next_event)
        else:
            print "No more simulation turns. Pending events: ", self.events.qsize()


def lone_ranger_simulation(drones, orders, warehouses, problem_context):
    print "Starting lone-ranger simulation ..."

    process_list = []
    total_turns = problem_context.total_turns

    lone_ranger = drones[0]
    process_list.append(
        drone_process(drone=lone_ranger, orders=orders, warehouses=warehouses, problem_context=problem_context))

    simulation = Simulator(process_list=process_list)
    simulation.run(total_turns=total_turns)

    return utils.get_schedule_results([lone_ranger], orders)


def egalitarian_strategy(drones, orders, warehouses, problem_context):
    print "Starting egalitarian simulation ..."

    process_list = []
    total_turns = problem_context.total_turns

    tasks_per_drone = len(orders) / len(drones)
    drone_tasks = [orders[start: start + tasks_per_drone] for start in xrange(0, len(orders), tasks_per_drone)]

    for index, drone in enumerate(drones):
        process_list.append(drone_process(drone=drone, orders=drone_tasks[index], warehouses=warehouses,
                                          problem_context=problem_context))

    simulation = Simulator(process_list=process_list)
    simulation.run(total_turns=total_turns)
    return utils.get_schedule_results(drones, orders)
