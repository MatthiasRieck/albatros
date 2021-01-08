from unittest import TestCase

from .test_indexedgrid import TestIndexedGrid

from albatros.discretization.grids import StateGrid
from albatros import State

import numpy as np


class TestControlGrid(TestIndexedGrid, TestCase):
    def __init__(self, *args, **kwargs):
        TestIndexedGrid.__init__(self, *args, indexedgrid_constructor=StateGrid, **kwargs)
        TestCase.__init__(self, *args, **kwargs)

    def test_init_stategrid(self):
        states = [
            State('a', lower_bound=-1, upper_bound=2),
            State('b', lower_bound=-2, upper_bound=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = StateGrid(states, tau)
        self.assertEqual(grid.states, states)

        self.assertEqual(grid.start_lower_bound[0], -1)
        self.assertEqual(grid.start_upper_bound[0], 2)
        self.assertEqual(grid.start_lower_bound[1], -2)
        self.assertEqual(grid.start_upper_bound[1], 5)

        self.assertEqual(grid.final_lower_bound[0], -1)
        self.assertEqual(grid.final_upper_bound[0], 2)
        self.assertEqual(grid.final_lower_bound[1], -2)
        self.assertEqual(grid.final_upper_bound[1], 5)

    def test_set_start_bounds_equal_stategrid(self):
        states = [
            State('a', lower_bound=-1, upper_bound=2),
            State('b', lower_bound=-2, upper_bound=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = StateGrid(states, tau)

        grid.set_start_bound(np.array([0, 1]))
        self.assertEqual(grid.start_lower_bound[0], 0)
        self.assertEqual(grid.start_upper_bound[0], 0)
        self.assertEqual(grid.start_lower_bound[1], 1)
        self.assertEqual(grid.start_upper_bound[1], 1)

    def test_set_start_bounds_low_high_stategrid(self):
        states = [
            State('a', lower_bound=-1, upper_bound=2),
            State('b', lower_bound=-2, upper_bound=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = StateGrid(states, tau)

        grid.set_start_bound(np.array([0, 1]), np.array([1, 4]))
        self.assertEqual(grid.start_lower_bound[0], 0)
        self.assertEqual(grid.start_upper_bound[0], 1)
        self.assertEqual(grid.start_lower_bound[1], 1)
        self.assertEqual(grid.start_upper_bound[1], 4)

    def test_set_final_bounds_equal_stategrid(self):
        states = [
            State('a', lower_bound=-1, upper_bound=2),
            State('b', lower_bound=-2, upper_bound=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = StateGrid(states, tau)

        grid.set_final_bound(np.array([0, 1]))
        self.assertEqual(grid.final_lower_bound[0], 0)
        self.assertEqual(grid.final_upper_bound[0], 0)
        self.assertEqual(grid.final_lower_bound[1], 1)
        self.assertEqual(grid.final_upper_bound[1], 1)

    def test_set_final_bounds_low_high_stategrid(self):
        states = [
            State('a', lower_bound=-1, upper_bound=2),
            State('b', lower_bound=-2, upper_bound=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = StateGrid(states, tau)

        grid.set_final_bound(np.array([0, 1]), np.array([1, 4]))
        self.assertEqual(grid.final_lower_bound[0], 0)
        self.assertEqual(grid.final_upper_bound[0], 1)
        self.assertEqual(grid.final_lower_bound[1], 1)
        self.assertEqual(grid.final_upper_bound[1], 4)
