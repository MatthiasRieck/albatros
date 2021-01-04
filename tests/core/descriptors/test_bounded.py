from unittest import TestCase
from albatros.core.descriptors.bounded import Bounded
from albatros import AlbatrosError
import numpy as np


class TestBounded(TestCase):
    def __init__(self, *args, bounded_constructor=Bounded, **kwargs):
        super().__init__(*args, **kwargs)
        self.bounded_constructor = bounded_constructor

    def test_bounded_init(self):
        bounded = self.bounded_constructor()
        self.assertEqual(bounded.lower_bound, -np.inf)
        self.assertEqual(bounded.upper_bound, np.inf)

    def test_bounded_check_consistency(self):
        self.bounded_constructor().check_consistency()

    def test_bounded_check_consistency_bounds(self):
        bounded = self.bounded_constructor(2, 1)

        with self.assertRaises(AlbatrosError) as ctx:
            bounded.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Lower bound "2" is higher than upper bound "1"!'
        )

    def test_bounded_check_consistency_wrong_inf(self):
        b_lower = self.bounded_constructor(lower_bound=np.inf)

        with self.assertRaises(AlbatrosError) as ctx:
            b_lower.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Lower bound must not be equal to infinity!'
        )

        b_upper = self.bounded_constructor(upper_bound=-np.inf)

        with self.assertRaises(AlbatrosError) as ctx:
            b_upper.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Upper bound must not be equal to minus infinity!'
        )
