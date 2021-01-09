from .phases import Phase
from albatros.integrators.trapezoidal import Trapezoidal

import hashlib
import numpy as np


class Problem:
    """Defines an optimization problem"""

    def __init__(self, name):
        self.name = name
        self.phases = []
        self.default_integrator = Trapezoidal

        self.parameters = []

        self._curr_z_md5 = ''

        self.n_z = None
        self.n_f = None

        self.jac_rows = None
        self.jac_cols = None

    def append_phase(self, phase):
        self.phases.append(phase)

    def add_phase(self, model, states, tau):
        phase = Phase(model, states, tau)
        self.append_phase(phase)
        return phase

    def prepare(self):
        params = []

        for phase in self.phases:
            params.extend(phase.prepare(self.default_integrator))

        self.parameters = list(set(params))

    def check_consistency(self):
        for phase in self.phases:
            phase.check_consistency()

    def complete_initial_guess(self):
        for p in self.parameters:
            p.complete_initial_guess()

        for phase in self.phases:
            phase.complete_initial_guess()

    def calculate_indices(self):
        z_ind = 0
        f_ind = 0

        for p in self.parameters:
            if p.is_fixed:
                p.index = np.nan
            else:
                p.index = z_ind
                z_ind += 1

        for phase in self.phases:
            z_ind, f_ind = phase.calculate_indices(z_ind, f_ind)

        self.n_z = z_ind
        self.n_f = f_ind

    def calculate_jac_sparsity(self):
        entries = []

        for phase in self.phases:
            entries.extend(phase.calculate_jac_sparsity())

        entries = set(entries)

        self.jac_rows = list(map(lambda x: x[0], entries))
        self.jac_cols = list(map(lambda x: x[1], entries))

        self.jac_nnz = len(self.jac_rows)
        print(f'Jacobian sparsity is {self.jac_nnz*100/(self.n_f * self.n_z)}')

        jac_lin_ind = list(range(self.jac_nnz))

        jac_lin_map = {}
        for entry, ind in zip(entries, jac_lin_ind):
            jac_lin_map[entry] = ind

        for phase in self.phases:
            phase.map_jac_sparsity(jac_lin_map)

    def create_z_f_vectors(self):
        z_ini = np.full(self.n_z, np.nan)
        z_lb = np.full(self.n_z, np.nan)
        z_ub = np.full(self.n_z, np.nan)

        f_lb = np.full(self.n_f, np.nan)
        f_ub = np.full(self.n_f, np.nan)

        for p in self.parameters:
            if not p.is_fixed:
                z_ini[p.index] = (p.value - p.offset) * p.scaling
                z_lb[p.index] = (p.lower_bound - p.offset) * p.scaling
                z_ub[p.index] = (p.upper_bound - p.offset) * p.scaling

        for phase in self.phases:
            z_ini, z_lb, z_ub, f_lb, f_ub = phase.create_z_f_vectors(z_ini, z_lb, z_ub, f_lb, f_ub)

        self.z_initial = z_ini
        self.z_lower_bound = z_lb
        self.z_upper_bound = z_ub

        self.f_lower_bound = f_lb
        self.f_upper_bound = f_ub

        # TODO: Check any isnan values

    def build(self):
        self.prepare()
        self.check_consistency()
        self.complete_initial_guess()
        self.calculate_indices()
        self.calculate_jac_sparsity()
        self.create_z_f_vectors()

    def evaluate(self, z):
        z_md5 = hashlib.md5(z).hexdigest()

        if z_md5 == self._curr_z_md5:
            return

        for p in self.parameters:
            if not p.is_fixed:
                p.value = (z[p.index] / p.scaling) + p.offset

        for phase in self.phases:
            phase.evaluate(z)

        self._curr_z_md5 = z_md5

    def evaluate_objective(self, z):
        self.evaluate(z)
        return self.phases[0].final_time.value

    def evaluate_gradient(self, z):
        grad = np.zeros(self.n_z)
        grad[0] = 1
        return grad

    def evaluate_constraints(self, z):
        self.evaluate(z)
        f = np.zeros(self.n_f)

        for phase in self.phases:
            f = phase.evaluate_constraints(f)

        return f

    def evaluate_jacobian(self, z):
        self.evaluate(z)

        jac = np.zeros(self.jac_nnz)

        for phase in self.phases:
            jac = phase.evaluate_jacobian(jac)

        return jac
