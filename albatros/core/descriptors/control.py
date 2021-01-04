from .named import Named
from .scaled import Scaled
from .bounded import Bounded
from .fixable import Fixable

import numpy as np


class Control(Named, Scaled, Bounded, Fixable):
    """Control optimization variable"""

    def __init__(self, name, lower_bound=-np.inf, upper_bound=np.inf, scaling=1, offset=0, is_fixed=False):
        Scaled.__init__(self, scaling, offset)
        Bounded.__init__(self, lower_bound, upper_bound)
        Named.__init__(self, name)
        Fixable.__init__(self, is_fixed)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Bounded.check_consistency(self)
        Named.check_consistency(self)
        Fixable.check_consistency(self)
