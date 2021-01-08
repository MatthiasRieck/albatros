from .indexedgrid import IndexedGrid


class ControlGrid(IndexedGrid):
    def __init__(self, controls, tau):
        super().__init__(controls, tau)
        self.interp_indices = None
        self.interp_values = None

    @property
    def controls(self):
        return self._descriptors

    def read_from_z(self, z):
        super().read_from_z(z)

        self.interp_values = self.values[self.interp_indices, :]
