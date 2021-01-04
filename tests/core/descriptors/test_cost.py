from unittest import TestCase

from .test_scaled import TestScaled
from .test_named import TestNamed

from albatros import Cost


class TestState(TestNamed, TestScaled, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda *ar, **kwar: Cost('state', *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=Cost)
        TestScaled.__init__(self, *args, **kwargs, scaled_constructor=func)
        TestCase.__init__(self, *args, **kwargs)
