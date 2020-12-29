from unittest import TestCase

from albatros.evaluators.model import repack_slices, Model


class TestRepackSlices(TestCase):
    def test_repack_scalar(self):
        val = repack_slices([(1,), (2,), (3,)])
        self.assertEqual(val, ([1, 2, 3],))

    def test_repack_twin(self):
        val = repack_slices([(1, 2), (3, 4), (5, 6)])
        self.assertEqual(val, ([1, 3, 5], [2, 4, 6]))


class TestModel(TestCase):
    def test_evaluate(self):
        model = Model(lambda x, u: (x*u,))
        values, = model.evaluate([1, 2, 3], [1, 2, 3])
        self.assertEqual(values, [1, 4, 9])
