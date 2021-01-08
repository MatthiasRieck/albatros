from unittest import TestCase

from albatros.discretization.grids.basegrid import BaseGrid
from albatros import State

import numpy as np


class TestBaseGrid(TestCase):
    def __init__(self, *args, basegrid_constructor=BaseGrid, **kwargs):
        super().__init__(*args, **kwargs)
        self.basegrid_constructor = basegrid_constructor

    def test_init_base_grid(self):
        states = [
            State('a'),
            State('b'),
        ]
        tau = np.linspace(0, 1, 101)

        grid = self.basegrid_constructor(states, tau)

        self.assertEqual(grid.num_descriptors, 2)
        self.assertEqual(grid.num_timesteps, 101)

        self.assertEqual(grid.values.shape, (101, 2))
