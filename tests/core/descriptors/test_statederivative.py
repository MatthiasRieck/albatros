from unittest import TestCase

from albatros import State
from albatros.core.descriptors import StateDerivative


class TestStateDerivative(TestCase):
    def test_name(self):
        state = State('state_name')
        statederivative = StateDerivative(state)
        self.assertEqual(statederivative.name, 'state_name_dot')
