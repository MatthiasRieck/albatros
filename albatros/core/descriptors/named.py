from albatros.core.core import AlbatrosError, assert_that


class Named():
    """Enables an optimization variable to describe a name"""

    def __init__(self, name):
        self.name = name

    def check_consistency(self):
        assert_that(
            self.name.isidentifier(),
            AlbatrosError(f'Name "{self.name}" does not fullfil the isidentifier requirements!')
        )
