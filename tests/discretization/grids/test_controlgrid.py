from unittest import TestCase

from .test_indexedgrid import TestIndexedGrid

from albatros.discretization.grids import ControlGrid
from albatros import Control

import numpy as np


class TestControlGrid(TestIndexedGrid, TestCase):
    def __init__(self, *args, **kwargs):
        TestIndexedGrid.__init__(self, *args, indexedgrid_constructor=ControlGrid, **kwargs)
        TestCase.__init__(self, *args, **kwargs)

    def test_init_controlgrid(self):
        controls = [
            Control('a'),
            Control('b'),
        ]
        tau = np.linspace(0, 1, 101)

        grid = ControlGrid(controls, tau)
        self.assertIsNone(grid.interp_indices)
        self.assertIsNone(grid.interp_values)
        self.assertEqual(grid.controls, controls)
