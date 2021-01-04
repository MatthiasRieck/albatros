from albatros.core.core import AlbatrosError, assert_that

import numpy as np


class Bounded:
    """Enables an optimization variable to describe a lower and upper bound"""
    INF = float('inf')

    def __init__(self, lower_bound=-np.inf, upper_bound=np.inf):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def check_consistency(self):
        assert_that(
            self.lower_bound <= self.upper_bound,
            AlbatrosError(f'Lower bound "{self.lower_bound}" is higher than upper bound "{self.upper_bound}"!')
        )
        assert_that(
            self.upper_bound != -self.INF,
            AlbatrosError('Upper bound must not be equal to minus infinity!'),
        )
        assert_that(
            self.lower_bound != self.INF,
            AlbatrosError('Lower bound must not be equal to infinity!'),
        )
