from unittest import TestCase

from albatros.discretization.utils import assert_valid_normalized_time, interpolation_indices
from albatros.core.core import AlbatrosError

import numpy as np


class TestAssertValidNormalizedTime(TestCase):
    def test_linear(self):
        assert_valid_normalized_time(np.linspace(0, 1, 11))

    def test_scalar(self):
        assert_valid_normalized_time([0])

    def test_does_not_start_with_zeros(self):
        with self.assertRaises(AlbatrosError) as ctx:
            assert_valid_normalized_time([0.5, 1])

        self.assertEqual(
            str(ctx.exception),
            'Normalized time must start with 0.0 but starts with "0.5"!',
        )

    def test_not_strict_monotonically_increasing(self):
        with self.assertRaises(AlbatrosError) as ctx:
            assert_valid_normalized_time([0, 0.5, 0.2])

        self.assertEqual(
            str(ctx.exception),
            'Normalized must be monotonically increasing strictly!',
        )

    def test_tau_one_required_ok(self):
        assert_valid_normalized_time([0, 0.5, 1], tau_one_required=True)

    def test_tau_one_required_incorrect(self):
        with self.assertRaises(AlbatrosError) as ctx:
            assert_valid_normalized_time([0, 0.5], tau_one_required=True)

        self.assertEqual(
            str(ctx.exception),
            'Normalized time must end with 1.0 but ends with "0.5"!',
        )


class TestInterpolationIndices(TestCase):
    def test_equal(self):
        indices = interpolation_indices(np.array([0, 0.5, 1]), np.array([0, 0.5, 1]))
        self.assertTrue(all(indices == np.array([0, 1, 2])))

    def test_unequal(self):
        indices = interpolation_indices(np.linspace(0, 1, 11), np.linspace(0, 1, 6))
        self.assertTrue(all(indices == np.array([0, 0, 2, 2, 4, 4, 6, 6, 8, 8, 10])))

    def test_root_invalid_type(self):
        with self.assertRaises(AlbatrosError) as ctx:
            interpolation_indices([], np.array([0]))

        self.assertEqual(
            str(ctx.exception),
            'root_tau must be of type numpy.ndarray but is of type "list"!'
        )

    def test_sub_invalid_type(self):
        with self.assertRaises(AlbatrosError) as ctx:
            interpolation_indices(np.array([0]), [])

        self.assertEqual(
            str(ctx.exception),
            'sub_tau must be of type numpy.ndarray but is of type "list"!'
        )

    def test_not_all_sub_elements_found(self):
        with self.assertRaises(AlbatrosError) as ctx:
            interpolation_indices(np.array([0, 0.5, 1]), np.array([0, 0.6, 1]))

        self.assertEqual(
            str(ctx.exception),
            'Not all elements of sub_tau "[0.  0.6 1. ]" are found in "[0.  0.5 1. ]"!',
        )
