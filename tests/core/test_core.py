from unittest import TestCase

from albatros.core.core import AlbatrosError, assert_that


class TestAlbatrosError(TestCase):
    def test_instance(self):
        self.assertIsInstance(AlbatrosError(), Exception)


class TestAssertThat(TestCase):
    def test_condition_true(self):
        assert_that(True, Exception('dummy'))

    def test_condition_false(self):
        with self.assertRaises(Exception):
            assert_that(False, Exception('dummy exception'))
