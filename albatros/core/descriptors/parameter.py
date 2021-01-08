from .named import Named
from .scaled import Scaled
from .bounded import Bounded
from .fixable import Fixable

from albatros.core import assert_that, AlbatrosError
from albatros.core.utils import get_initial_guess

import numpy as np


class Parameter(Named, Scaled, Bounded, Fixable):
    """Parameter optimization variable"""

    def __init__(self, name, value=np.nan, lower_bound=-np.inf, upper_bound=np.inf, scaling=1, offset=0, is_fixed=False):  # noqa: E501
        Scaled.__init__(self, scaling, offset)
        Bounded.__init__(self, lower_bound, upper_bound)
        Named.__init__(self, name)
        Fixable.__init__(self, is_fixed)

        self.value = value
        self.index = np.nan

    def check_consistency(self):
        Scaled.check_consistency(self)
        Bounded.check_consistency(self)
        Named.check_consistency(self)
        Fixable.check_consistency(self)

        if self.value:
            assert_that(
                isinstance(self.value, (float, int)),
                AlbatrosError(f'Parameter value "{self.name}" must be numeric but is "{type(self.value).__name__}"!'),
            )
            self.value = float(self.value)

            assert_that(
                not np.isnan(self.value) and not np.isinf(self.value),
                AlbatrosError(f'Parameter "{self.name}" has invalid value "{self.value}"!')
            )

        if not self.is_fixed:
            assert_that(
                self.value >= self.lower_bound,
                AlbatrosError(
                    f'Value "{self.value}" of parameter "{self.name}" is below lower bound "{self.lower_bound}"!',
                ),
            )
            assert_that(
                self.value <= self.upper_bound,
                AlbatrosError(
                    f'Value "{self.value}" of parameter "{self.name}" is higher than upper bound "{self.upper_bound}"!',
                ),
            )

    def complete_initial_guess(self):
        if self.is_fixed:
            return

        if not np.isnan(self.value):
            return

        try:
            self.value = get_initial_guess(self.lower_bound, self.upper_bound)
        except AlbatrosError:
            raise AlbatrosError(f'The initial guess for parameter "{self.name}" cannot automatically generated!')
