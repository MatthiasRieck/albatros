import numpy as np


class BaseGrid:
    def __init__(self, descriptors, tau):
        self._descriptors = descriptors
        self.tau = tau
        self.values = np.full((len(tau), len(descriptors)), np.nan)

    @property
    def num_descriptors(self):
        return len(self._descriptors)

    @property
    def num_timesteps(self):
        return len(self.tau)
