from .indexedgrid import IndexedGrid
from albatros.core.utils import get_initial_guess

import numpy as np


class StateGrid(IndexedGrid):
    def __init__(self, states, tau):
        super().__init__(states, tau)

        lower_bounds = np.array(list(map(lambda x: x.lower_bound, states)))
        upper_bounds = np.array(list(map(lambda x: x.upper_bound, states)))
        self.start_lower_bound = lower_bounds.copy()
        self.start_upper_bound = upper_bounds.copy()
        self.final_lower_bound = lower_bounds.copy()
        self.final_upper_bound = upper_bounds.copy()

    @property
    def states(self):
        return self._descriptors

    def _evaluate_bound_args(self, *args):
        """Extract lower and upper bound limits"""

        if len(args) == 1:
            # all bound must be set to equal
            bounds = args[0]
            assert len(bounds) == len(self.states)
            indices = np.array(range(0, len(self.states)))
            return indices, bounds, bounds
        elif len(args) == 2:
            indices = np.array(range(0, len(self.states)))
            return indices, args[0], args[1]
        else:
            raise NotImplementedError

        # TODO: Check consistency Bounds out of state bounds

    def set_start_bound(self, *args):
        indices, lower, upper = self._evaluate_bound_args(*args)
        print(indices)
        print(lower)
        self.start_lower_bound[indices] = lower
        self.start_upper_bound[indices] = upper

    def set_final_bound(self, *args):
        indices, lower, upper = self._evaluate_bound_args(*args)
        # TODO Testcase setting start bound must not change final bounds
        self.final_lower_bound[indices] = lower
        self.final_upper_bound[indices] = upper

    def write_bounds(self, z_lower_bound, z_upper_bound):
        z_lower_bound, z_upper_bound = super().write_bounds(z_lower_bound, z_upper_bound)

        z_lower_bound[self.indices[0]] = (self.start_lower_bound - self.offset_vec) * self.scaling_vec
        z_upper_bound[self.indices[0]] = (self.start_upper_bound - self.offset_vec) * self.scaling_vec

        z_lower_bound[self.indices[-1]] = (self.final_lower_bound - self.offset_vec) * self.scaling_vec
        z_upper_bound[self.indices[-1]] = (self.final_upper_bound - self.offset_vec) * self.scaling_vec

        return z_lower_bound, z_upper_bound

    def complete_initial_guess(self):
        for i in range(self.num_descriptors):
            if not np.isnan(self.values[0][i]):
                continue

            d = self._descriptors[i]
            start_guess = get_initial_guess(
                [d.lower_bound, self.start_lower_bound[i]],
                [d.upper_bound, self.start_upper_bound[i]],
            )
            final_guess = get_initial_guess(
                [d.lower_bound, self.final_lower_bound[i]],
                [d.upper_bound, self.final_upper_bound[i]],
            )
            self.values[:, i] = np.linspace(start_guess, final_guess, len(self.tau))
