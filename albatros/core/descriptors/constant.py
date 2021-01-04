from .named import Named

import numpy as np


class Constant(Named):
    """Constant value"""

    def __init__(self, name, value):
        Named.__init__(self, name)
        self.value = value

        if type(self.value) is not np.ndarray:
            self.value = np.array(self.value)

    @property
    def shape(self):
        return self.value.shape
