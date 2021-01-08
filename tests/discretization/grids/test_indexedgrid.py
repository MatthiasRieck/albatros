from unittest import TestCase

from .test_basegrid import TestBaseGrid

from albatros.discretization.grids.indexedgrid import IndexedGrid
from albatros import State

import numpy as np


class TestIndexedGrid(TestBaseGrid, TestCase):
    def __init__(self, *args, indexedgrid_constructor=IndexedGrid, **kwargs):
        TestBaseGrid.__init__(self, *args, basegrid_constructor=IndexedGrid, **kwargs)
        TestCase.__init__(self, *args, **kwargs)
        self.indexedgrid_constructor = indexedgrid_constructor

    def test_init_indexedgrid(self):
        states = [
            State('a', scaling=2),
            State('b', offset=5),
        ]
        tau = np.linspace(0, 1, 101)

        grid = self.indexedgrid_constructor(states, tau)

        self.assertEqual(grid.indices.shape, (101, 2))
        self.assertTrue(np.all(grid.indices.flatten() == -1))

        self.assertEqual(grid.scalings.shape, (101, 2))
        self.assertTrue(np.all(grid.scaling_vec == np.array([2, 1])))
        for scale in grid.scalings:
            self.assertTrue(np.all(scale == np.array([2, 1])))

        self.assertEqual(grid.offsets.shape, (101, 2))
        self.assertTrue(np.all(grid.offset_vec == np.array([0, 5])))
        for offset in grid.offsets:
            self.assertTrue(np.all(offset == np.array([0, 5])))

    def test_read_from_z_indexedgrid(self):
        states = [
            State('a', scaling=2),
            State('b', offset=5),
        ]
        tau = np.linspace(0, 1, 3)

        grid = self.indexedgrid_constructor(states, tau)
        grid.indices[0] = np.array([1, 2])
        grid.indices[1] = np.array([4, 5])
        grid.indices[2] = np.array([7, 8])

        z = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

        grid.read_from_z(z)

        self.assertEqual(grid.values[0][0], 1.0)
        self.assertEqual(grid.values[0][1], 8.0)

        self.assertEqual(grid.values[1][0], 2.5)
        self.assertEqual(grid.values[1][1], 11.0)

        self.assertEqual(grid.values[2][0], 4.0)
        self.assertEqual(grid.values[2][1], 14.0)

    def test_write_to_z_indexedgrid(self):
        states = [
            State('a', scaling=2),
            State('b', offset=5),
        ]
        tau = np.linspace(0, 1, 3)

        grid = self.indexedgrid_constructor(states, tau)
        grid.indices[0] = np.array([1, 2])
        grid.indices[1] = np.array([4, 5])
        grid.indices[2] = np.array([7, 8])

        grid.values[0] = np.array([1.0, 8.0])
        grid.values[1] = np.array([2.5, 11.0])
        grid.values[2] = np.array([4.0, 14.0])

        z = np.zeros(10)

        z = grid.write_to_z(z)
        self.assertTrue(np.all(z == np.array([0., 2., 3., 0., 5., 6., 0., 8., 9., 0.])))

    def test_write_bounds_indexedgrid(self):
        states = [
            State('a', lower_bound=-2, upper_bound=5, scaling=0.1),
            State('b', lower_bound=0, upper_bound=10, scaling=0.2, offset=5),
        ]
        tau = np.linspace(0, 1, 3)

        grid = self.indexedgrid_constructor(states, tau)
        grid.indices[0] = np.array([1, 2])
        grid.indices[1] = np.array([4, 5])
        grid.indices[2] = np.array([7, 8])

        z_lb = np.zeros(10)
        z_ub = np.zeros(10)

        z_lb, z_ub = grid.write_bounds(z_lb, z_ub)

        self.assertTrue(np.all(z_lb == np.array([0., -0.2, -1., 0., -0.2, -1., 0., -0.2, -1., 0.])))
        self.assertTrue(np.all(z_ub == np.array([0., 0.5, 1., 0., 0.5, 1., 0., 0.5, 1., 0.])))

    def test_complete_initial_guess_indexedgrid(self):
        states = [
            State('a', lower_bound=-2, upper_bound=2, scaling=0.1),
            State('b', lower_bound=0, upper_bound=10, scaling=0.2, offset=5),
        ]
        tau = np.linspace(0, 1, 3)

        grid = self.indexedgrid_constructor(states, tau)

        grid.complete_initial_guess()

        self.assertEqual(grid.values[0][0], 0.0)
        self.assertEqual(grid.values[0][1], 5.0)

        self.assertEqual(grid.values[1][0], 0.0)
        self.assertEqual(grid.values[1][1], 5.0)

        self.assertEqual(grid.values[2][0], 0.0)
        self.assertEqual(grid.values[2][1], 5.0)

    def test_complete_initial_guess_partiallyset_indexedgrid(self):
        states = [
            State('a', lower_bound=-2, upper_bound=2, scaling=0.1),
            State('b', lower_bound=0, upper_bound=10, scaling=0.2, offset=5),
        ]
        tau = np.linspace(0, 1, 3)

        grid = self.indexedgrid_constructor(states, tau)

        grid.values[0][0] = 1
        grid.values[1][0] = 2
        grid.values[2][0] = 3

        grid.complete_initial_guess()

        self.assertEqual(grid.values[0][0], 1.0)
        self.assertEqual(grid.values[0][1], 5.0)

        self.assertEqual(grid.values[1][0], 2.0)
        self.assertEqual(grid.values[1][1], 5.0)

        self.assertEqual(grid.values[2][0], 3.0)
        self.assertEqual(grid.values[2][1], 5.0)
