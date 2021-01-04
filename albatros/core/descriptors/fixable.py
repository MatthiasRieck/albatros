from albatros.core import AlbatrosError, assert_that


class Fixable():
    """Enables an optimization variable to be fixed to a certain value"""

    def __init__(self, is_fixed=False):
        self.is_fixed = is_fixed

    def check_consistency(self):
        assert_that(
            type(self.is_fixed) == bool,
            AlbatrosError(f'Property is_fixed must be of type bool but is of type "{type(self.is_fixed).__name__}"!')
        )
