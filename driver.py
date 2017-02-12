"""
This is the file that will coordinate the execution of the solution
"""
import dronesim
import io
import optimizer

DEBUG = False


def schedule_drones(problem_configuration):
    best_score, command_list = optimizer.random_optimizer(problem_configuration=problem_configuration,
                                                             strategy=dronesim.egalitarian_strategy)

    print "Best Score: ", best_score
    return command_list


def main():
    input_instance = "busy_day"
    # input_instance = "example_input"

    # problem_configuration = io.read_configuration("inputs/mother_of_all_warehouses.in")
    # problem_configuration = io.read_configuration("inputs/redundancy.in")

    problem_configuration = io.read_configuration(input_instance)
    solution = schedule_drones(problem_configuration)
    io.write_solution(solution, input_instance)


if __name__ == "__main__":
    main()
