import ipopt


class IpoptWrapper:
    def __init__(self, problem):
        self.problem = problem

        self.ipopt = ipopt.problem(
            n=problem.n_z,
            m=problem.n_f,
            problem_obj=self,
            lb=problem.z_lower_bound,
            ub=problem.z_upper_bound,
            cl=problem.f_lower_bound,
            cu=problem.f_upper_bound,
        )

    def objective(self, z):
        return self.problem.evaluate_objective(z)
        # from time import sleep
        # sleep(0.05)
        # # TODO: HARD CODED FINAL TIME COST FUN
        # return self.problem.parameters[-1].value

    def gradient(self, z):
        return self.problem.evaluate_gradient(z)
        # grad = np.zeros(self.problem.n_z)
        # grad[0] = 1
        # return grad

    def constraints(self, z):
        return self.problem.evaluate_constraints(z)

    def jacobianstructure(self):
        return self.problem.jac_rows, self.problem.jac_cols

    def jacobian(self, z):
        return self.problem.evaluate_jacobian(z)

    def solve(self, z_initial=None):
        z_initial = z_initial if z_initial else self.problem.z_initial
        return self.ipopt.solve(z_initial)
