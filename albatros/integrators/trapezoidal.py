from albatros.discretization.grids import StateGrid

import numpy as np

DEFECT_MULT = 10


class Trapezoidal:
    def __init__(self):
        self.defect_grid = None
        self.state_grid = None
        self.control_grids = None
        self.start_time = None
        self.final_time = None
        self.model = None

        self.tf_entries = []
        self.tf_lin_ind = None

        self.jac_i_entries = []
        self.jac_i_lin_ind = None

        self.jac_ip1_entries = []
        self.jac_ip1_lin_ind = None

        self.x_i_entries = []
        self.x_i_lin_ind = None

        self.x_ip1_entries = []
        self.x_ip1_lin_ind = None

    def prepare(self, state_grid, control_grids, model, start_time, final_time):
        self.state_grid = state_grid
        self.control_grids = control_grids
        # TODO: DefectGrid???
        self.defect_grid = StateGrid(self.state_grid.states, self.state_grid.tau[0:-1])
        self.start_time = start_time

        assert self.start_time.is_fixed
        self.final_time = final_time

        self.model = model

    def calculate_jac_sparsity(self):
        jac_sparsity = self.model.jac_sparsity
        for i in range(len(self.defect_grid.tau)):
            ind_x_i = self.state_grid.indices[i]
            ind_x_ip1 = self.state_grid.indices[i+1]

            ind_u_i = np.concatenate(list(map(lambda x: x.indices[i], self.control_grids)))
            ind_u_ip1 = np.concatenate(list(map(lambda x: x.indices[i+1], self.control_grids)))

            ind_d_i = self.defect_grid.indices[i]

            # defect tf
            self.tf_entries.extend(list(map(lambda x: (x[0], self.final_time.index), zip(ind_d_i, ind_x_i))))

            # defect_jac_i
            row_matrix = np.tile(ind_d_i.reshape(3, 1), [1, 4])
            rows = row_matrix[jac_sparsity]

            ind_z_i = np.concatenate((ind_x_i, ind_u_i))
            colmatrix = np.tile(ind_z_i.reshape(1, 4), [3, 1])
            cols = colmatrix[jac_sparsity]

            self.jac_i_entries.extend(list(map(lambda x: (x[0], x[1]), zip(rows, cols))))

            # defect_jac_ip1
            row_matrix = np.tile(ind_d_i.reshape(3, 1), [1, 4])
            rows = row_matrix[jac_sparsity]

            ind_z_ip1 = np.concatenate((ind_x_ip1, ind_u_ip1))
            colmatrix = np.tile(ind_z_ip1.reshape(1, 4), [3, 1])
            cols = colmatrix[jac_sparsity]

            self.jac_ip1_entries.extend(list(map(lambda x: (x[0], x[1]), zip(rows, cols))))

            # defect_x_i
            self.x_i_entries.extend(list(map(lambda x: (x[0], x[1]), zip(ind_d_i, ind_x_i))))

            # defect_x_ip1
            self.x_ip1_entries.extend(list(map(lambda x: (x[0], x[1]), zip(ind_d_i, ind_x_ip1))))

        return self.tf_entries + self.jac_i_entries + self.jac_ip1_entries + self.x_i_entries + self.x_ip1_entries

    def create_f_vectors(self, f_lb, f_ub):
        f_lb[self.defect_grid.indices] = 0
        f_ub[self.defect_grid.indices] = 0

        return f_lb, f_ub

    def map_jac_sparsity(self, jac_lin_map):
        self.tf_lin_ind = list(map(lambda x: jac_lin_map[x], self.tf_entries))
        self.jac_i_lin_ind = list(map(lambda x: jac_lin_map[x], self.jac_i_entries))
        self.jac_ip1_lin_ind = list(map(lambda x: jac_lin_map[x], self.jac_ip1_entries))
        self.x_i_lin_ind = list(map(lambda x: jac_lin_map[x], self.x_i_entries))
        self.x_ip1_lin_ind = list(map(lambda x: jac_lin_map[x], self.x_ip1_entries))

    def evaluate_constraints(self, f, start_time, final_time, states_dot_grid):
        tau = self.state_grid.tau
        h = np.tile(np.diff(tau).reshape(-1, 1), [1, len(self.state_grid.states)])

        t0 = self.start_time.value
        tf = self.final_time.value

        x_i = np.array(self.state_grid.values[:-1][:])
        x_ip1 = np.array(self.state_grid.values[1:][:])

        x_dot_i = np.array(states_dot_grid.values[:-1][:])
        x_dot_ip1 = np.array(states_dot_grid.values[1:][:])

        defects = x_i + (x_dot_i + x_dot_ip1) * h * (tf-t0) / 2 - x_ip1

        # defects[:][3] *=DEFECT_MULT

        f[self.defect_grid.indices] += defects

        return f

    def evaluate_jacobian(self, jac, start_time, final_time, states_dot_grid):
        jac_sparsity = self.model.jac_sparsity
        jac[self.x_i_lin_ind] += 1
        jac[self.x_ip1_lin_ind] += -1

        assert start_time.is_fixed

        tau = self.state_grid.tau
        # TODO: Test: in case of constant diff may want to resort to scalar h for speed
        h = np.tile(np.diff(tau).reshape(-1, 1), [1, len(self.state_grid.states)])
        H = np.tile(np.diff(tau).reshape(-1, 1, 1), [1, len(self.state_grid.states), 4])

        t0 = self.start_time.value
        tf = self.final_time.value

        x_dot_i = np.array(states_dot_grid.values[:-1][:])
        x_dot_ip1 = np.array(states_dot_grid.values[1:][:])

        j_x_dot_i = np.array(states_dot_grid.jacobians[:-1][:][:])
        j_x_dot_ip1 = np.array(states_dot_grid.jacobians[1:][:][:])

        # tf
        jac[self.tf_lin_ind] += ((x_dot_i + x_dot_ip1) * h / 2).flatten()

        vals = []
        for i in range(len(tau)-1):
            jac_i = (tf - t0) * H[i] * j_x_dot_i[i] / 2
            # jac_i[2,:] *= DEFECT_MULT
            vals.extend(jac_i[jac_sparsity])
        jac[self.jac_i_lin_ind] += vals

        vals = []
        for i in range(len(tau)-1):
            jac_i = (tf - t0) * H[i] * j_x_dot_ip1[i] / 2
            # jac_i[2,:] *= DEFECT_MULT
            vals.extend(jac_i[jac_sparsity])
        jac[self.jac_ip1_lin_ind] += vals

        return jac
