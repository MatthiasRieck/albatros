from .named import Named
from .scaled import Scaled


class Cost(Named, Scaled):
    """Cost optimization variable"""

    def __init__(self, name, scaling=1, offset=0):
        Scaled.__init__(self, scaling, offset)
        Named.__init__(self, name)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Named.check_consistency(self)
