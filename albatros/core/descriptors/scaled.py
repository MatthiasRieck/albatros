from albatros.core.core import assert_that, AlbatrosError
import numpy as np


class Scaled():
    """Enables an optimization variable to describe a scaling and offset"""

    def __init__(self, scaling=1., offset=0.):
        self.scaling = scaling
        self.offset = offset

    def check_consistency(self):
        assert_that(
            self.scaling != 0.,
            AlbatrosError('Scaling must not be equal to zero!'),
        )
        assert_that(
            self.offset != np.inf and self.offset != -np.inf,
            AlbatrosError('Offset must not be equal to infinity!')
        )
