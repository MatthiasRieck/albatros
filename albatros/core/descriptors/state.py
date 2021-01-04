from .named import Named
from .scaled import Scaled
from .bounded import Bounded
from .statederivative import StateDerivative

import numpy as np


class State(Named, Scaled, Bounded):
    """State optimization variable"""

    def __init__(self, name, lower_bound=-np.inf, upper_bound=np.inf, scaling=1, offset=0):
        Scaled.__init__(self, scaling, offset)
        Bounded.__init__(self, lower_bound, upper_bound)
        Named.__init__(self, name)

        self.derivative = StateDerivative(self)

    def check_consistency(self):
        Scaled.check_consistency(self)
        Bounded.check_consistency(self)
        Named.check_consistency(self)
