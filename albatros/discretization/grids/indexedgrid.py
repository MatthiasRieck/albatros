from .basegrid import BaseGrid
from albatros.core.utils import get_initial_guess

import numpy as np


class IndexedGrid(BaseGrid):
    """Container that holds a time of an optimization value"""

    def __init__(self, descriptors, tau):
        super().__init__(descriptors, tau)

        self.indices = np.full((len(tau), len(descriptors)), -1, dtype=int)

        self.scaling_vec = np.array(list(map(lambda x: x.scaling, self._descriptors))).reshape(1, len(descriptors))
        self.scalings = np.tile(self.scaling_vec, [len(tau), 1])

        self.offset_vec = np.array(list(map(lambda x: x.offset, self._descriptors))).reshape(1, len(descriptors))
        self.offsets = np.tile(self.offset_vec, [len(tau), 1])

    def read_from_z(self, z):
        self.values = (z[self.indices] / self.scalings) + self.offsets

    def write_to_z(self, z):
        z[self.indices] = (self.values - self.offsets) * self.scalings
        return z

    def write_bounds(self, z_lower_bound, z_upper_bound):
        lb_vec = np.array(list(map(lambda x: x.lower_bound, self._descriptors))).reshape(1, self.num_descriptors)
        lb_matrix = np.tile(lb_vec, [self.num_timesteps, 1])
        z_lower_bound[self.indices] = (lb_matrix - self.offsets) * self.scalings

        ub_vec = np.array(list(map(lambda x: x.upper_bound, self._descriptors))).reshape(1, self.num_descriptors)
        ub_matrix = np.tile(ub_vec, [self.num_timesteps, 1])
        z_upper_bound[self.indices] = (ub_matrix - self.offsets) * self.scalings

        return z_lower_bound, z_upper_bound

    def complete_initial_guess(self):
        # TODO: Handle different for stategrid
        for i in range(self.num_descriptors):
            if not np.isnan(self.values[0][i]):
                continue

            d = self._descriptors[i]
            guess = get_initial_guess(d.lower_bound, d.upper_bound)
            self.values[:, i] = guess
