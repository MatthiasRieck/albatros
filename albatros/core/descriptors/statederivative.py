class StateDerivative:
    def __init__(self, state):
        self.state = state

    @property
    def name(self):
        return f'{self.state.name}_dot'
