from unittest import TestCase

from .test_basegrid import TestBaseGrid

from albatros.discretization.grids.valuegrid import ValueGrid
from albatros import State

import numpy as np


class TestValueGrid(TestBaseGrid, TestCase):
    def __init__(self, *args, valuegrid_constructor=ValueGrid, **kwargs):
        TestBaseGrid.__init__(self, *args, basegrid_constructor=ValueGrid, **kwargs)
        TestCase.__init__(self, *args, **kwargs)
        self.valuegrid_constructor = valuegrid_constructor

    def test_init_valuegrid(self):
        states = [
            State('a'),
            State('b'),
        ]
        tau = np.linspace(0, 1, 101)

        grid = self.valuegrid_constructor(states, tau)

        self.assertIsNone(grid.jacobians)
