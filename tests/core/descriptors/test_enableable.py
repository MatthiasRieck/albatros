from unittest import TestCase
from albatros import AlbatrosError
from albatros.core.descriptors import Enableable


class TestEnableable(TestCase):
    def __init__(self, *args, enableable_constructor=Enableable, **kwargs):
        super().__init__(*args, **kwargs)
        self.enableable_constructor = enableable_constructor

    def test_enableable_init(self):
        enableable = self.enableable_constructor()
        self.assertEqual(enableable.enabled, True)

    def test_enableable_check_consistency(self):
        enableable = self.enableable_constructor(enabled=5)

        with self.assertRaises(AlbatrosError) as ctx:
            enableable.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Property enabled must be of type bool but is of type "int"!'
        )
