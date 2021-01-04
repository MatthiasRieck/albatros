from unittest import TestCase

from .test_bounded import TestBounded
from .test_scaled import TestScaled
from .test_named import TestNamed

from albatros import State


class TestState(TestNamed, TestBounded, TestScaled, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda *ar, **kwar: State('state', *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=State)
        TestBounded.__init__(self, bounded_constructor=func)
        TestScaled.__init__(self, *args, **kwargs, scaled_constructor=func)
        TestCase.__init__(self, *args, **kwargs)
