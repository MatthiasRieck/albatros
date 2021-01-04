from unittest import TestCase

from .test_bounded import TestBounded
from .test_scaled import TestScaled
from .test_named import TestNamed
from .test_enableable import TestEnableable

from albatros import Constraint


class TestState(TestNamed, TestBounded, TestScaled, TestEnableable, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda *ar, **kwar: Constraint('state', *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=Constraint)
        TestBounded.__init__(self, bounded_constructor=func)
        TestScaled.__init__(self, *args, **kwargs, scaled_constructor=func)
        TestEnableable.__init__(self, *args, **kwargs, enableable_constructor=func)
        TestCase.__init__(self, *args, **kwargs)
