from unittest import TestCase

from .test_named import TestNamed

from albatros import Constant


class TestState(TestNamed, TestCase):
    def __init__(self, *args, **kwargs):
        func = lambda name, *ar, **kwar: Constant(name, 5, *ar, **kwar)  # noqa: E731
        TestNamed.__init__(self, *args, **kwargs, named_constructor=func)
        TestCase.__init__(self, *args, **kwargs)

    def test_constant_value_scalar(self):
        constant = Constant('const', 5)
        self.assertEqual(constant.value, 5)

    def test_constant_value_vector(self):
        constant = Constant('const', [1, 2, 3, 4, 5])
        self.assertEqual(constant.shape, (5, ))

    def test_constant_value_matrix(self):
        constant = Constant('const', [
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
        ])
        self.assertEqual(constant.shape, (3, 5))
