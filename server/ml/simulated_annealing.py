import unittest
import numpy as np
# import config
import random
from math import exp
from ml import annealing_config
from functools import lru_cache, wraps


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)  # add assertion here


# def parameters_to_condition(position, temperature, iteration):
#     _logging.checkpoint([position, temperature, iteration])
#
#
# def condition_to_parameters(path):
#     condition = _logging.start_from_checkpoint(path)
#     position, temperature, iteration = condition
#     scheduler = get_scheduler()
#     if config.COOLING_SCHEDULE == "log_1":
#         scheduler.count = iteration + 1
#     elif config.COOLING_SCHEDULE == "log_2":
#         scheduler.count = iteration
#     return position, temperature, scheduler, iteration


def random_neighbour(position, borders):
    step = np.random.uniform(annealing_config.CLOSEST_STEP, annealing_config.FURTHER_STEP, size=len(position))
    step = np.where(np.random.random(len(step)) > 0.5, -step, step)
    position = position + step / 100 * (borders[1, :] - borders[0, :])
    sub_res = np.where(borders[0, :] < position, position, borders[0, :])
    return np.where(sub_res < borders[1, :], sub_res, borders[1, :])


def get_scheduler():
    if annealing_config.COOLING_SCHEDULE == "linear":
        # if annealing_config.linear_param <= 0:
        #     _logging.error_message("Linear param <= than 0")
        return lambda x: x - annealing_config.linear_param
    elif annealing_config.COOLING_SCHEDULE == "geom":
        # if annealing_config.geom_param >= 1:
        #     _logging.error_message("Geom param > 1")
        return lambda x: annealing_config.geom_param * x
    elif annealing_config.COOLING_SCHEDULE == "log_1":
        def log_1(x):
            log_1.count += 1
            return annealing_config.STARTING_TEMPERATURE / np.log(log_1.count)

        log_1.count = 1
        return log_1
    else:
        def log_2(x):
            log_2.count += 1
            return annealing_config.STARTING_TEMPERATURE / log_2.count

        log_2.count = 1
        return log_2


def optimize(func, start, borders, break_after_calling=0):
    scheduler = get_scheduler()
    iteration_counter = 0
    T = annealing_config.STARTING_TEMPERATURE
    position = start
    checkpoint_counter = 0
    log_steps = [position]
    calling = 0
    while T > annealing_config.STOPPING_TEMPERATURE:
        iteration_counter += 1
        for i in range(annealing_config.ITERATION_PER_TEMPERATURE):
            neighbour = random_neighbour(position, borders)
            try:
                diff = func(neighbour) - func(position)
                calling += 1
            except Exception as ex:
                # _logging.warning_message("Error during function calculation:" + str(ex))
                return

            try:
                if diff > 0 or random.random() < exp(-diff / (T + annealing_config.SAVING_DIVISION_EPSILON)):
                    position = neighbour
                    log_steps.append(position)
            except Exception as ex:
                # _logging.warning_message(f"Error during position changing:{ex}")
                continue
        # if break_after_calling > 0 and break_after_calling == calling:
        #     return position, log_steps
        T = scheduler(T)
        checkpoint_counter += 1
    return position, log_steps


if __name__ == '__main__':
    unittest.main()

import pandas as pd


def preprocessing(input_data):  # we will get data in expected format here
    x = {'Temperature_1': [120, 160], 'Time_1': 12, 'Velocity': 2, 'Temperature_2': [350, 500], 'Time_2': 2,
         'Base': 'Urea',
         'Measure_1': 'mmol', 'Mass_Base': 100, 'Reagent_1': 'Ni(NO3)2-6H2O', 'Measure_2': 'mmol',
         'Mass_Reagent_1': 100,
         'Reagent_2': 'Co(NO3)2-6H2O', 'Measure_3': 'mmol', 'Mass_Reagent_2': 100, 'Volume_solvent': 70, 'Density': 70}
    up_borders = []
    low_borders = []
    params = dict()
    for key, val in input_data.items():
        if type(val) is str:
            params[key] = val
            continue
        if type(val) is int:
            low_borders.append(0)
            up_borders.append(val)
        else:
            low_borders.append(val[0])
            up_borders.append(val[1])
    # print(borders)
    print(params)
    borders = np.array([low_borders, up_borders])
    print(borders)
    return borders, params


def np_cache(function):
    @lru_cache()
    def cached_wrapper(hashable_array):
        array = np.array(hashable_array)
        return function(array)

    @wraps(function)
    def wrapper(array):
        return cached_wrapper(tuple(array))

    # copy lru_cache attributes over too
    wrapper.cache_info = cached_wrapper.cache_info
    wrapper.cache_clear = cached_wrapper.cache_clear

    return wrapper


@np_cache
def function_call(value_vector):
    # print("hear_1")
    # print(value_vector)
    # print(function_call.params)
    value_vector = value_vector.tolist()
    value_vector.append(function_call.params["Base"])
    value_vector.append(function_call.params["Reagent_1"])
    value_vector.append(function_call.params["Reagent_2"])
    # print("hear_2")
    # print("here too")
    res = function_call.model.predict(value_vector)
    # print("calc", res)
    return res
    # return parse_expr(function_call.expr, local_dict=vars_val)
