from unittest import TestCase
from albatros.core.descriptors.scaled import Scaled

from albatros import AlbatrosError

import numpy as np


class TestScaled(TestCase):
    def __init__(self, *args, scaled_constructor=Scaled, **kwargs):
        super().__init__(*args, **kwargs)
        self.scaled_constructor = scaled_constructor

    def test_scaled_init(self):
        scaled = self.scaled_constructor()
        self.assertEqual(scaled.scaling, 1.)
        self.assertEqual(scaled.offset, 0.)

    def test_scaled_check_consistency(self):
        self.scaled_constructor().check_consistency()

    def test_scaled_check_consistency_scaling(self):
        s_scaling = self.scaled_constructor(scaling=0)

        with self.assertRaises(AlbatrosError) as ctx:
            s_scaling.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Scaling must not be equal to zero!',
        )

    def test_scaled_check_consistency_offset_inf(self):
        s_offset_inf = self.scaled_constructor(offset=np.inf)

        with self.assertRaises(AlbatrosError) as ctx:
            s_offset_inf.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Offset must not be equal to infinity!',
        )

        s_offset_m_inf = self.scaled_constructor(offset=-np.inf)

        with self.assertRaises(AlbatrosError) as ctx:
            s_offset_m_inf.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Offset must not be equal to infinity!',
        )
