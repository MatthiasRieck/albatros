from albatros.core import AlbatrosError, assert_that


class Enableable():
    """Specifies whether an opimization constraint is considered in the optimization"""

    def __init__(self, enabled=True):
        self.enabled = enabled

    def check_consistency(self):
        assert_that(
            type(self.enabled) == bool,
            AlbatrosError(f'Property enabled must be of type bool but is of type "{type(self.enabled).__name__}"!')
        )
