from unittest import TestCase

from albatros.core.core import AlbatrosException, assert_that, ConsistencyCheckable


class TestAlbatrosException(TestCase):
    def test_instance(self):
        self.assertIsInstance(AlbatrosException(), Exception)


class TestAssertThat(TestCase):
    def test_condition_true(self):
        assert_that(True, Exception('dummy'))

    def test_condition_false(self):
        with self.assertRaises(Exception):
            assert_that(False, Exception('dummy exception'))


class TestConsitencyCheckable(TestCase):
    def test_raises_not_implemented(self):
        with self.assertRaises(NotImplementedError):
            ConsistencyCheckable().check_consistency()