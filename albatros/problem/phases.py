from albatros.discretization.grids import StateGrid, ControlGrid, StateDerivativeGrid
from albatros.discretization.utils import interpolation_indices


class Phase:
    """Defines an Optimization Phase"""

    def __init__(self, model, states, tau):
        self.model = model
        self.states = states
        self.tau = tau
        self.state_grid = StateGrid(states, tau)
        state_derivatives = list(map(lambda x: x.derivative, states))
        self.state_derivative_grid = StateDerivativeGrid(state_derivatives, tau)
        self.control_grids = []
        # self.output_grid = None
        self.start_time = None
        self.final_time = None
        self.integrator = None

    def add_controls(self, controls, tau=None):
        tau = tau if tau else self.tau
        control_grid = ControlGrid(controls, tau)
        self.control_grids.append(control_grid)
        return control_grid

    def set_outputs(self, outputs):
        raise NotImplementedError

    def prepare(self, default_integrator):
        if not self.integrator:
            self.integrator = default_integrator()
        self.integrator.prepare(self.state_grid, self.control_grids, self.model, self.start_time, self.final_time)
        return [self.start_time, self.final_time]

    def check_consistency(self):
        # self.state_grid.check_consistency()
        # for control_grid in self.control_grids:
        #     control_grid.check_consistency()
        # self.output_grid.check_consistency()
        # TODO: Check name uniqueness
        # TODO: Check grid consistency
        # raise NotImplementedError
        pass

    def complete_initial_guess(self):
        self.state_grid.complete_initial_guess()
        for cg in self.control_grids:
            cg.complete_initial_guess()

    def calculate_indices(self, z_ind, f_ind):
        for control_grid in self.control_grids:
            control_grid.interp_indices = interpolation_indices(self.state_grid.tau, control_grid.tau)

        cg_curr_ind = [0] * len(self.control_grids)

        for i in range(len(self.state_grid.tau)):
            state_tau = self.state_grid.tau[i]
            self.state_grid.indices[i], z_ind = get_index_range(z_ind, len(self.state_grid.states))

            for k in range(len(self.control_grids)):
                cg = self.control_grids[k]
                cg_i = cg_curr_ind[k]
                control_tau = self.control_grids[k].tau[cg_i]
                if control_tau == state_tau:
                    self.control_grids[k].indices[cg_i], z_ind = get_index_range(z_ind, len(cg.controls))
                    cg_curr_ind[k] += 1

        for i in range(len(self.integrator.defect_grid.tau)):
            self.integrator.defect_grid.indices[i], f_ind = get_index_range(f_ind, len(self.state_grid.states))

        return z_ind, f_ind

    def calculate_jac_sparsity(self):
        entries = []
        entries.extend(self.integrator.calculate_jac_sparsity())
        return entries

    def map_jac_sparsity(self, jac_lin_map):
        self.integrator.map_jac_sparsity(jac_lin_map)

    def create_z_f_vectors(self, z_ini, z_lb, z_ub, f_lb, f_ub):
        z_ini = self.state_grid.write_to_z(z_ini)
        z_lb, z_ub = self.state_grid.write_bounds(z_lb, z_ub)

        for cg in self.control_grids:
            z_ini = cg.write_to_z(z_ini)
            z_lb, z_ub = cg.write_bounds(z_lb, z_ub)

        f_lb, f_ub = self.integrator.create_f_vectors(f_lb, f_ub)

        return z_ini, z_lb, z_ub, f_lb, f_ub

    def evaluate(self, z):
        self.state_grid.read_from_z(z)
        for cg in self.control_grids:
            cg.read_from_z(z)

        assert len(self.control_grids) == 1
        interp_controls = self.control_grids[0].interp_values

        self.state_derivative_grid.values, self.state_derivative_grid.jacobians = self.model.evaluate(
            self.state_grid.values,
            interp_controls,
        )

    def evaluate_constraints(self, f):
        f = self.integrator.evaluate_constraints(f, self.start_time, self.final_time, self.state_derivative_grid)
        return f

    def evaluate_jacobian(self, jac):
        jac = self.integrator.evaluate_jacobian(jac, self.start_time, self.final_time, self.state_derivative_grid)
        return jac


def get_index_range(z_ind, n):
    inds = range(z_ind, z_ind+n)
    return inds, z_ind+n
