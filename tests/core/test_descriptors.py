from unittest import TestCase

from albatros.core.descriptors import Bounded, Scaled, Named, _NamedScaledBounded, Cost
from albatros.core.descriptors import State, Control, Parameter, Constraint
from albatros.core.core import AlbatrosError


_INF = float('inf')


class TestBounded(TestCase):
    def test_init(self):
        bounded = Bounded()
        self.assertEqual(bounded.lower_bound, -_INF)
        self.assertEqual(bounded.upper_bound, _INF)

    def test_check_consistency(self):
        Bounded().check_consistency()

    def test_check_consistency_bounds(self):
        bounded = Bounded(2, 1)

        with self.assertRaises(AlbatrosError) as ctx:
            bounded.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Lower bound "2" is higher than upper bound "1"!'
        )

    def test_check_consistency_wrong_inf(self):
        b_lower = Bounded(lower_bound=_INF)

        with self.assertRaises(AlbatrosError) as ctx:
            b_lower.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Lower bound must not be equal to infinity!'
        )

        b_upper = Bounded(upper_bound=-_INF)

        with self.assertRaises(AlbatrosError) as ctx:
            b_upper.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Upper bound must not be equal to minus infinity!'
        )


class TestScaled(TestCase):
    def test_init(self):
        scaled = Scaled()
        self.assertEqual(scaled.scaling, 1.)
        self.assertEqual(scaled.offset, 0.)

    def test_check_consistency(self):
        Scaled().check_consistency()

    def test_check_consistency_scaling(self):
        s_scaling = Scaled(scaling=0)

        with self.assertRaises(AlbatrosError) as ctx:
            s_scaling.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Scaling must not be equal to zero!',
        )

    def test_check_consistency_offset_inf(self):
        s_offset_inf = Scaled(offset=_INF)

        with self.assertRaises(AlbatrosError) as ctx:
            s_offset_inf.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Offset must not be equal to infinity!',
        )

        s_offset_m_inf = Scaled(offset=-_INF)

        with self.assertRaises(AlbatrosError) as ctx:
            s_offset_m_inf.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Offset must not be equal to infinity!',
        )


class TestNamed(TestCase):
    def test_init(self):
        value = Named(name='varname')
        self.assertEqual(value.name, 'varname')

    def test_valid_name(self):
        Named('varname').check_consistency()

    def test_invalid_name_blank(self):
        value = Named('var name')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "var name" does not fullfil the isidentifier requirements!',
        )

    def test_invalid_name_number(self):
        value = Named('2')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "2" does not fullfil the isidentifier requirements!',
        )

    def test_invalid_name_empty(self):
        value = Named('')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "" does not fullfil the isidentifier requirements!',
        )


class Test_NamedScaledBounded(TestCase):
    def test_init(self):
        value = _NamedScaledBounded(name='varname')
        self.assertEqual(value.name, 'varname')
        self.assertEqual(value.lower_bound, -_INF)
        self.assertEqual(value.upper_bound, _INF)
        self.assertEqual(value.scaling, 1)
        self.assertEqual(value.offset, 0)

    def test_bounds(self):
        value = _NamedScaledBounded('varname', lower_bound=2, upper_bound=1)

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Lower bound "2" is higher than upper bound "1"!',
        )

    def test_scaling(self):
        value = _NamedScaledBounded('varname', scaling=0)

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Scaling must not be equal to zero!',
        )

    def test_invalid_name_blank(self):
        value = _NamedScaledBounded('var name')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "var name" does not fullfil the isidentifier requirements!',
        )

    def test_correct_inheritance(self):
        self.assertEqual(State.__base__, _NamedScaledBounded)
        self.assertEqual(Control.__base__, _NamedScaledBounded)
        self.assertEqual(Parameter.__base__, _NamedScaledBounded)
        self.assertEqual(Constraint.__base__, _NamedScaledBounded)


class TestCost(TestCase):
    def test_init(self):
        value = Cost(name='varname')
        self.assertEqual(value.name, 'varname')
        self.assertEqual(value.scaling, 1)
        self.assertEqual(value.offset, 0)

    def test_scaling(self):
        value = Cost('varname', scaling=0)

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Scaling must not be equal to zero!',
        )

    def test_invalid_name_blank(self):
        value = Cost('var name')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "var name" does not fullfil the isidentifier requirements!',
        )
