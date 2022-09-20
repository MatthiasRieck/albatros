from albatros.discretization.grids import StateGrid

import numpy as np


def repack_slices(slices):
    """Repacks the slices of the model evaluate execution"""

    # This implementation has been tested with the following code
    # values = [(1, 2, 3,)] * 10001
    # t = time.time()
    # for _ in range(100):
    #     val = repack_slices(values)
    # elapsed = (time.time() - t)/100
    # print(elapsed) --> 0.002648179531097412
    return tuple(map(lambda x: list(x), (zip(*tuple(slices)))))


class Model:
    """Executes the model dynamics step function"""
    def __init__(self, step_fun, states, jac_sparsity=None):
        self.states = states
        self.step_fun = step_fun
        self.jac_sparsity = np.array(jac_sparsity, dtype=bool)

    def evaluate(self, *args):
        out_slices = []

        for in_slice in zip(*args):
            out_slices.append(self.step_fun(*in_slice))

        return repack_slices(out_slices)
