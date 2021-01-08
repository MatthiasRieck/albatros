from .basegrid import BaseGrid


class ValueGrid(BaseGrid):
    def __init__(self, descriptors, tau):
        super().__init__(descriptors, tau)
        self.jacobians = None
