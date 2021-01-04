from unittest import TestCase

from .test_bounded import TestBounded
from .test_scaled import TestScaled
from .test_named import TestNamed
from .test_fixable import TestFixable

from albatros import Parameter, AlbatrosError

import numpy as np


class TestState(TestNamed, TestBounded, TestScaled, TestFixable, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda name, *ar, **kwar: Parameter(name, 5, *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=func)

        func = lambda *ar, **kwar: Parameter('state', 5, *ar, **kwar)  # noqa: E731
        TestBounded.__init__(self, bounded_constructor=func)
        TestScaled.__init__(self, *args, **kwargs, scaled_constructor=func)
        TestFixable.__init__(self, *args, **kwargs, fixable_constructor=func)
        TestCase.__init__(self, *args, **kwargs)

    def test_parameter_default_value(self):
        param = Parameter('param')
        self.assertTrue(np.isnan(param.value))
        self.assertTrue(np.isnan(param.index))

        param = Parameter('param', 5)
        self.assertEqual(param.value, 5)

    def test_parameter_value_is_not_numeric(self):
        param = Parameter('param', 'p')

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Parameter value "param" must be numeric but is "str"!'
        )

    def test_parameter_value_is_nan(self):
        param = Parameter('param')

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Parameter "param" has invalid value "nan"!'
        )

    def test_parameter_value_is_fixed_inf(self):
        param = Parameter('param', np.inf, is_fixed=True)

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Parameter "param" has invalid value "inf"!'
        )

    def test_parameter_value_is_fixed_nan(self):
        param = Parameter('param', np.nan, is_fixed=True)

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Parameter "param" has invalid value "nan"!'
        )

    def test_parameter_value_is_below_lower_bound(self):
        param = Parameter('param', -5, lower_bound=0)

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Value "-5.0" of parameter "param" is below lower bound "0"!'
        )

    def test_parameter_value_is_above_upper_bound(self):
        param = Parameter('param', 5, upper_bound=0)

        with self.assertRaises(AlbatrosError) as ctx:
            param.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Value "5.0" of parameter "param" is higher than upper bound "0"!'
        )

    def test_parameter_initial_guess_upper_bound(self):
        param = Parameter('param', upper_bound=1)
        param.complete_initial_guess()
        self.assertEqual(param.value, 1)

    def test_parameter_initial_guess_lower_bound(self):
        param = Parameter('param', lower_bound=1)
        param.complete_initial_guess()
        self.assertEqual(param.value, 1)

    def test_parameter_initial_guess_lower_upper_bound(self):
        param = Parameter('param', lower_bound=1, upper_bound=2)
        param.complete_initial_guess()
        self.assertEqual(param.value, 1.5)

    def test_parameter_initial_guess_cannot_be_generated(self):
        param = Parameter('param')

        with self.assertRaises(AlbatrosError) as ctx:
            param.complete_initial_guess()

        self.assertEqual(
            str(ctx.exception),
            'The initial guess for parameter "param" cannot automatically generated!'
        )

    def test_parameter_initial_guess_is_fixed(self):
        param = Parameter('param', is_fixed=True)
        param.complete_initial_guess()

    def test_parameter_initial_guess_value(self):
        param = Parameter('param', 5)
        param.complete_initial_guess()
