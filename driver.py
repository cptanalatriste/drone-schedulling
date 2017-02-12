"""
This is the file that will coordinate the execution of the solution
"""

import io
import optimizer

DEBUG = False


def schedule_drones(problem_configuration):
    best_score, command_list = optimizer.random_optimizer(problem_configuration)

    print "Best Score: ", best_score
    return command_list


def main():
    # problem_configuration = io.read_configuration("inputs/busy_day.in")
    # problem_configuration = io.read_configuration("inputs/mother_of_all_warehouses.in")
    # problem_configuration = io.read_configuration("inputs/redundancy.in")

    problem_configuration = io.read_configuration("task/example_input.txt")

    solution = schedule_drones(problem_configuration)
    io.write_solution(solution)


if __name__ == "__main__":
    main()
