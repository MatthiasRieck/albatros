from unittest import TestCase

from .test_bounded import TestBounded
from .test_scaled import TestScaled
from .test_named import TestNamed
from .test_fixable import TestFixable

from albatros import Control


class TestState(TestNamed, TestBounded, TestScaled, TestFixable, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda *ar, **kwar: Control('state', *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=Control)
        TestBounded.__init__(self, bounded_constructor=func)
        TestScaled.__init__(self, *args, **kwargs, scaled_constructor=func)
        TestFixable.__init__(self, *args, **kwargs, fixable_constructor=func)
        TestCase.__init__(self, *args, **kwargs)
