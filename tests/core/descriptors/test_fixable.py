from unittest import TestCase
from albatros import AlbatrosError
from albatros.core.descriptors import Fixable


class TestFixable(TestCase):
    def __init__(self, *args, fixable_constructor=Fixable, **kwargs):
        super().__init__(*args, **kwargs)
        self.fixable_constructor = fixable_constructor

    def test_fixable_init(self):
        fixable = self.fixable_constructor()
        self.assertEqual(fixable.is_fixed, False)

    def test_fixable_check_consistency(self):
        fixable = self.fixable_constructor(is_fixed=5)

        with self.assertRaises(AlbatrosError) as ctx:
            fixable.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Property is_fixed must be of type bool but is of type "int"!'
        )
