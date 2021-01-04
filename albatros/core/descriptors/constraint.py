from .named import Named
from .scaled import Scaled
from .bounded import Bounded
from .enableable import Enableable

import numpy as np


class Constraint(Named, Scaled, Bounded, Enableable):
    """Constraint optimization variable"""

    def __init__(self, name, lower_bound=-np.inf, upper_bound=np.inf, scaling=1, offset=0, enabled=True):
        Scaled.__init__(self, scaling, offset)
        Bounded.__init__(self, lower_bound, upper_bound)
        Named.__init__(self, name)
        Enableable.__init__(self, enabled)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Bounded.check_consistency(self)
        Named.check_consistency(self)
        Enableable.check_consistency(self)
