from .core import AlbatrosException, ConsistencyCheckable, assert_that


_INF = float('inf')


class Bounded(ConsistencyCheckable):
    """Enables an optimization variable to describe a lower and upper bound"""

    def __init__(self, lower_bound=-_INF, upper_bound=_INF):
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

    def check_consistency(self):
        assert_that(
            self.lower_bound <= self.upper_bound,
            AlbatrosException(f'Lower bound "{self.lower_bound}" is higher than upper bound "{self.upper_bound}"!')
        )
        assert_that(
            self.upper_bound != -_INF,
            AlbatrosException('Upper bound must not be equal to minus infinity!'),
        )
        assert_that(
            self.lower_bound != _INF,
            AlbatrosException('Lower bound must not be equal to infinity!'),
        )


class Scaled(ConsistencyCheckable):
    """Enables an optimization variable to describe a scaling and offset"""

    def __init__(self, scaling=1., offset=0.):
        self.scaling = scaling
        self.offset = offset

    def check_consistency(self):
        assert_that(
            self.scaling != 0.,
            AlbatrosException('Scaling must not be equal to zero!'),
        )
        assert_that(
            self.offset != _INF and self.offset != -_INF,
            AlbatrosException('Offset must not be equal to infinity!')
        )


class Named(ConsistencyCheckable):
    """Enables an optimization variable to describe a name"""

    def __init__(self, name):
        self.name = name

    def check_consistency(self):
        assert_that(
            self.name.isidentifier(),
            AlbatrosException(f'Name "{self.name}" does not fullfil the isidentifier requirements!')
        )


class _NamedScaledBounded(Named, Scaled, Bounded, ConsistencyCheckable):
    """Optimization variable with name, bound, scaling, and offset"""

    def __init__(self, name, lower_bound=-_INF, upper_bound=_INF, scaling=1, offset=0):
        Scaled.__init__(self, scaling, offset)
        Bounded.__init__(self, lower_bound, upper_bound)
        Named.__init__(self, name)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Bounded.check_consistency(self)
        Named.check_consistency(self)


class State(_NamedScaledBounded):
    """State optimization variable"""


class Control(_NamedScaledBounded):
    """Control optimization variable"""


class Parameter(_NamedScaledBounded):
    """Parameter optimization variable"""


class Constraint(_NamedScaledBounded):
    """Constraint optimization variable"""


class Cost(Named, Scaled, ConsistencyCheckable):
    """Cost optimization variable"""

    def __init__(self, name, scaling=1, offset=0):
        Scaled.__init__(self, scaling, offset)
        Named.__init__(self, name)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Named.check_consistency(self)
