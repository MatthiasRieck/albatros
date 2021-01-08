import numpy as np


def get_initial_guess(lower_bounds, upper_bounds):
    from albatros import AlbatrosError

    if lower_bounds is not list:
        lower_bounds = [lower_bounds]

    if upper_bounds is not list:
        upper_bounds = [upper_bounds]

    bound_values = [np.max(lower_bounds), np.min(upper_bounds)]
    bound_values = list(filter(lambda x: not np.isinf(x), bound_values))

    if len(bound_values) > 0:
        return np.mean(bound_values)
    else:
        raise AlbatrosError('Cannot generate initial guess!')
