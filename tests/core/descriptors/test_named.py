from unittest import TestCase
from albatros.core.descriptors.named import Named
from albatros import AlbatrosError


class TestNamed(TestCase):
    def __init__(self, *args, named_constructor=Named, **kwargs):
        super().__init__(*args, **kwargs)
        self.named_constructor = named_constructor

    def test_named_init(self):
        value = self.named_constructor(name='varname')
        self.assertEqual(value.name, 'varname')

    def test_named_valid_name(self):
        self.named_constructor('varname').check_consistency()

    def test_named_invalid_name_blank(self):
        value = self.named_constructor('var name')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "var name" does not fullfil the isidentifier requirements!',
        )

    def test_named_invalid_name_number(self):
        value = self.named_constructor('2')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "2" does not fullfil the isidentifier requirements!',
        )

    def test_named_invalid_name_empty(self):
        value = self.named_constructor('')

        with self.assertRaises(AlbatrosError) as ctx:
            value.check_consistency()

        self.assertEqual(
            str(ctx.exception),
            'Name "" does not fullfil the isidentifier requirements!',
        )
