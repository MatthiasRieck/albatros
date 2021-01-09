import albatros as alba
from albatros.solvers.ipopt import IpoptWrapper
import numpy as np


def model_dynamics(states, controls):
    v = states[2]
    u = controls[0]

    g = 9.81

    x_dot = v * np.sin(u)
    y_dot = v * np.cos(u)
    v_dot = g * np.cos(u)

    states_dot = [x_dot, y_dot, v_dot]
    j_states_dot = [
        [0, 0, np.sin(u), v * np.cos(u)],
        [0, 0, np.cos(u), -v * np.sin(u)],
        [0, 0, 0, -g * np.sin(u)],
    ]

    return states_dot, j_states_dot


def test_brachistochrone(num_ts=301, x_fb=5, y_fb=4):
    states = [
        alba.State('x', lower_bound=0),
        alba.State('y', lower_bound=0),
        alba.State('v', lower_bound=0),
    ]

    controls = [
        alba.Control('u', lower_bound=0, upper_bound=np.pi),
    ]

    t_final = alba.Parameter('t_final', 5, lower_bound=0)

    problem = alba.Problem('brachistrochone')
    tau = np.linspace(0, 1, num_ts)

    model = alba.Model(model_dynamics, jac_sparsity=[[0, 0, 1, 1], [0, 0, 1, 1], [0, 0, 0, 1]])
    phase = problem.add_phase(model, states, tau)
    phase.add_controls(controls)
    phase.start_time = alba.Parameter('start_time', 0, is_fixed=True)
    phase.final_time = t_final
    phase.state_grid.set_start_bound(np.array([0, 0, 0]))
    phase.state_grid.set_final_bound([x_fb, y_fb, 0], [x_fb, y_fb, np.inf])

    problem.build()
    ipopt = IpoptWrapper(problem)
    ipopt.solve()

    x_opt = problem.phases[0].state_grid.values

    for i in range(len(tau)):
        assert np.abs(np.sqrt(2*9.81*x_opt[i, 1]) - x_opt[i, 2]) < 1e-4
